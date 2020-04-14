# from keras.datasets import mnist
from numpy import load
import matplotlib.pyplot as plt

numpy_file_dir = "NN_files/"
# load dict of arrays
X_train = load(numpy_file_dir + "X_train.npz")
y_train = load(numpy_file_dir + "y_train.npz")
X_test = load(numpy_file_dir + "X_test.npz")
y_test = load(numpy_file_dir + "y_test.npz")

# extract the first array
X_train = X_train["arr_0"]
y_train = y_train["arr_0"]
X_test = X_test["arr_0"]
y_test = y_test["arr_0"]

# download mnist data and split into train and test sets
# (X_train, y_train), (X_test, y_test) = mnist.load_data()

# plot the first image in the dataset
plt.imshow(X_train[0])
plt.show()

# check image shape
print(X_train.shape)
print(y_train.shape)

# reshape data to fit model
# liczba zdjęć, rozmiar x (zdjęcia), rozmiar y (zdjęcia), liczba kolorów (1 - odcienie szarości)
# X_train = X_train.reshape(60000, 28, 28, 1)
# X_test = X_test.reshape(10000, 28, 28, 1)

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
model.add(Conv2D(64, kernel_size=5, activation="relu", input_shape=(220, 220, 3)))
model.add(Conv2D(32, kernel_size=3, activation="relu"))
model.add(Conv2D(16, kernel_size=3, activation="relu"))
model.add(Conv2D(16, kernel_size=3, activation="relu"))
# warstwa łącząca conv2d z warstwą dense
model.add(Flatten())
# liczba taka ile wyjść, tu 10 liczb (u mnie będzie 6 wyjść bo tyle jest typów)
model.add(Dense(6, activation="softmax"))

# compile model using accuracy to measure model performance
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# train the model
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=3)

# predict first 4 images in the test set
print(model.predict(X_test[:4]))

# actual results for first 4 images in test set
print(y_test[:4])
