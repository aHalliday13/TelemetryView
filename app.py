"""
Flask web server to render telemetry overlay.
"""

from flask import Flask, render_template
import serial
import altos
import threading
from datetime import timedelta

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("overlay.html")

@app.route("/telemonly")
def telemonly():
    return render_template("telemetry_only.html")

@app.route("/data/<key>")
def data(key):
    t = fetch_telemetry()[key]
    return str(t)

def fetch_telemetry():
    global live_packet

    try:
        tick = live_packet["preamble"]["tick"]
        tick = timedelta(seconds=tick//100)
        t = {
            "speed":live_packet["sensor"]["speed"],
            "agl":live_packet["sensor"]["height"],
            "time": tick
        }
    except Exception as e:
        print(e)
        t = {
            "speed":"ERROR",
            "agl":"ERROR",
            "time":"ERROR"
        }
    return t

class Listener(threading.Thread):
    def run(self):
        global live_packet
        global tty
        with serial.Serial(tty, timeout=1) as ser:
            while True:
                try:
                    telem = ser.readline()
                    telem = telem.decode().strip().upper()
                    packet = altos.parse_serial_line(telem)
                    if packet["preamble"]["type"] == 0x0A:
                        live_packet = packet
                except Exception:
                    pass

if __name__ == "__main__":
    tty = input("Please specify TTY: ")
    if tty != "":
        print("Telemetry Listener Starting")
        listen_thread = Listener()
        listen_thread.start()
    app.run(debug=True)