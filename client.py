import requests
import base64
import cv2
import os
from PIL import Image
import matplotlib.pyplot as plt
from io import BytesIO

image_name = os.path.join("ex","oh.png")
with open(image_name, 'rb') as f:
    img_data = f.read()

b64_string = base64.b64encode(img_data).decode('utf-8')

files = {
            "img": b64_string,
        }

r = requests.post("http://192.168.24.185:8000/parsing", json=files)
img = r.json()["PNGImage"]
img = base64.b64decode(img)
img = BytesIO(img)
plt.imshow(img)
plt.show()