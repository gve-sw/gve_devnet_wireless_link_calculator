""" Copyright (c) 2020 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied. 
"""

# Import Section
from flask import Flask, render_template, request, redirect
import json, os, webexteamssdk
from dotenv import load_dotenv

import radio1
import radio2

# load all environment variables
load_dotenv()

# Global variables
app = Flask(__name__)

def get_json(filename):
    with open(filename ,'r') as f:
        return json.load(f)

def write_json(data, filename):
    with open(filename ,'w') as f:
        json.dump(data, f, indent=2)

## Routes

#Index
@app.route('/', methods=["GET","POST"])
def index():
    if request.method == "GET":
        try:
            # Page without error message and defined header links 
            return render_template('settings.html', settings = get_json('settings.json'), devices = get_json('devices.json'), antennas = get_json('antennas.json'), cables = get_json('cables.json'), hiddenLinks=True)
        except Exception as e: 
            print(e)
            return render_template('settings.html', settings = get_json('settings.json'), devices = get_json('devices.json'), antennas = get_json('antennas.json'), cables = get_json('cables.json'), hiddenLinks=True)
    else:
        # try:
            freq = request.form.get('frequency')

            settings = {
                'rxdevice' : request.form.get('rxdevice'),
                'txdevice' : request.form.get('txdevice'),
                'rxcable' : request.form.get('rxcable'),
                'rxantenna' : request.form.get('rxantenna'),
                'txcable' : request.form.get('txcable'),
                'txantenna' : request.form.get('txantenna'),
                'frequency' : freq,
                'desiredrange' : float(request.form.get('range'))/1.609,
                'desiredrate' : int(request.form.get('datarate')),
                'domain' : request.form.get('domain'),
                'bandwidth' : request.form.get('bandwidth'),
                'channel' : request.form.get('channel'),
                'height1' : int(request.form.get('height1')),
                'height2' : int(request.form.get('height2'))
            }

            metrics = []
            if freq == "2.4ghz":
                metrics = radio1.get_metrics(settings)
            else:
                metrics = radio2.get_metrics(settings)

                return render_template('settings.html', settings = get_json('settings.json'), devices = get_json('devices.json'), antennas = get_json('antennas.json'), cables = get_json('cables.json'), hiddenLinks=True, calculated = True, metrics = metrics)
        # except Exception as e: 
        #     print(e)  
        #     return render_template('settings.html', settings = get_json('settings.json'), devices = get_json('devices.json'), antennas = get_json('antennas.json'), cables = get_json('cables.json'), hiddenLinks=True, error=True, errormessage="Make sure either the range- or rate-field is non-zero.", errorcode=e)

@app.route('/add-device', methods=["GET","POST"])
def add_device():
    if request.method == "POST":
        device = {
            "2.4ghz": {
                "spatial-streams" : int(request.form.get('ss1')),
                "mcs-limit" : int(request.form.get('mcs1')),
                "beamforming" : int(request.form.get('bf1')),
                "tx-ss" : int(request.form.get('txss1')),
                "rx-ss" : int(request.form.get('rxss1')),
                "noise-figure" : int(request.form.get('nf1')),
                "builtin-antenna" : request.form.get('bi1'),
                "PL": {
                    "PL1" : int(request.form.get('pl11')),
                    "PL2" : int(request.form.get('pl21')),
                }
            },
            "5ghz": {
                "spatial-streams" : int(request.form.get('ss2')),
                "mcs-limit" : int(request.form.get('mcs2')),
                "beamforming" : int(request.form.get('bf2')),
                "tx-ss" : int(request.form.get('txss2')),
                "rx-ss" : int(request.form.get('rxss2')),
                "noise-figure" : int(request.form.get('nf2')),
                "builtin-antenna" : request.form.get('bi2'),
                "PL": {
                    "PL1" : int(request.form.get('pl12')),
                    "PL2" : int(request.form.get('pl22')),
                }
            }
        }
        name = request.form.get('model')
        devices = get_json('devices.json')
        devices[name] = device
        write_json(devices, 'devices.json')
        send_files_on_webex()
        return redirect('/p2ptool/')

    return render_template('add_device.html', antennas=get_json('antennas.json'))

@app.route('/add-antenna', methods=["GET","POST"])
def add_antenna():
    if request.method == "POST":
        frequency = request.form.get('frequency')
        gain = int(request.form.get('gain'))
        model = request.form.get('model')
        antennas = get_json('antennas.json')
        antennas[frequency][model] = gain
        write_json(antennas, 'antennas.json')
        send_files_on_webex()
        return redirect('/p2ptool/')

    return render_template('add_antenna.html')

@app.route('/add-cable', methods=["GET","POST"])
def add_cable():
    if request.method == "POST":
        frequency = request.form.get('frequency')
        loss = int(request.form.get('loss'))
        name = request.form.get('name')
        cables = get_json('cables.json')
        cables[frequency][name] = loss
        write_json(cables, 'cables.json')
        send_files_on_webex()
        return redirect('/p2ptool/')

    return render_template('add_cable.html')

def send_files_on_webex():
    token = "ZTJhNDNjNDktM2E5MC00MWI3LTk2YTktMDFjNTM3ZDY1MWQwMDE1ODI4Y2QtOGU3_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f"
    api = webexteamssdk.WebexTeamsAPI(access_token=token)
    api.messages.create(toPersonEmail="stienvan@cisco.com", files=[os.path.abspath("antennas.json")])
    api.messages.create(toPersonEmail="stienvan@cisco.com", files=[os.path.abspath("devices.json")])
    api.messages.create(toPersonEmail="stienvan@cisco.com", files=[os.path.abspath("cables.json")])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5678, debug=True)