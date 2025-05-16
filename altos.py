"""
AltOS telemetry packet decoder. Primarily supports the TeleMetrum.
Based on specification at https://altusmetrum.org/AltOS/doc/telemetry.html
"""

import warnings

def segment_packet(packet : bytes):
    ret_p = {
        "preamble": {
            "serial": int(packet[0:2]),
            "tick": int(packet[2:4]),
            "type": int(packet[4])
        }
    }

    if ret_p["preamble"]["type"] not in [0x0A, 0x0B, 0x04]:
        warnings.warn("Unsupported packet type. Returning early with missing data!")
        return ret_p
    
    if ret_p["preamble"]["type"] == 0x0A:   # Sensor
        ret_p["sensor"] = {
            "state": int(packet[5]),
            "accel": int(packet[6:8]),
            "pres": int(packet[8:12]),
            "temp": int(packet[12:14]),
            "acceleration": int(packet[14:16]),
            "speed": int(packet[16:18]),
            "height": int(packet[18:20]),
            "v_batt": int(packet[20:22]),
            "sense_d": int(packet[22:24]),
            "sense_m": int(packet[24:26])
        }
    elif ret_p["preamble"]["type"] == 0x0B: # Calibration
        ret_p["calibration"] = {
            "ground_pres": int(packet[8:12]),
            "ground_accel": int(packet[12:14]),
            "accel_plus_g": int(packet[14:16]),
            "accel_minus_g": int(packet[16:18])            
        }
    elif ret_p["preamble"]["type"] == 0x04: # Configuration
        ret_p["config"] = {
            "type": int(packet[5]),
            "number": int(packet[6:8]),
            "config_major": int(packet[8]),
            "config_minor": int(packet[9]),
            "apogee_delay": int(packet[10:12]),
            "main_deploy": int(packet[12:14]),
            "flight_log_max": int(packet[14:16]),
            "callsign": packet[16:24].decode(),
            "version": packet[24:32].decode()
        }

def parse_serial_line(line : str):
    if line[0:5] != "TELEM":
        raise ValueError("Not valid telemetry")

    data = line[6:]
    data = bytes.fromhex(data)
    
    length = int(data[0])
    packet = data[1:length-1]
    rssi = int(data[length-1])
    lqi = int(data[length])
    checksum = int(data[length+1])

    return packet