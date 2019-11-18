import matplotlib
import numpy as np
import os
from PIL import Image,ImageOps
from keras.preprocessing.image import ImageDataGenerator
import operator
from keras.models import load_model
from keras.preprocessing import image
import base64
import ast
import sys


def recommand(predictions, class_dict):
    # Recommend top 3
    predictions = predictions[0].tolist()
    predict = []
    for i in range(len(predictions)):
        predict.insert(i, [i, predictions[i]])

    predict2 = sorted(predict, key=lambda x: x[1], reverse=True)

    re_str = ""
    for i in range(10):
        recommend = [name for name, target in class_dict.items() if target == predict2[i][0]]
        re_str = re_str + str(recommend)[2:len(recommend)-3]
        if i == 9:
            break
        re_str += ","
        # recommand_percent = predict2[i][1]
        # print(recommand, " ", round(recommand_percent, 3) * 100, "%")\
    return re_str


# base64.txt -> image -> save folder
remove_str = 'data:image/png;base64,'

image_path = '/home/student/2019_Capstone-design/node/image_predict/predict_image/12/out.png'
g = open(image_path, 'wb')
g.write(base64.b64decode(sys.argv[1][len(remove_str):]))
g.close()


model1 = load_model('/home/student/2019_Capstone-design/node/image_predict/v2.01.h5')
model1.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# Print test prediction

f2 = open('/home/student/2019_Capstone-design/node/image_predict/label_dict.txt')
label_dict = eval(f2.read())
f2.close()

batchsize = 32
image_size = (48, 48)

img = Image.open('/home/student/2019_Capstone-design/node/image_predict/predict_image/12/out.png')
img = img.resize(image_size, Image.ANTIALIAS)
img = img.convert('L')
inv_image = ImageOps.invert(img)

pred_gen = np.expand_dims(inv_image, axis=0)
pred_gen = pred_gen.reshape(1,48,48,1)

predictions = model1.predict(pred_gen)

np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
import operator
index, value = max(enumerate(predictions[0]), key=operator.itemgetter(1))
pred_result = [name for name, target in label_dict.items() if target == index]

#recommand_top3
re_list = recommand(predictions, label_dict)
print(re_list, sys.argv[1])
