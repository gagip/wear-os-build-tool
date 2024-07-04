import subprocess
import os
from flask import Flask, render_template, request

app = Flask(__name__)


def run_commend(commend):
    result = subprocess.run(
        commend, capture_output=True, text=True, check=True)
    return result.stdout


@app.route('/')
def home():
    try:
        file_names = os.listdir('files')
    except FileNotFoundError:
        file_names = []
    return render_template('home.html', options=file_names)


@app.route('/install', methods=['POST'])
def process():
    selected_option = request.form['options']
    ip_address = request.form['ipAddress']
    pairing_code = request.form['pairingCode']
    results = {}

    try:
        kill_server_result = run_commend(
            ['adb', 'kill-server'])
        results['kill-server'] = kill_server_result

        start_server_result = run_commend(
            ['adb', 'start-server'])
        results['start-server'] = start_server_result

        if pairing_code:
            pair_result = run_commend(
                ['adb', 'pair', ip_address, pairing_code])
            results['pair'] = pair_result

        connect_result = run_commend(
            ['adb', 'connect', ip_address])
        results['connect'] = connect_result

        install_result = run_commend(
            ['adb', 'install', f'./files/{selected_option}'])
        results['install'] = install_result

    except subprocess.CalledProcessError as e:
        results['error'] = f"An error occurred: {e.stderr}"

    except Exception as e:
        results['error'] = f"An unexpected error occurred: {e}"

    return render_template(
        'home.html',
        options=os.listdir('files'),
        results=results
    )


if __name__ == '__main__':
    app.run(debug=True)
