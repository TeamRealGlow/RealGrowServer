import os.path

from flask import Flask,request
from flask_restx import Api, Resource
import dotenv
from face_parsing.face_parser import Parser
from PIL import Image
import numpy as np
app = Flask(__name__)
api = Api(app)

@api.route('/parsing')
class HelloWorld(Resource):
    def post(self):
        image_file = request.files['img']
        image_path = os.path.join("static","pic", image_file.filename)
        image_file.save(image_path)
        parsing = parser.out_parsing(image_path)
        parsingimage = Image.fromarray((parsing * 255).astype(np.uint8))
        parsingimage_path = os.path.join("static", "grayScale",os.path.splitext(os.path.basename(image_path))[0] + ".jpg")
        parsingimage.save(parsingimage_path)
        return {"image_path": parsingimage_path}

if __name__ == '__main__':
    parser = Parser(os.path.join("best_model", "examplemodel.pth"))
    app.run(host='0.0.0.0', port=8000, debug = True)

