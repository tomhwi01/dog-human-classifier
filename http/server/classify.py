import numpy as np
import keras
from keras import applications
import time
from keras.utils import img_to_array, load_img
import time
from playsound import playsound
from datetime import timedelta, datetime
import os
import shutil

vgg16 = applications.VGG16(include_top=False, weights='imagenet')
model = keras.models.load_model('animal_class_model2.h5')

def read_image(file_path):
    image = load_img(file_path, target_size=(224, 224))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image /= 255.
    return image

def test_single_image(path, foldername):
    # animals = ['butterflies', 'chickens', 'elephants', 'horses', 'spiders', 'squirells']
    animals = ['dogs', 'humans']
    images = read_image(path)
    bt_prediction = vgg16.predict(images, verbose=0)
    preds = model.predict(bt_prediction, verbose=0)
    folder_path = os.path.join(directory, foldername, 'result')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    f = open(os.path.join(folder_path, 'text.txt'), 'w')
    for idx, animal, x in zip(range(0,6), animals , preds[0]):
        f.write("ID: {}, Label: {} {}%".format(idx, animal, round(x*100,2) ))
        f.write('\n')
    f.close()
    # class_predicted = preds.argmax(axis=-1)
    return

directory = 'uploads'

while True:
    for foldername in os.listdir(directory):
        f = os.path.join(directory, foldername)
        if os.path.isdir(f):
            if datetime.now() >= (datetime.strptime(foldername, '%Y-%m-%d %H%M%S.%f') + timedelta(minutes=10)):
                shutil.rmtree(f)
            else:
                for filename in os.listdir(os.path.join(directory, foldername)):
                    print('File is found')
                    f2 = os.path.join(directory, foldername, filename)
                    # checking if it is a file
                    if os.path.isfile(f2):
                        test_single_image(f2, foldername)
    print('Go to the next loop')
    time.sleep(1)
