import os
import subprocess

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


def run_command(command):
    result = subprocess.run(
        command, capture_output=True, text=True, check=True)
    return result.stdout


def adb_process(commands):
    results = {}
    try:
        kill_server_result = run_command(['adb', 'kill-server'])
        results['kill-server'] = kill_server_result

        start_server_result = run_command(['adb', 'start-server'])
        results['start-server'] = start_server_result

        for command in commands:
            command_result = run_command(command)
            results[command[0]] = command_result

    except subprocess.CalledProcessError as e:
        results['error'] = f"An error occurred: {e.stderr}"

    except Exception as e:
        results['error'] = f"An unexpected error occurred: {e}"

    return results


@app.route('/')
def home():
    try:
        file_names = os.listdir('files')
    except FileNotFoundError:
        file_names = []
    # 내림차순 정렬
    sorted_file_names = sorted(file_names, reverse=True)
    return render_template('home.html', options=sorted_file_names)


@app.route('/pair', methods=['POST'])
def pair():
    ip_address = request.form['ipAddress']
    pairing_code = request.form['pairingCode']
    if not ip_address:
        return jsonify({'error': 'IP address is required.'})
    if not pairing_code:
        return jsonify({'error': 'Pairing code is required.'})

    commands = [
        ['adb', 'pair', ip_address, pairing_code],
        ['adb', 'connect', ip_address]
    ]
    results = adb_process(commands)
    return jsonify(results)


@app.route('/install', methods=['POST'])
def install():
    selected_option = request.form['options']
    ip_address = request.form['ipAddress']
    if not ip_address:
        return jsonify({'error': 'IP address is required.'})
    if not selected_option:
        return jsonify({'error': 'An option is required.'})
    
    commands = [
        ['adb', 'connect', ip_address],
        ['adb', 'install', f'./files/{selected_option}']
    ]
    results = adb_process(commands)
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
