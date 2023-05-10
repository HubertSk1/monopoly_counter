from tensorflow import keras
import numpy as np
import glob
import cv2

x_train=[]
y_train=[]
x_test=[]
y_test=[]

#UTWORZENIE ZBIOROW UCZACEGO I TESTOWEGO
number=0
for sciezka in glob.glob("do_sieci/zielony/*.png"):
    img=cv2.imread(sciezka,cv2.IMREAD_REDUCED_COLOR_2)
    img=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # (img,_,_) = cv2.split(img)  
    if number%5==0:
        x_test.append(img)
        y_test.append([1,0,0,0,0,0])
    else :
        x_train.append(img)
        y_train.append([1,0,0,0,0,0])
    number+=1
for sciezka in glob.glob("do_sieci/zolty/*.png"):
    img=cv2.imread(sciezka,cv2.IMREAD_REDUCED_COLOR_2)
    img=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # (img,_,_) = cv2.split(img)
    if number%5==0:
        x_test.append(img)
        y_test.append([0,1,0,0,0,0])
    else :
        x_train.append(img)
        y_train.append([0,1,0,0,0,0])
    number+=1
for sciezka in glob.glob("do_sieci/szary/*.png"):
    img=cv2.imread(sciezka,cv2.IMREAD_REDUCED_COLOR_2)
    img=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # (img,_,_) = cv2.split(img)
    if number%5==0:
        x_test.append(img)
        y_test.append([0,0,1,0,0,0])
    else :
        x_train.append(img)
        y_train.append([0,0,1,0,0,0])
    number+=1  
for sciezka in glob.glob("do_sieci/niebieski/*.png"):
    img=cv2.imread(sciezka,cv2.IMREAD_REDUCED_COLOR_2)
    img=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # (img,_,_) = cv2.split(img)
    if number%5==0:
        x_test.append(img)
        y_test.append([0,0,0,1,0,0])
    else :
        x_train.append(img)
        y_train.append([0,0,0,1,0,0])
    number+=1
for sciezka in glob.glob("do_sieci/fiolet/*.png"):
    img=cv2.imread(sciezka,cv2.IMREAD_REDUCED_COLOR_2)
    img=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # (img,_,_) = cv2.split(img)
    if number%5==0:
        x_test.append(img)
        y_test.append([0,0,0,0,1,0])
    else :
        x_train.append(img)
        y_train.append([0,0,0,0,1,0])
    number+=1
for sciezka in glob.glob("do_sieci/czerwony/*.png"):
    img=cv2.imread(sciezka,cv2.IMREAD_REDUCED_COLOR_2)
    img=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # (img,_,_) = cv2.split(img)
    if number%5==0:
        x_test.append(img)
        y_test.append([0,0,0,0,0,1])
    else :
        x_train.append(img)
        y_train.append([0,0,0,0,0,1])
    number+=1
    

x_train=np.array(x_train)/255
y_train=np.array(y_train)
print(len(x_train))
x_test=np.array(x_test)/255
y_test=np.array(y_test)

# model=keras.models.Sequential()
# model.add(keras.layers.Conv2D(32, (3, 3), activation='leaky_relu', input_shape=(32, 32, 3)))
# model.add(keras.layers.MaxPooling2D((1, 1)))
# model.add(keras.layers.Conv2D(40, (10, 10), activation='leaky_relu'))
# model.add(keras.layers.MaxPooling2D((1, 1)))
# model.add(keras.layers.Conv2D(45, (3, 3), activation='leaky_relu'))
# model.add(keras.layers.MaxPooling2D((1, 1)))
# model.add(keras.layers.Conv2D(50, (3, 3), activation='leaky_relu'))
# model.add(keras.layers.Flatten())
# model.add(keras.layers.Dense(6, activation='softmax'))

# model.compile(optimizer = "adam", loss = "categorical_crossentropy", metrics = ["accuracy"])
# model.fit(x = x_train, y = y_train, epochs = 50, batch_size = 1000)
# model.save('cnn2.h5')
# preds =  model.evaluate(x = x_test, y = y_test)
# print(preds)

model= keras.models.load_model("cnn2.h5")
preds =  model.evaluate(x = x_test, y = y_test)
preds=model.predict(x_test[:100])
etykiety=[]
for predykcja in preds:
    n=0
    for wartosc in predykcja:
        if wartosc==max(predykcja):
            etykiety.append(n);
        n+=1
print(etykiety)