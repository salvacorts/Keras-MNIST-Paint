from keras.models import model_from_json
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Activation
from keras.layers import Flatten
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.utils import np_utils
from keras.datasets import mnist
import numpy as np


(X_train, y_train), (X_test, y_test) = mnist.load_data()
print(y_train.shape)    # Only labels
print(X_train.shape)    # Data

# We have (n, width, height) but we need (n, depth, width, height)
# where n is the number of entries
X_train = X_train.reshape(X_train.shape[0], 28, 28, 1)
X_test = X_test.reshape(X_test.shape[0], 28, 28, 1)

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
# Each entry is (256, 256, 256) bcause is RGB, dividing by 255 we will make it be between 0 and 1
X_train /= 255
X_test /= 255

# Our labels are bad formated, because we need to have a Nth dimensional array
# according to the all possible labels we can have.
# In this case we have 10 different values
Y_train = np_utils.to_categorical(y_train, 10)
Y_test = np_utils.to_categorical(y_test, 10)

# ConvNet architectures:
#   1º Convolutional Layer
#   2º Pooling Layer
#   3º Fully-Connected Layer
# REF: https://cs231n.github.io/convolutional-networks/

# Now we will define out NN
model = Sequential() # First One layer and then the next

####### Convultional Layer #######
# Add a layer with:
# 32 Convultion filters
# (3 rows and 3 cols for each convultion filter)
# Relu activation: will return = if value is below 0 and raw input if above
# An input with 1 depth (channels), 28 widht and 28 height
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(28,28,1)))
model.add(Conv2D(32, (3, 3), activation='relu'))   # Add another layer

####### Pooling Layer #######
# To reduce the parameters, it will take the maximum of the 4 values (2x2)
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))  # To avoid overfitting

####### Fully-Connected Layer #######
# The weights from the Convolution layers must be flattened (made 1-dimensional)
# before passing them to the fully connected Dense layer.
model.add(Flatten())
model.add(Dense(128, activation='relu'))    # output of 120
model.add(Dropout(0.5))
# Softmax allow us to convert inputs to values between 0 and 1. The sum of them will be 1
# REF: https://github.com/Kulbear/deep-learning-nano-foundation/wiki/ReLU-and-Softmax-Activation-Functions
model.add(Dense(10, activation='softmax'))  # output of 10 (final layer!!!)



# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
# batch_size: Fom training dataset how many entries use each time
# nb_epoch: Neural networks are trained iteratively,
#   making multiple passes over entire dataset.
#   Each pass over entire dataset is referred to as epoch.
model.fit(X_train, Y_train, batch_size=32, epochs=10, verbose=1)


score = model.evaluate(X_test, Y_test, verbose=0)
print("Score: {}".format(score))

# Save Model
#   REF: https://machinelearningmastery.com/save-load-keras-deep-learning-models/
model.save_weights("models/model.weights")
with open("models/model.json", "w") as json_file:
    model_json = model.to_json()
    json_file.write(model_json)
