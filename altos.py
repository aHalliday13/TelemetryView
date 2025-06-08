"""
AltOS telemetry packet decoder. Primarily supports the TeleMetrum.
Based on specification at https://altusmetrum.org/AltOS/doc/telemetry.html
"""

import warnings

def segment_packet(packet : bytes):
    ret_p = {
        "preamble": {
            "serial": int.from_bytes(packet[0:2]),
            "tick": int.from_bytes(packet[2:4]),
            "type": int(packet[4])
        }
    }

    if ret_p["preamble"]["type"] not in [0x0A, 0x0B, 0x04]:
        warnings.warn("Unsupported packet type. Returning early with missing data!")
        return ret_p
    
    if ret_p["preamble"]["type"] == 0x0A:   # Sensor
        ret_p["sensor"] = {
            "state": int(packet[5]),
            "accel": int.from_bytes(packet[6:8]),
            "pres": int.from_bytes(packet[8:12]),
            "temp": int.from_bytes(packet[12:14]),
            "acceleration": int.from_bytes(packet[14:16]),
            "speed": int.from_bytes(packet[16:18]),
            "height": int.from_bytes(packet[18:20]),
            "v_batt": int.from_bytes(packet[20:22]),
            "sense_d": int.from_bytes(packet[22:24]),
            "sense_m": int.from_bytes(packet[24:26])
        }
    elif ret_p["preamble"]["type"] == 0x0B: # Calibration
        ret_p["calibration"] = {
            "ground_pres": int.from_bytes(packet[8:12]),
            "ground_accel": int.from_bytes(packet[12:14]),
            "accel_plus_g": int.from_bytes(packet[14:16]),
            "accel_minus_g": int.from_bytes(packet[16:18])            
        }
    elif ret_p["preamble"]["type"] == 0x04: # Configuration
        ret_p["config"] = {
            "type": int(packet[5]),
            "number": int.from_bytes(packet[6:8]),
            "config_major": int.from_bytes(packet[8]),
            "config_minor": int.from_bytes(packet[9]),
            "apogee_delay": int.from_bytes(packet[10:12]),
            "main_deploy": int.from_bytes(packet[12:14]),
            "flight_log_max": int.from_bytes(packet[14:16]),
            "callsign": packet[16:24].decode(),
            "version": packet[24:32].decode()
        }

    return ret_p

def parse_serial_line(line : str):
    if line[0:5] != "TELEM":
        raise NotImplementedError("Bad Telemetry")

    data = line[6:]
    data = bytes.fromhex(data)
    
    length = int(data[0])
    packet = data[1:length-1]
    rssi = int(data[length-1])
    lqi = int(data[length])
    checksum = int(data[length+1])

    packet = segment_packet(packet)

    return packet
