import os.path
import json
from flask import Flask,request
from flask_restx import Api, Resource
from face_parsing.face_parser import Parser
from flask import abort
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)
api = Api(app)


@api.route('/parsing')
class Parsing(Resource):
    def post(self):
        try:
            json_data = request.get_json()
            img = json_data['img']
            img = base64.b64decode(img)
            img = Image.open(BytesIO(img))
            parsing = parser.out_parsing(img)
            byte_img = BytesIO()
            parsing.save(byte_img,format="PNG")
            parsing = byte_img.getvalue()
            b64_string = base64.b64encode(parsing).decode('utf-8')
            return {"PNGImage": b64_string}
        except Exception as e:
            print(e)
            abort(400,f"{e}")



@api.route("/loadItem/<string:Item>")
class LoadItem(Resource):
    def get(self,Item):
        rootpath =os.path.join("static","ItemDir")
        Jsonpath =os.path.join(rootpath,Item+".json")
        try:
            with open(Jsonpath,'r',encoding="utf-8") as file:
                json_data = json.load(file)
                body = {"Category": Item,"Itemlen": len(json_data["row"]),"row":json_data["row"]}
                print(body)
                return body
        except FileNotFoundError:
            abort(400,f"{Item} is not found")

if __name__ == '__main__':
    # debug를 True로 세팅하면, 해당 서버 세팅 후에 코드가 바뀌어도 문제없이 실행됨.
    parser = Parser(os.path.join("best_model", "examplemodel.pth"))
    app.run(host='0.0.0.0', port=8000, debug = True)

