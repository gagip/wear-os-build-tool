import os
import subprocess

from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

FILES_DIR = "files"

# adb 명령이 멈춰도 웹 요청이 무한 대기하지 않도록 timeout(초)을 둔다.
# install은 apk 전송 때문에 더 넉넉히 잡는다.
DEFAULT_TIMEOUT_SECONDS = 30
INSTALL_TIMEOUT_SECONDS = 300


def run_command(command, timeout=DEFAULT_TIMEOUT_SECONDS):
    result = subprocess.run(
        command, capture_output=True, text=True, check=True, timeout=timeout
    )
    return result.stdout


def adb_process(commands):
    results = {}
    try:
        kill_server_result = run_command(["adb", "kill-server"])
        results["kill-server"] = kill_server_result

        start_server_result = run_command(["adb", "start-server"])
        results["start-server"] = start_server_result

        for command in commands:
            timeout = (
                INSTALL_TIMEOUT_SECONDS
                if "install" in command
                else DEFAULT_TIMEOUT_SECONDS
            )
            command_result = run_command(command, timeout=timeout)
            results[command[0]] = command_result

    except subprocess.TimeoutExpired as e:
        results["error"] = f"Command timed out after {e.timeout}s: {' '.join(e.cmd)}"

    except subprocess.CalledProcessError as e:
        results["error"] = f"An error occurred: {e.stderr}"

    except Exception as e:
        results["error"] = f"An unexpected error occurred: {e}"

    return results


@app.route("/")
def home():
    try:
        file_names = os.listdir(FILES_DIR)
    except FileNotFoundError:
        file_names = []
    # 내림차순 정렬
    sorted_file_names = sorted(file_names, reverse=True)
    return render_template("home.html", options=sorted_file_names)


@app.route("/pair", methods=["POST"])
def pair():
    ip_address = request.form["ipAddress"]
    pairing_code = request.form["pairingCode"]
    if not ip_address:
        return jsonify({"error": "IP address is required."})
    if not pairing_code:
        return jsonify({"error": "Pairing code is required."})

    commands = [
        ["adb", "pair", ip_address, pairing_code],
    ]
    results = adb_process(commands)
    return jsonify(results)


@app.route("/install", methods=["POST"])
def install():
    selected_option = request.form["options"]
    ip_address = request.form["ipAddress"]
    if not ip_address:
        return jsonify({"error": "IP address is required."})
    if not selected_option:
        return jsonify({"error": "An option is required."})

    commands = [
        ["adb", "connect", ip_address],
        ["adb", "install", f"./{FILES_DIR}/{selected_option}"],
    ]
    results = adb_process(commands)
    return jsonify(results)


@app.route("/upload", methods=["POST"])
def upload():
    # 프로세스 경계(HTTP 멀티파트 업로드) — 잘못된 입력은 Result처럼 JSON 에러로 반환한다.
    uploaded = request.files.get("apk")
    if uploaded is None or uploaded.filename == "":
        return jsonify({"error": "APK file is required."})

    filename = secure_filename(uploaded.filename)
    if not filename.lower().endswith(".apk"):
        return jsonify({"error": "Only .apk files are allowed."})

    # files/ 폴더가 없으면 생성하고, 같은 이름이면 덮어쓴다.
    os.makedirs(FILES_DIR, exist_ok=True)
    save_path = os.path.join(FILES_DIR, filename)
    try:
        uploaded.save(save_path)
    except OSError as e:
        return jsonify({"error": f"Failed to save file: {e}"})

    return jsonify({"upload": f"Saved as {filename}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
