import keras
import matplotlib
import numpy as np
import os
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten
from keras.preprocessing.image import ImageDataGenerator
from PIL import Image

'''
    - Keras base image classification 
    - Latest update : 10.31
    - Last acc : 80.12%
    - version : 1.52

'''


def image_set():
    print("Get images....")
    # image_set()

    batchsize = 64
    image_size = (255, 255)

    #
    train_gen = ImageDataGenerator().flow_from_directory(
        '/home/mll/Capstone/fix_image_set/train/',
        class_mode='categorical',
        batch_size=batchsize,
        target_size=image_size
    )

    test_gen = ImageDataGenerator().flow_from_directory(
        '/home/mll/Capstone/fix_image_set/test/',
        class_mode='categorical',
        batch_size=batchsize,
        target_size=image_size
    )
    valid_gen = ImageDataGenerator().flow_from_directory(
        '/home/mll/Capstone/fix_image_set/valid/',
        class_mode='categorical',
        batch_size=batchsize,
        target_size=image_size
    )

    return train_gen, test_gen, valid_gen


def createModel(numclass):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), padding='same', activation='sigmoid', input_shape=(255, 255, 3)))
    model.add(Conv2D(32, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(16, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(16, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(16, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(16, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(numclass, activation='softmax'))  # label count = dense label.

    return model


import matplotlib.pyplot as plt


def plt_show_loss(history):
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model Loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc=0)


def plt_show_acc(history):
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc=0)


def main():
    print("Start....")

    train_gen, test_gen, valid_gen = image_set()
    numclass = train_gen.num_classes
    print(train_gen.num_classes)
    print("(1) Train model | (2) Load saved model")
    number = input()

    if (number == "1"):
        print("Model build....")
        model1 = createModel(numclass)
        model1.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        print("Training....")
        history = model1.fit_generator(train_gen, steps_per_epoch=2000, epochs=100, validation_data=valid_gen,
                                       validation_steps=100)
        # origin : step 200 epoch 100

        # Saving model
        # Save sturcture to json file, weight to h5 file.

        print("Input model's name")
        name = input()
        model1.save('save_model/{}.h5'.format(name))

        plt_show_loss(history)
        plt.show()

        plt_show_acc(history)
        plt.show()


    elif (number == "2"):
        from keras.models import load_model

        model_list = os.listdir('./save_model')
        print('---- Saved model list ----')
        for model_file in model_list:
            print(model_file)

        print("Input model_structure 's name (json only)")
        name = input()
        model1 = load_model('./save_model/{}'.format(name))

        model1.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])  # model compile


    else:
        print("wrong input")
        exit()

    print("Test....")
    scores = model1.evaluate_generator(test_gen, steps=10)
    print("%s: %.2f%%" % (model1.metrics_names[1], scores[1] * 100))
    print("loss : ", scores[0], "/ acc : ", scores[1])

    model1.summary()

    # ----------------------#
    # Recommended labels top3

    # Print test prediction
    print("-- Predict --")
    batchsize = 64
    image_size = (255, 255)
    pred_gen = ImageDataGenerator().flow_from_directory(
        '/home/mll/Capstone/predict_image/',
        class_mode='categorical',
        batch_size=batchsize,
        target_size=image_size
    )
    predictions = model1.predict_generator(pred_gen)
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
    import operator
    index, value = max(enumerate(predictions[0]), key=operator.itemgetter(1))
    pred_result = [name for name, target in test_gen.class_indices.items() if target == index]
    print("label : " + index, "| acc : ", value)
    print("-- pred is : " + pred_result)


if __name__ == "__main__":
    main()
