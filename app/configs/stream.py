import cv2
import zmq
import base64
import numpy as np
import os

def streamer(host):
    context = zmq.Context()
    footage_socket = context.socket(zmq.SUB)
    isZMQSuccess = False

    # Mendapatkan path absolut ke gambar "noimage.png"
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Direktori file ini
    no_image_path = os.path.join(base_dir, "noimage.png")

    noImage = cv2.imread(no_image_path)
    if noImage is None:
        raise FileNotFoundError(f"File noimage.png tidak ditemukan di {no_image_path}")

    noImage = cv2.imencode('.jpg', noImage)[1].tobytes()

    try:
        footage_socket.connect(host)
        footage_socket.setsockopt_string(zmq.SUBSCRIBE, '')
        isZMQSuccess = True
    except Exception as e:
        print(f"ZMQ Connection Error: {e}")
        isZMQSuccess = False

    if isZMQSuccess:
        while True:
            frame = footage_socket.recv_string()
            if len(frame) == 0:
                return noImage
            img = base64.b64decode(frame)
            npimg = np.frombuffer(img, dtype=np.uint8)
            source = cv2.imdecode(npimg, 1)
            return cv2.imencode('.jpg', source)[1].tobytes()
    
    while True:
        return noImage
