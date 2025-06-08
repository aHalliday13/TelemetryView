from flask import Flask, render_template
import serial
import altos
import threading
from pyvirtualserial import VirtualSerial

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("overlay.html")

@app.route("/data/<key>")
def data(key):
    t = fetch_telemetry()[key]
    return str(t)

def fetch_telemetry():
    global live_packet

    try:
        t = {
            "speed":live_packet["sensor"]["speed"],
            "agl":live_packet["sensor"]["height"],
            "time":live_packet["preamble"]["tick"]
        }
    except:
        t = {
            "speed":"BADDATA",
            "agl":"BADDATA",
            "time":"BADDATA"
        }
    return t

class Listener(threading.Thread):
    def run(self):
        global live_packet
        global tty
        global virtual_dongle
        with serial.Serial(tty, timeout=1) as ser:
            while True:
                try:
                    telem = ser.readline()
                    virtual_dongle.write(telem)
                    telem = telem.decode().strip().upper()
                    packet = altos.parse_serial_line(telem)
                    if packet["preamble"]["type"] == 0x0A:
                        live_packet = packet
                except Exception:
                    pass

if __name__ == "__main__":
    tty = input("Please specify TTY: ")
    print("Telemetry Listener Starting")
    virtual_dongle = VirtualSerial()
    print(f"Virtual serial port available on {virtual_dongle.get_slave_name()}")
    listen_thread = Listener()
    listen_thread.start()
    app.run()