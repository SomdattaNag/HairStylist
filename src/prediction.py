from tensorflow.keras.models import load_model
import cv2
import numpy as np
from src.label import hairtype

model = load_model("../models/model.h5")
im_size = 224  

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  
    img = cv2.resize(img, (im_size, im_size))  
    img = img / 255.0  
    img = np.expand_dims(img, axis=0)  
    return img

#prediction
def predict_hairtype(image_path):
    newimg = preprocess_image(image_path)
    prediction = model.predict(newimg)
    predictlabel = np.argmax(prediction)  
    return hairtype[predictlabel]

