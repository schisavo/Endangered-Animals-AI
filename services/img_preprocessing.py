import numpy as np

def preprocess_image(image):
    img = image.resize((128,128))
    img_array = np.array(img) / 255.0

    if img_array.shape[-1] != 3:
        img_array = np.stack((img_array,)*3, axis=-1)

    return np.expand_dims(img_array, axis=0)
