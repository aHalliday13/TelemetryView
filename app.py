from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("overlay.html")

@app.route("/data/<key>")
def data(key):
    t = fetch_telemetry()[key]
    return str(t)

def fetch_telemetry():
    t = {
        "speed":9000,
        "agl":6969,
        "time":"01:23.45"
    }
    return t