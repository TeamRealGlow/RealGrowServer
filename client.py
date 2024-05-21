import os

from dotenv import load_dotenv

def imgRequestTest(HOST_SERVER):
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

    # r = requests.post(f"{HOST_SERVER}/parsing", json=files)
    r = requests.post(f"http://192.168.24.187:5000/parsing", json=files)
    print(r)
    img = r.json()["PNGImage"]
    img = base64.b64decode(img)
    img = BytesIO(img)
    img = Image.open(img)
    plt.imshow(img)
    plt.show()
    np_img = np.array(img)
    print(np_img.max())

def ItemGetTest(HOST_SERVER):
    import requests
    import base64
    import os
    r = requests.get(f"{HOST_SERVER}/loadItem/hairItem")
    b = r.json()
    print(b)


if __name__ == "__main__":
    load_dotenv()
    HOST_SERVER = os.getenv("HOST_SERVER")
    choice = 1
    if choice == 1:
        imgRequestTest(HOST_SERVER)
    elif choice == 2:
        ItemGetTest(HOST_SERVER)