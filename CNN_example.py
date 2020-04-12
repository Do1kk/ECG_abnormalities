from keras.datasets import mnist

# download mnist data and split into train and test sets
(X_train, y_train), (X_test, y_test) = mnist.load_data()

import matplotlib.pyplot as plt

# plot the first image in the dataset
# plt.imshow(X_train[0])
# plt.show()

# check image shape
X_train[0].shape
y_train[0].shape

# reshape data to fit model
# liczba zdjęć, rozmiar x (zdjęcia), rozmiar y (zdjęcia), liczba kolorów (1 - odcienie szarości)
X_train = X_train.reshape(60000, 28, 28, 1)
X_test = X_test.reshape(10000, 28, 28, 1)

from keras.utils import to_categorical

# one-hot encode target column
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

y_train[0]

from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten

# create model
model = Sequential()

# add model layers
# 64 - liczba neuronów, kernel_size - maska 3x3,
model.add(Conv2D(64, kernel_size=3, activation="relu", input_shape=(28, 28, 1)))
model.add(Conv2D(32, kernel_size=3, activation="relu"))
# warstwa łącząca conv2d z warstwą dense
model.add(Flatten())
# liczba taka ile wyjść, tu 10 liczb (u mnie będzie 6 wyjść bo tyle jest typów)
model.add(Dense(10, activation="softmax"))

# compile model using accuracy to measure model performance
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# train the model
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=3)

# predict first 4 images in the test set
model.predict(X_test[:4])

# actual results for first 4 images in test set
y_test[:4]
