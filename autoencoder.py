import os
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Input, Conv2D, UpSampling2D, MaxPool2D, BatchNormalization
from tensorflow.keras.models import Model

# Count images from src folder
_, _, files = next(os.walk("data/src_faces"))
src_file_count = len(files)

# Count images from dst folder
_, _, files = next(os.walk("data/dst_faces"))
dst_file_count = len(files)

file_count = None
if dst_file_count > src_file_count:
    file_count = src_file_count
elif dst_file_count < src_file_count:
    file_count = dst_file_count
else:
    file_count = src_file_count = dst_file_count


# Creating train dataset
X = []
for i in range(file_count):
    image = cv.imread('data/src_faces/src_face{i}.jpg'.format(i=i))
    image = cv.resize(image, (200, 200))
    X.append(image)
X = np.asarray(X)

Y = []
for i in range(file_count):
    image = cv.imread('data/dst_faces/dst_face{i}.jpg'.format(i=i))
    image = cv.resize(image, (200, 200))
    Y.append(image)
Y = np.asarray(Y)

# Normalize dataset before training
X = X.astype('float32')
Y = Y.astype('float32')
X /= 255
Y /= 255

# Create model
input_shape = (200, 200, 3)

inputs = Input(shape=input_shape)
x = Conv2D(64, (3, 3), activation='relu', padding='same')(inputs)
x = MaxPool2D(pool_size=(2, 2))(x)
x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)
x = MaxPool2D(pool_size=(2, 2))(x)
x = Conv2D(256, (3, 3), activation='relu', padding='same')(x)
x = MaxPool2D(pool_size=(2, 2))(x)
x = Conv2D(256, (3, 3), activation='relu', padding='same')(x)

x = Conv2D(256, (3, 3), activation='relu', padding='same')(x)
x = UpSampling2D((2, 2))(x)
x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)
x = UpSampling2D((2, 2))(x)
x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
x = UpSampling2D((2, 2))(x)
outputs = Conv2D(3, (3, 3), activation='sigmoid', padding='same')(x)

model = Model(inputs=inputs, outputs=outputs)
model.compile(loss='mean_squared_error', optimizer='adam')
print(model.summary())
model.fit(X, Y, epochs=10, batch_size=50)
model.save('data/models/model_dual_face.h5')

# Test model
prediction = model.predict(X[0:10])

for i in range(5):
    plt.subplot(231), plt.imshow(prediction[i], 'gray')
    plt.subplot(232), plt.imshow(X[i], 'gray')
    plt.subplot(233), plt.imshow(Y[i], 'gray')
    plt.show()