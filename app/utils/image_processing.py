import base64
# cargar imagenes
def get_base64_image(path):
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()


