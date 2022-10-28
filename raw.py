import json
from ssl import get_server_certificate

# Basic config
def get_setting(key):
    with open('settings.json', 'r') as f:
        settings = json.load(f)
        return settings[key]

def get_json(filename):
    with open(filename ,'r') as f:
        return json.load(f)

def get_tx_device():
    return get_json('devices.json')[get_setting('rxdevice')]

def get_rx_device():
    return get_json('devices.json')[get_setting('txdevice')]

def get_snr():
    return get_json('snr.json')

def get_cable_loss():
    return get_json('cables.json')

def get_antenna_gain():
    return get_json('antennas.json')

# Raw values
MCS_TO_RANGE_RAD1 = [17.63, 15.23, 14.34, 11.18, 8.56, 5.91, 5.14, 4.46, 3.08, 2.68, 14.45, 10.18, 6.63]
MCS_TO_RATE_RAD1 = [7.2, 14.4, 21.7, 28.9, 43.3, 57.8, 65, 72.2, 86.7, 99.2, 14.42, 28.92, 43.32]

MCS_TO_RANGE_RAD2 = {
    "20" : [8.46, 7.31, 6.88, 5.36, 4.11, 2.84, 2.47, 2.14, 1.48, 1.29, 6.93, 4.89],
    "40" : [6.18, 5.18, 5.05, 4.29, 3.27, 2.35, 2.04, 1.76, 1.23, 1.01, 5.04, 3.73],
    "80" : [4.51, 3.76, 3.66, 3.18, 3.29, 1.75, 1.53, 1.29, 0.93, 0.78, 3.63, 2.72],
    "160" : [3.29, 2.74, 2.67, 2.32, 1.8, 1.28, 1.12, 0,94, 0.68, 0.57, 2.65, 1.99],
}
MCS_TO_RATE_RAD2 = {
    "20": [7.2, 14.4, 21.7, 28.9, 43.3, 57.8, 65.0, 72.2, 86.7, 99.2, 14.42, 28.92],
    "40": [15, 30, 45, 60, 90, 120, 135, 150, 180, 200, 30.2, 60.2],
    "80": [32.5, 65, 97.5, 130, 195, 260, 292.5, 325, 390, 433.3, 65.2, 135],
    "160": [65, 130, 195, 260, 390, 520, 585, 650, 780, 866.7, 130.2, 260.2]
}

COUNTRY = {
    "US": {
        "2.4ghz" : {
            "bfbo" : 1,
            "2.4ghzin": {
                "eirp" : 36,        
                "txp" : 30,
            },
            "2.4ghzout": {
                "eirp" : 36,        
                "txp" : 30,
            },
        },
        "5ghz" : {
            "bfbo" : 1,
            "unii1" : {
                "eirp" : 36,
                "txp" : 30,
            }
        }
    },    
}