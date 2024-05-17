import os.path

from flask import Flask,request
from flask_restx import Api, Resource
from face_parsing.face_parser import Parser

import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)
api = Api(app)

@api.route('/parsing')
class HelloWorld(Resource):
    def post(self):
        json_data = request.get_json()
        img = json_data['img']
        img = base64.b64decode(img)
        img = Image.open(BytesIO(img))
        parsing = parser.out_parsing(img)
        b64_string = base64.b64encode(parsing).decode('utf-8')
        return {"PNGImage": b64_string}

if __name__ == '__main__':
    # debug를 True로 세팅하면, 해당 서버 세팅 후에 코드가 바뀌어도 문제없이 실행됨.
    parser = Parser(os.path.join("best_model", "examplemodel.pth"))
    app.run(host='0.0.0.0', port=8000, debug = True)

