from flask import Blueprint, render_template, Response
from app.configs.stream import streamer
import json
import requests

zr = Blueprint('zeromq_routes', __name__)

def stream_1():
    # Hardcoded ZeroMQ sender URL
    zmq_url = "tcp://localhost:9101"  # Replace with your actual ZeroMQ sender URL

    while True:
        stream = streamer(zmq_url)
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + stream + b'\r\n\r\n')

@zr.route('/')
def index():
    return 'zero sayang'

@zr.route('/stream_1')
def live_camera():
    return Response(stream_1(), mimetype='multipart/x-mixed-replace; boundary=frame')