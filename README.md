### RealGrowBackServer

# API 명세서

| 기능        | endpoint  | 메서드 | 요청값(request body)                   | 반환값(response body)                                |
|-------------|-----------|--------|----------------------------------------|-----------------------------------------------------|
| 사진업로드 | /parsing  | POST   | {"img": "base64EncodingImg"}          | {"PNGImage": "face_parsingPNGIMG(GrayScale)_base64EncodingImg"} |



# API Specification
| Feature       | Endpoint  | Method | Request Body                        | Response Body                                         |
|---------------|-----------|--------|-------------------------------------|--------------------------------------------------------|
| Upload Photo  | /parsing  | POST   | {"img": "base64EncodingImg"}       | {"PNGImage": "face_parsingPNGIMG(GrayScale)_base64EncodingImg"} |

# Based Model
https://github.com/TeamRealGlow/face_parsing_model

# our pretrain_model
https://drive.google.com/file/d/16QtviOUcka3A8CMzsqIeLWhHAO5en1yT/view?usp=sharing

# Class Map
    0.background
    1.hair
    2.brow
    3.eye
    4.lip
    5.mouth
    6.nose
    7.skin
    8.ear