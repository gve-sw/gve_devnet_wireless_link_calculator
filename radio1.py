import math
import json
from scipy import constants

from raw import *

TX_CHANNEL = "2.4ghz"
TX_RAD1_BW_CHOICE = 20
TX_RAD1_BW = 20

TX_RAD1_CABLE = get_setting('txcable')
TX_RAD1_ANTENNA = get_setting('txantenna')
TX_BEAMFORMING = '4x4:3(BF20-10)'
TX_OTHER_TXP_DBM = -1
TX_PL_NAME = "PL2"
TX_RAD1_LINK_MARGIN = 7.8 # Needs to be looked up
TX_RAD1_OTHER_CABLE_LOSS = -1
TX_RAD1_OTHER_ANTENNA_GAIN = -1

RX_RAD1_ANTENNA = get_setting('rxantenna')
RX_RAD1_CABLE = get_setting('rxcable')
RX_RAD1_OTHER_CABLE_LOSS = -1
RX_RAD1_OTHER_ANTENNA_GAIN = -1

TX_DEVICE = get_tx_device()
RX_DEVICE = get_rx_device()
TX_DEVICE = get_tx_device()
RX_DEVICE = get_rx_device()
SNR = get_snr()
CABLE_LOSS = get_cable_loss()
ANTENNA_GAIN = get_antenna_gain()

def eirp_site1_rad1():
    TX_PL_DBM = TX_OTHER_TXP_DBM
    if TX_OTHER_TXP_DBM == -1:
        TX_PL_DBM = TX_DEVICE[TX_CHANNEL]["PL"][TX_PL_NAME]

    TXP_DBM = min(
        [
            TX_PL_DBM,
            get_txp_limit_site1()
        ]
    )

    return TXP_DBM - get_cable_loss_tx_rad1() + get_antenna_gain_tx_rad1()

def get_rx_sensitivity_site2_rad1():
    rad1_ktb = -(-174 + 10*math.log10(TX_RAD1_BW*1000000))

    return -(rad1_ktb - RX_DEVICE[TX_CHANNEL]['noise-figure'] - get_rx_rad1_snr())

def get_max_path_loss_rad1():
    return eirp_site1_rad1() + get_antenna_gain_rx_rad1() - get_cable_loss_rx_rad1() - get_rx_sensitivity_site2_rad1()

def get_max_mcs():
    return min(
        TX_DEVICE[TX_CHANNEL]['mcs-limit'] * TX_DEVICE[TX_CHANNEL]['spatial-streams'],
        RX_DEVICE[TX_CHANNEL]['mcs-limit'] * RX_DEVICE[TX_CHANNEL]['spatial-streams'],
        get_mcs_selection(),
        get_max_mcs_range()
    )

def get_rx_rad1_snr():
    max_mcs = get_max_mcs()

    if max_mcs != 0:
        return SNR[TX_BEAMFORMING][max_mcs-1]
    else:
        return 0

def get_tx_rad1_ss_in_mcs():
    return int((get_max_mcs()-1)/10) + 1

def get_txp_limit_site1():
    if get_tx_rad1_ss_in_mcs() != 0:
        if TX_DEVICE[TX_CHANNEL]['beamforming'] > 0 and COUNTRY[get_setting('domain')][TX_CHANNEL]['bfbo'] > 0:
            return COUNTRY[get_setting('domain')][TX_CHANNEL][get_setting('channel')]['txp'] - 10.0*math.log10(TX_DEVICE[TX_CHANNEL]['beamforming']/get_tx_rad1_ss_in_mcs())
        else:
            return TX_DEVICE[TX_CHANNEL]('txp')
    else:
        return 0

def get_max_mcs_range():
    if get_setting('desiredrange') > 0:
        min_diff = 1000
        max_range = 0
        max_range_i = 0
        current_i = 0
        for i in range(len(MCS_TO_RANGE_RAD1)):
            if MCS_TO_RANGE_RAD1[i] > max_range:
                max_range = MCS_TO_RANGE_RAD1[i]
                max_range_i = i

            diff = MCS_TO_RANGE_RAD1[i] - get_setting('desiredrange')
            if diff > 0 and diff < min_diff:
                min_diff = diff
                current_i = i
        if min_diff == 1000:
            return max_range_i
        return current_i
    else:
        return 1000

def get_mcs_selection():
    return get_mcs_for_rate(get_setting('desiredrate'))

def get_mcs_for_rate(rate):
    if rate > 0:
        min_diff = 1000
        current_i = 0
        for i in range(len(MCS_TO_RATE_RAD1)):
            diff = abs(rate - MCS_TO_RATE_RAD1[i])
            if diff >= 0 and diff < min_diff:
                min_diff = diff
                current_i = i
        return current_i+1
    else:
        return 1000

def get_cable_loss_tx_rad1():
    if TX_RAD1_OTHER_CABLE_LOSS == -1:
        return CABLE_LOSS[TX_CHANNEL][TX_RAD1_CABLE]
    else:
        return TX_RAD1_OTHER_CABLE_LOSS

