def imgRequestTest():
    import numpy as np
    import requests
    import base64
    import cv2
    import os
    from PIL import Image
    import matplotlib.pyplot as plt
    from io import BytesIO

    image_name = os.path.join("ex","oh.png")
    with open(image_name, 'rb') as f:
        img_data = f.read()

    b64_string = base64.b64encode(img_data).decode('utf-8')

    files = {
                "img": b64_string,
            }

    r = requests.post("http://192.168.24.185:8000/parsing", json=files)

    print(r)
    img = r.json()["PNGImage"]
    img = base64.b64decode(img)
    img = BytesIO(img)
    img = Image.open(img)
    plt.imshow(img)
    plt.show()
    np_img = np.array(img)
    print(np_img.shape)

def ItemGetTest():
    import requests
    import base64
    import os
    r = requests.get("http://192.168.24.185:8000/loadItem/hairItem1")
    b = r.json()
    print(b)


if __name__ == "__main__":
    choice = 2
    if choice == 1:
        imgRequestTest()
    elif choice == 2:
        ItemGetTest()