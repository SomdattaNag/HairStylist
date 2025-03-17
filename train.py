import pandas as pd
import numpy as np
import cv2
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tqdm import tqdm
from sklearn.preprocessing import LabelEncoder
from label import hairtype
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator

df = pd.read_csv('hair_dataset.csv')
im_size = 224
images = []
labels = []

for i in tqdm(range(len(df))):
    img_path = df.iloc[i]['Image Path']
    label = df.iloc[i]['Label']
    img = cv2.imread(img_path)
    if img is None:
        continue
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  
    img = cv2.resize(img, (im_size, im_size))  
    img = img / 255.0 
    images.append(img)
    labels.append(label)

images = np.array(images)
labels = np.array(labels)

def plot(images, labels):
    plt.figure(figsize=(15, 10)) 
    for i in range(len(images)):
        plt.subplot(5, 5, i + 1)  
        plt.imshow(images[i])
        plt.title(labels[i])  
        plt.axis('off') 
    
    plt.show()  
plot(images[:25], labels[:25])

# Encodelabels
label_encode = LabelEncoder()
labels = label_encode.fit_transform(labels)
labels = to_categorical(labels)

xtrain, xtest, ytrain, ytest = train_test_split(images, labels, test_size=0.3, random_state=1, stratify=labels)

# DataAugmentation
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)
datagen.fit(xtrain)

# Transfer-Learning 
base_model = MobileNetV2(input_shape=(im_size, im_size, 3), include_top=False, weights='imagenet')
base_model.trainable = False  

model = tf.keras.Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dense(128, activation='relu'),
    Dropout(0.4),
    Dense(len(hairtype), activation='softmax')
])

model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])
history = model.fit(datagen.flow(xtrain, ytrain, batch_size=32), epochs=3, validation_data=(xtest, ytest))
testloss, testacc = model.evaluate(xtest, ytest)
print(f"test accuracy: {testacc:.4f}")
model.save("model.h5")

