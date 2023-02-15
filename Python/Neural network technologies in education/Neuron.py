# -*- coding: utf-8 -*-
"""Ронгинский Ф.А. 15 февраля.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17A4u0wkgZQd52PmGjko05MwqQTexxAf8

Подключаем библиотеки
"""

# Commented out IPython magic to ensure Python compatibility.
import matplotlib
import numpy as np
from keras.datasets import cifar10
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.layers import Dropout
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.utils import np_utils
from keras.preprocessing import image
import matplotlib.pyplot as plt
import tensorflow as tf
# %matplotlib inline

# Размер мини-выборки
batch_size = 128
# Количество классов изображений
nb_classes = 10
# Количество эпох для обучения
nb_epoch = 25
# Размер изображений
img_rows, img_cols = 32, 32
# Количество каналов в изображении: RGB
img_channels = 3
# Название классов из набора данных CIFAR-10
classes = ['самолет','автомобиль','птица','кот','олень','собака','лягушка','лошадь','корабль','грузовик']

"""**Подготовка данных**

Загружаем данные
"""

(X_train, y_train), (X_test, y_test) = cifar10.load_data()

"""Просмотр примеров данных"""

n = 167
plt.imshow(X_train[n])
plt.show()
print("Номер класса: ", y_train[n])
print("Тип объекта: ", classes[y_train[n][0]])

"""Нормализуем данные"""

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255

"""Преобразуем правильные ответы в формат one hot encoding"""

Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)

"""**Создаём нейронную сеть**"""

# Создаём последовательную модель
model = Sequential()
# Первый сверточный слой
model.add(Conv2D(32,(3,3), padding='same', input_shape=(32,32,3), activation='relu'))
# Второй сверточный слой
model.add(Conv2D(32,(3,3), padding='same', activation = 'relu'))
# Первый слой подвыборки
model.add(MaxPooling2D(pool_size=(2,2)))
# Слой регуляризации
model.add(Dropout(0.25))
# Третий сверточный слой
model.add(Conv2D(64, (3,3), padding='same', activation='relu'))
# Четвертый сверточный слой
model.add(Conv2D(64, (3,3), activation='relu'))
# Второй слой подвыборки
model.add(MaxPooling2D(pool_size=(2,2)))
# Слой регуляризации
model.add(Dropout(0.25))
# Слой преобразования данных с понижением размерности
model.add(Flatten())
# Полносвязный слой для классификации
model.add(Dense(512, activation='relu'))
# Слой регуляризации
model.add(Dropout(0.5))
# Выходной полносвязный слой
model.add(Dense(nb_classes, activation='softmax'))

"""Печатаем информацию о сети"""

print(model.summary())

"""Компилируем модель"""

from keras.optimizers.optimizer_v1 import Optimizer
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

"""Обучение нейронной сети"""

history = model.fit(X_train, Y_train,
                    batch_size=batch_size,
                    epochs=nb_epoch,
                    validation_split=0.1,
                    shuffle=True,
                    verbose=2)

"""Оцениваем качество обучения сети"""

scores=model.evaluate(X_test, Y_test, verbose=0)
print("Точность работы на тестовых данных: %2f%%"%(scores[1]*100))

"""Графически"""

history_dict = history.history
print(history_dict.keys())
acc_values = history_dict['accuracy']
val_acc_values = history_dict['val_accuracy']
epochs = range(1, len(acc_values)+1)
plt.plot(epochs, acc_values, 'bo', label = 'Training acc')
plt.plot(epochs, val_acc_values, 'b', label = 'Validation acc')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

"""Сохраняем обученную нейронную сеть

"""

model_json = model.to_json()
json_file = open("cifar10_model.json", "w")
json_file.write(model_json)
json_file.close()
model.save_weights('cifar10_model.h5')

!ls

from google.colab import files

files.download("cifar10_model.json")

files.download("cifar10_model.h5")

"""**Применяем сеть для распознавания объектов на изображениях**

Просмотр изображения из набора данных для тестирования
"""

index=11
plt.imshow(X_test[index])
plt.show()

"""Преобразование тестового изображения"""

x = X_test[index]
x = np.expand_dims(x,axis=0)

"""Запуск распознавания"""

prediction = model.predict(x)

"""Печатаем результаты распознавания"""

print(prediction)

"""Преобазуем результаты из формата one hot encoding"""

prediction = np.argmax(prediction)
print(classes[prediction])

"""Печатаем правильный ответ"""

print(classes[y_test[index][0]])

"""Распознавание дополнительного изображения"""

from google.colab import files
 files.upload()

"""Проверяем загрузку файлов"""

!ls

"""Смотрим загруженную картинку"""

img_path = 'frog.png'
img = tf.keras.utils.load_img(img_path, target_size=(32, 32))
img_arr = np.array(img)
plt.imshow(img_arr)
plt.show()

img_arr = img_arr.astype('float32')
img_arr /= 255

my_x = img_arr
my_x = np.expand_dims(my_x, axis=0)

prediction = model.predict(my_x)

print(prediction)

prediction = np.argmax(prediction)

print(classes[prediction])