def get_cable_loss_rx_rad1():
    if RX_RAD1_OTHER_CABLE_LOSS == -1:
        return CABLE_LOSS[TX_CHANNEL][RX_RAD1_CABLE]
    else:
        return RX_RAD1_OTHER_CABLE_LOSS

def get_antenna_gain_tx_rad1():
    if TX_RAD1_OTHER_ANTENNA_GAIN == -1:
        if TX_RAD1_ANTENNA == 'buitin':
            return TX_DEVICE[TX_CHANNEL]['builtin-antenna']
        else:
            return ANTENNA_GAIN["2.4ghz"][TX_RAD1_ANTENNA]
    else:
        return TX_RAD1_OTHER_ANTENNA_GAIN

def get_antenna_gain_rx_rad1():
    if RX_RAD1_OTHER_ANTENNA_GAIN == -1:
        if RX_RAD1_ANTENNA == 'buitin':
            return RX_DEVICE[TX_CHANNEL]['builtin-antenna']
        else:
            return ANTENNA_GAIN["2.4ghz"][RX_RAD1_ANTENNA]
    else:
        return RX_RAD1_OTHER_ANTENNA_GAIN

def get_tx_rad1_los():
    return (0.3/2.4)/(4*math.pi*math.pow(10**(-get_max_path_loss_rad1()/10), 1/2.2))

def get_tx_rad1_rssi():
    return eirp_site1_rad1() + get_antenna_gain_rx_rad1() + get_cable_loss_rx_rad1() - get_path_loss_rad1()

def get_path_loss_rad1():
    wavelength = constants.speed_of_light/(2.4*10**9)
    return 30 + 20*math.log( (4*math.pi*MCS_TO_RANGE_RAD1[get_max_mcs()-1]) / wavelength , 10 )

def get_outdoor_range_urban_rad1():
    freq = 33.9*math.log10(1000*2.4)
    tx_height_factor = 13.82 * (math.log10(max(
        get_setting('height1'), get_setting('height2')
    )))
    a_factor = 3.2 * math.pow(math.log10(11.75*min(
        get_setting('height1'), get_setting('height2')
    )), 2) - 4.97
    cm_term = 3
    return 1000 * math.pow(10, ((get_max_path_loss_rad1() - TX_RAD1_LINK_MARGIN - 46.3 - freq + tx_height_factor + a_factor - cm_term) / (
        44.9 - 6.55*math.log10(max(
            get_setting('height1'), get_setting('height2')
        ))
    )))

def get_outdoor_range_suburban_rad1():
    freq = 33.9*math.log10(1000*2.4)
    tx_height_factor = 13.82 * (math.log10(max(
        get_setting('height1'), get_setting('height2')
    )))
    a_factor = (1.1*math.log10(1000*2.4) - 0.7)*min(
        get_setting('height1'), get_setting('height2')
    ) - (1.56*math.log10(1000*2.4) - 0.8)
    cm_term = 0
    return 1000 * math.pow(10, ((get_max_path_loss_rad1() - TX_RAD1_LINK_MARGIN - 46.3 - freq + tx_height_factor + a_factor - cm_term) / (
        44.9 - 6.55*math.log10(max(
            get_setting('height1'), get_setting('height2')
        ))
    )))

def get_value(name, value, unit, alerts=[]):
    return {
        "metric" : name,
        "value" : value,
        "unit" : unit,
        "alerts" : alerts
    }

def get_metrics(settings):
    with open('settings.json', 'w') as f:
        json.dump(settings, f)
    
    # BEGIN Warnings #
    eirp_warning = []
    if eirp_site1_rad1() > COUNTRY[get_setting('domain')][TX_CHANNEL][get_setting('channel')]['eirp']:
        eirp_warning = ["Max EIRP Exceeded"]
    
    range_warning = []
    if MCS_TO_RANGE_RAD1[get_max_mcs()-1] < get_setting('desiredrange'):
        range_warning = ["Desired range not obtained"]
    
    rate_warning = []
    if MCS_TO_RATE_RAD1[get_max_mcs()-1] < get_setting('desiredrate'):
        rate_warning = ["Desired rate not obtained"]
    # END Warnings #

    return [
        get_value("Actual range", MCS_TO_RANGE_RAD1[get_max_mcs()-1]*1.609, "km", range_warning),
        get_value("Actual data rate", MCS_TO_RATE_RAD1[get_max_mcs()-1], "Mbps", rate_warning),
        get_value("MCS", get_max_mcs(), ""),
        get_value("EIRP", eirp_site1_rad1(), "Dbm", eirp_warning),
        get_value("Pathloss", get_path_loss_rad1(), "Dbm"),
        get_value("Max Pathloss", get_max_path_loss_rad1(), "Dbm"),
        get_value("RX Sensitivity", get_rx_sensitivity_site2_rad1(), "Dbm"),
        get_value("RSSI", get_tx_rad1_rssi(), "Dbm"),
        get_value("Line of Sight", get_tx_rad1_los(), "meter"),
        get_value("Outdoor distance (suburban)", get_outdoor_range_suburban_rad1(), "meter"),
        get_value("Outdoor distance (urban)", get_outdoor_range_urban_rad1(), "meter"),
    ]