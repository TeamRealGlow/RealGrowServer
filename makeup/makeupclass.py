import cv2
import requests
import base64
from io import BytesIO
import numpy as np
from PIL import Image

class FaceFeature():
    def __init__(self):
        self.features = {
            "skin":None,
            "eye":None,
            "brow":None,
            "lip":None,
            "mouth":None,
            "nose":None,
            "hair":None,
            "ear":None
        }

    def setFeature(self,parsing):
        cv_parsing = cv2.imdecode(parsing,cv2.IMREAD_GRAYSCALE)
        self.features["skin"] = (cv_parsing == 7).astype(np.uint8) * 255
        self.features["lip"] = (cv_parsing == 4).astype(np.uint8) * 255
        self.features["hair"] = (cv_parsing == 1).astype(np.uint8) * 255
        self.features["nose"] = (cv_parsing == 6).astype(np.uint8) * 255


    def getFeature(self,feature):
        return self.features[feature]
class MakeUpEngine():
    def __init__(self):
        self.__org_img = None
        self.__face_feature = FaceFeature()
        self.change_img_data = {
            "hair":None,
            "skin":None,
            "lip":None,
        }

    @property
    def org_img(self):
        return self.__org_img

    @org_img.setter
    def org_img(self,img):
        try:
            if isinstance(img, np.ndarray):
                self.__org_img = img
            elif isinstance(img, Image.Image):
                img = np.array(img)
                self.__org_img  =img
            else:
                raise Exception("plses input PIL Image.Image Type or np.ndarry type")
        except Exception as e:
            print(e)

    def faceParsing(self,ip):
        img_byte = BytesIO()
        img = Image.fromarray(self.__org_img)
        img.save(img_byte,format="PNG")
        b64_string = base64.b64encode(img_byte.getvalue()).decode('utf-8')
        files = {
            "img":b64_string
        }
        r = requests.post(f"{ip}/parsing", json=files)
        try:
            if r.status_code == 200 or 201:
                parsing_img = r.json()["PNGImage"]
                img = base64.b64decode(parsing_img)
                img_byte = BytesIO(img)
                self.__face_feature.setFeature(np.frombuffer(img_byte.getvalue(), np.uint8))
            else:
                raise Exception("APILoadError")
        except Exception as e:
            print(e)
    def faceParsing_img(self,base64_str):
        img = base64.b64decode(base64_str)
        img_byte = BytesIO(img)
        self.__face_feature.setFeature(np.frombuffer(img_byte.getvalue(), np.uint8))
    def makeup_skin(self,color:tuple):
        '''
        change_img_data["skin"] input imgdata
        :param color:
        Input RGB tuple
        :return:
        None
        '''
        blackmask = np.add(self.__face_feature.features["skin"], self.__face_feature.features["nose"])
        makeup = cv2.cvtColor(blackmask,cv2.COLOR_GRAY2BGR)
        makeup[(makeup == 255).all(axis=-1)] = color
        self.change_img_data["skin"] = makeup
    def makeup_hair(self,color:tuple):
        '''
        input change_img_data["hair"] imgdata
        :param color:
        Input RGB tuple
        :return:
        None
        '''
        blackmask = self.__face_feature.features["hair"]
        makeup = cv2.cvtColor(blackmask, cv2.COLOR_GRAY2BGR)
        makeup[(makeup == 255).all(axis=-1)] = color
        self.change_img_data["hair"] = makeup

    def makeup_lip(self,color):
        '''
        input change_img_data["lip"] imgdata
        :param color:
        Input RGB tuple
        :return:
        None
        '''
        blackmask = self.__face_feature.features["lip"]
        makeup = cv2.cvtColor(blackmask,cv2.COLOR_GRAY2BGR)
        makeup[(makeup == 255).all(axis=-1)] = color
        self.change_img_data["lip"] = makeup

    def alladdImg(self,*args):

        skin_alpha = 0.9 + 0.01 * args[1]
        hair_alpha = 0.85 + 0.01 * args[0]
        lip_alpha = 0.9 + 0.01 * args[2]

        skin_beta = 1-skin_alpha
        hair_beta = 1-hair_alpha
        lip_beta = 1-lip_alpha

        change_img = self.__org_img.copy()
        imgorg = self.__org_img.copy()
        if self.change_img_data["hair"] is not None:
            change_img = cv2.addWeighted(change_img, hair_alpha, self.change_img_data["hair"], hair_beta, 0.0)
            mask = cv2.bitwise_not(self.__face_feature.features["hair"])
            cropimg = cv2.bitwise_and(change_img, change_img , mask=self.__face_feature.features["hair"])
            body_maskless = cv2.bitwise_and(imgorg, imgorg, mask=mask)
            imgorg = cv2.add(body_maskless, cropimg)


        if self.change_img_data["skin"] is not None or self.change_img_data["skin"] is not None:
            change_img = cv2.addWeighted(imgorg, skin_alpha, self.change_img_data["skin"], skin_beta, 0.0)
            mask = cv2.bitwise_not(np.add(self.__face_feature.features["skin"],self.__face_feature.features["nose"]))
            cropimg = cv2.bitwise_and(change_img,change_img,mask = np.add(self.__face_feature.features["skin"],self.__face_feature.features["nose"]))
            body_maskless = cv2.bitwise_and(imgorg, imgorg, mask=mask)
            imgorg = cv2.add(body_maskless, cropimg)

        if self.change_img_data["lip"] is not None:
            change_img = cv2.addWeighted(imgorg, lip_alpha, self.change_img_data["lip"], lip_beta, 0.0)
            mask = cv2.bitwise_not(self.__face_feature.features["lip"])
            cropimg = cv2.bitwise_and(change_img,change_img,mask=cv2.bitwise_not(mask))
            body_maskless = cv2.bitwise_and(imgorg, imgorg, mask=mask)
            imgorg = cv2.add(body_maskless, cropimg)

        return imgorg





if __name__ == "__main__":
    make_up_engine = MakeUpEngine()
    imgorg = requests.get(
        "https://pds.joongang.co.kr/news/component/htmlphoto_mmdata/202306/04/138bdfca-3e86-4c09-9632-d22df52a0484.jpg")
    b64_string = base64.b64encode(imgorg.content).decode('utf-8')
    imgorg = imgorg.content
    imgorg = np.frombuffer(imgorg, np.uint8)
    imgorg = cv2.imdecode(imgorg, cv2.IMREAD_COLOR)
    make_up_engine.org_img = imgorg
    make_up_engine.faceParsing("http://192.168.24.190:5959")
    make_up_engine.makeup_skin((177, 206, 251))
    make_up_engine.makeup_hair((255, 0, 0))
    make_up_engine.makeup_lip((213, 12, 112))
    img = make_up_engine.alladdImg(5,8,3)
    cv2.imshow('pred', img)
    cv2.imshow('org',make_up_engine.org_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()