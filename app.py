from flask import Flask,render_template, request
from flask_bootstrap import Bootstrap
import aiohttp
import asyncio
import requests
import os
from PIL import Image
app = Flask(__name__)
Bootstrap(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def file_upload():
    image_file = request.files['file']
    data ={
        'img': (image_file.filename, image_file.stream, image_file.content_type),
    }
    url = "http://192.168.24.185:8000/parsing"
    response = requests.post(url, files=data)
    response = response.json()
    reslute = response["image_path"]
    return render_template("reasult.html",img = reslute)

if __name__ =="__main__":
    app.run(host='0.0.0.0', port=8081, debug = True)

