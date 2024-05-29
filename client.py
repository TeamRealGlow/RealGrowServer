import os

from dotenv import load_dotenv

from threading import Thread


def imgRequestTest(HOST_SERVER = None):
    import numpy as np
    import requests
    import base64
    import os
    from PIL import Image
    import matplotlib.pyplot as plt
    from io import BytesIO

    img = requests.get("https://t1.gstatic.com/licensed-image?q=tbn:ANd9GcTmi89YSignGumXvvD2zPRevLiB_GUHG18_76BuugGHkM85DDNZn1rWlx9uKr2w3dUH")

    b64_string = base64.b64encode(img.content).decode('utf-8')

    files = {
                "img": b64_string,
            }

    r = requests.post(f"{HOST_SERVER}/parsing", json=files)
    # r = requests.post(f"http://192.168.24.187:5000/parsing", json=files)
    print(r)
    img = r.json()["PNGImage"]
    img = base64.b64decode(img)
    img = BytesIO(img)
    img = Image.open(img)
    plt.imshow(img)
    plt.show()
    np_img = np.array(img)
    print(np_img.max())

def imgRequestMulti():
    import numpy as np
    import requests
    import base64
    import os
    from PIL import Image
    import matplotlib.pyplot as plt
    from io import BytesIO

    img = requests.get("https://t1.gstatic.com/licensed-image?q=tbn:ANd9GcTmi89YSignGumXvvD2zPRevLiB_GUHG18_76BuugGHkM85DDNZn1rWlx9uKr2w3dUH")

    b64_string = base64.b64encode(img.content).decode('utf-8')

    files = {
                "img": b64_string,
            }

    r = requests.post(f"{HOST_SERVER}/parsing", json=files)
    # r = requests.post(f"http://192.168.24.190:5000/parsing", json=files)
    print(r)
    img = r.json()["PNGImage"]
    img = base64.b64decode(img)
    img = BytesIO(img)
    img = Image.open(img)
    # plt.imshow(img)
    # plt.show()
    np_img = np.array(img)
    print(np_img.max())

def ItemGetTest(HOST_SERVER):
    import requests
    import base64
    import os
    r = requests.get(f"{HOST_SERVER}/loadItem/hairItem1")
    b = r.json()
    print(b)

def PostImg():
    import requests
    import base64
    import matplotlib.pyplot as plt
    from io import BytesIO
    from PIL import Image
    img = requests.get(
        "https://pds.joongang.co.kr/news/component/htmlphoto_mmdata/202306/04/138bdfca-3e86-4c09-9632-d22df52a0484.jpg")
    b64_string = base64.b64encode(img.content).decode('utf-8')
    files = {
        "img": b64_string,
    }
    r = requests.post(f"{HOST_SERVER}/parsing", json=files)
    # r = requests.post(f"http://192.168.24.187:5000/parsing", json=files)
    print(r)
    parsingImg = r.json()["PNGImage"]

    postmake = {
        "img" : b64_string,
        "parsing" : parsingImg,
        "skin_color":[[177, 206, 251],0],
        "hair_color":[[255, 0, 0],0],
        "lip_color":[[213, 12, 112],0]
    }

    r = requests.post(f"{HOST_SERVER}/makeup",json=postmake)
    changeImg = r.json()["changeImg"]
    changeImg = base64.b64decode(changeImg)
    changeImg = BytesIO(changeImg)
    changeImg = Image.open(changeImg)
    plt.imshow(changeImg)
    plt.show()



if __name__ == "__main__":
    load_dotenv()
    HOST_SERVER = os.getenv("HOST_SERVER")
    commond = {"단일 이미지 전송":1,"아이템 불러오기":2, "멀티 이미지 전송":3}
    choice = 4
    if choice == 1:
        imgRequestTest(HOST_SERVER=HOST_SERVER)
    elif choice == 2:
        ItemGetTest(HOST_SERVER)
    elif choice == 3:
        workList = []
        for item in range(1000):
            workList.append(Thread(target=imgRequestMulti))
        for item in workList:
            item.start()
        for item in workList:
            item.join()
    elif choice == 4:
        PostImg()

