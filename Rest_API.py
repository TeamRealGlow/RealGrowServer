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
import numpy as np

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
            bytes_io = BytesIO()
            parsing.save(bytes_io,format="PNG")
            b64_string = base64.b64encode(bytes_io.getvalue()).decode('utf-8')
            # tempparsing = base64.b64decode(b64_string)
            # tempimg = BytesIO(tempparsing)
            # tempimg = Image.open(tempimg)
            # tempnp = np.array(tempimg)
            # print(tempnp.max())
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
    import requests
    img = requests.get("https://t1.gstatic.com/licensed-image?q=tbn:ANd9GcTmi89YSignGumXvvD2zPRevLiB_GUHG18_76BuugGHkM85DDNZn1rWlx9uKr2w3dUH")
    PORT = os.getenv('PORT')
    parser = Parser(os.path.join("best_model", "examplemodel.pth"))
    app.run(host='0.0.0.0', port=PORT,debug=True)

