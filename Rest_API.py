import os.path
import json
from flask import Flask,request
from flask_restx import Api, Resource
from face_parsing.face_parser import Parser
from flask import abort
import base64
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv

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
                return body
        except FileNotFoundError:
            abort(400,f"{Item} is not found")

if __name__ == '__main__':
    load_dotenv()
    PORT = os.getenv('PORT')
    parser = Parser(os.path.join("best_model", "examplemodel.pth"))
    app.run(host='0.0.0.0', port=PORT)

