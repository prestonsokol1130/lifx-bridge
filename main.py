from flask import Flask, request, jsonify
import os, requests

app = Flask(__name__)
TOKEN = os.environ["LIFX_TOKEN"]

@app.post("/")
def lifx():
    data = request.get_json(force=True)
    for cmd in data:
        sel, hsbk = cmd["selector"], cmd["hsbk"]
        color = f"hue:{hsbk['h']} saturation:{hsbk['s']} brightness:{hsbk['b']} kelvin:{hsbk['k']}"
        url = f"https://api.lifx.com/v1/lights/{sel}/state"
        hdr = {"Authorization": f"Bearer {TOKEN}"}
        rsp = requests.put(url, json={"color": color, "duration": 2}, headers=hdr)
        if rsp.status_code != 207: return rsp.text, rsp.status_code
    return jsonify(ok=True)
