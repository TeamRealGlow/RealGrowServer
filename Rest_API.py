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
import logging
import os

app = Flask(__name__)
api = Api(app)

def logStting():
    logging.getLogger('werkzeug').disabled = True
    # 4. 저장위치, 레벨, 포맷 세팅
    logging.basicConfig(filename="logs/server.log", level=logging.DEBUG
                        # , datefmt = '%Y/%m/%d %H:%M:%S %p'  # 년/월/일 시(12시간단위)/분/초 PM/AM
                        , datefmt='%Y/%m/%d %H:%M:%S'  # 년/월/일 시(24시간단위)/분/초
                        , format='%(asctime)s:%(levelname)s:%(message)s')


@api.route('/parsing')
class Parsing(Resource):
    def post(self):
        try:
            app.logger.info(f'[{request.method}] :: [{request.remote_addr}] :: {request.path}')
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
            app.logger.error(f'[{request.method}] :: [{request.remote_addr}] :: {e}')
            abort(400,f"{e}")



@api.route("/loadItem/<string:Item>")
class LoadItem(Resource):
    def get(self,Item):
        rootpath =os.path.join("static","ItemDir")
        Jsonpath =os.path.join(rootpath,Item+".json")
        try:
            app.logger.info(f'[{request.method}] {request.path}')
            with open(Jsonpath,'r',encoding="utf-8") as file:
                json_data = json.load(file)
                body = {"Category": Item,"Itemlen": len(json_data["row"]),"row":json_data["row"]}
                return body
        except FileNotFoundError:
            app.logger.error(f'[{request.method}] :: [{request.remote_addr}] :: {FileNotFoundError}')
            abort(400,f"{Item} is not found")

if __name__ == '__main__':
    if not os.path.isdir('logs'):
        os.mkdir('logs')
    load_dotenv()
    logStting()
    PORT = os.getenv('PORT')
    parser = Parser(os.path.join("best_model", "examplemodel.pth"))
    app.logger.info("server on :: PORT=" + str(PORT))
    app.run(host='0.0.0.0', port=PORT,debug=True)

