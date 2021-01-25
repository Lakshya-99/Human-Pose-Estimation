# -*- coding: utf-8 -*-
"""Explo

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZdDkGxbpqIuRUMKkwk72qeqruoe83tKH

For more information about working with Colaboratory notebooks, see [Overview of Colaboratory](/notebooks/basic_features_overview.ipynb).
"""

import scipy.io
import glob
import cv2
import numpy as np
from google.colab import drive

import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from keras import applications
from keras import optimizers
from keras.models import Sequential, Model
from keras.layers import Dropout, Flatten, Dense, BatchNormalization, Activation, Flatten
from keras.layers.merge import Concatenate
from keras import backend as k
from keras.callbacks import EarlyStopping

import tensorflow as tf

drive.mount('/content/gdrive', force_remount = True)



mat = scipy.io.loadmat('/content/gdrive/My Drive/joints.mat')
data = mat['joints'] #Add the meaning here
print(data.shape)

def get_joint(column_index):
    y = np.zeros((2000, 2))
    for i in range(2):
        for j in range(2000):
            y[j, i] = data[i, column_index, j]
    return y

def get_images(n_images):
    imgs = []
    for i in range(n_images):
        path = '/content/gdrive/My Drive/images/im' + str('000' + str(i+1))[-4:] + '.jpg'
        img = np.array(cv2.imread(path, 1))
        imgs.append(img)
    return np.array(imgs)

def resize_images(imgs, y):
    images = []
    for i, img in enumerate(imgs[:2000]):
        y[i][0] = (y[i][0]/img.shape[1])*150
        y[i][1] = (y[i][1]/img.shape[0])*150
        resized = cv2.resize(img, (150, 150), interpolation = cv2.INTER_AREA)
        images.append(resized)
    labels = y
    return np.array(images), labels
  
def resize_images2(imgs, y):
    images = []
    for i, img in enumerate(imgs[:2000]):
        y[i][0] = (y[i][0]/img.shape[1])*75
        y[i][1] = (y[i][1]/img.shape[0])*75
        resized = cv2.resize(img, (75, 75), interpolation = cv2.INTER_AREA)
        images.append(resized)
    labels = y
    return np.array(images), labels
        
def draw_joint(image, label):
    fig,ax = plt.subplots(1)
    ax.set_aspect('equal')
    circ = Circle((label[0], label[1]), 5)
    ax.add_patch(circ)
    ax.imshow(image)
    plt.show()

def flip_horizontal(image, label):
    img2 = np.flip(image, 1)
    return img2, [150-label[0]-1, label[1]]

def flip_vertical(image, label):
    img2 = np.flip(image, 0)
    return img2, [label[0], 150-label[1]-1]

def data_augment(images, labels):
    images_new = []
    labels_new = []
    for i in range(2000):
        images_new.append(images[i])
        labels_new.append(labels[i])
    for i in range(2000):
        im, l = flip_horizontal(images[i], labels[i])
        images_new.append(im)
        labels_new.append(l)
    for i in range(2000):
        im, l = flip_vertical(images[i], labels[i])
        images_new.append(im)
        labels_new.append(l)
    for i in range(2000):
        im, l = flip_horizontal(images[i], labels[i])
        im, l = flip_vertical(im, l)
        images_new.append(im)
        labels_new.append(l)
        
    return np.array(images_new), np.array(labels_new)





from keras import Model
import keras
def network():
    
    model1=keras.applications.inception_v3.InceptionV3(include_top = False,
                                                input_shape=(150,150,3))
                                       
                                       

    for layer in model1.layers:
        layer.trainable = False
    

    for layer in model1.layers[-5:]:
        layer.trainable = True
        
    x = model1.output
    x = Flatten()(x)
    
    x = Dense(1024)(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    
    predictions = Dense(16, activation="linear")(x)

    model_final = Model(input = model1.input, output = predictions)
    
    return model_final

m = network()
m.summary()



models = []
for i in range(0, 14):
    y = get_joint(i)
    imgs = get_images(2000)
    images, labels = resize_images(imgs, y)
    images_new, labels_new = data_augment(images, labels)
    #images2, labels2 = resize_images2(imgs, y)
    #images_new2, labels_new2 = data_augment(images2, labels2)
    
    model = network()
    
    model = Model(inputs = , outputs = pred)
    model.summary()
    model.compile(
    loss = "mse",
    optimizer = optimizers.Adam(lr=0.1, beta_1=0.9, beta_2=0.999, epsilon=None),
    metrics = ["accuracy"])
    
    model.fit(x=[images_new, images_new2], y=labels_new, 
        batch_size=16, epochs=25, verbose=1, validation_split=0)
    
    model_json = model_final.to_json()
    with open("model_" + str(i) + ".json", "w") as json_file:
        json_file.write(model_json)
    model_final.save_weights("model_" + str(i) + ".h5")
    print("Saved model to disk")

    model_yaml = model_final.to_yaml()
    with open("model_" + str(i) + ".yaml", "w") as yaml_file:
        yaml_file.write(model_yaml)
    model_final.save_weights("model_" + str(i) + ".h5")
    print("Saved model to disk")
    
    models.append(model_final)



