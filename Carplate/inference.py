import os
import sys
import random
import math
import re
import time
import numpy as np
import tensorflow as tf
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import skimage
import skimage.io
import skimage.transform

import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K

# Root directory of the project
ROOT_DIR = os.path.abspath("./")

# Import Mask RCNN
sys.path.append(os.path.join(ROOT_DIR, "Mask_RCNN"))  # To find local version of the library
from mrcnn import utils
from mrcnn import visualize
from mrcnn.visualize import display_images
import mrcnn.model as modellib
from mrcnn.model import log

import carplate


# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

CARPLATE_WEIGHTS_PATH = "mask_rcnn_carplate_0030.h5"  

config = carplate.CarplateConfig()
CARPLATE_DIR = os.path.join(ROOT_DIR, "dataset/carplate")

# Override the training configurations with a few
# changes for inferencing.
class InferenceConfig(config.__class__):
    # Run detection on one image at a time
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

config = InferenceConfig()

# Device to load the neural network on.
# Useful if you're training a model on the same 
# machine, in which case use CPU and leave the
# GPU for training.
#DEVICE = "/gpu:0"  # /cpu:0 or /gpu:0
DEVICE = "/cpu:0"
# Inspect the model in training or inference modes
# values: 'inference' or 'training'
# TODO: code for 'training' test mode not ready yet
TEST_MODE = "inference"

def get_ax(rows=1, cols=1, size=16):
    """Return a Matplotlib Axes array to be used in
    all visualizations in the notebook. Provide a
    central point to control graph sizes.
    
    Adjust the size attribute to control how big to render images
    """
    _, ax = plt.subplots(rows, cols, figsize=(size*cols, size*rows))
    return ax

# Create model in inference mode
with tf.device(DEVICE):
    model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

# Load weights
weights_path = CARPLATE_WEIGHTS_PATH
print("Loading weights", weights_path)
model.load_weights(weights_path, by_name=True)


image = skimage.io.imread('./dataset/carplate/val/粤BZ89M9.jpg')
min_dim=config.IMAGE_MIN_DIM
min_scale=config.IMAGE_MIN_SCALE
max_dim=config.IMAGE_MAX_DIM
mode=config.IMAGE_RESIZE_MODE
image, window, scale, padding, crop = utils.resize_image(
        image,
        min_dim=config.IMAGE_MIN_DIM,
        min_scale=config.IMAGE_MIN_SCALE,
        max_dim=config.IMAGE_MAX_DIM,
        mode=config.IMAGE_RESIZE_MODE)
results = model.detect([image], verbose=1)
ax = get_ax(1)
r = results[0]
'''
visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], 
                            ['','carplate'], r['scores'], ax=ax,
                            title="Predictions")
                            '''


# 假设只有一个车牌
p = np.where(r['masks'].flatten() == True)[0]
'''
print(r['masks'].flatten())
print(len(r['masks']))
print(len(r['masks'][0]))
print(np.where(r['masks'] == True))
print(p)
print(image.shape[0])
print(image.shape[1])
'''
x0 = np.min([i%image.shape[1] for i in p])
x1 = np.max([i%image.shape[1] for i in p])
y0 = np.min([i//image.shape[1] for i in p])
y1 = np.max([i//image.shape[1] for i in p])
#print(x0,x1,y0,y1)
img = image[y0:y1, x0:x1]
skimage.io.imshow(img)


import skimage.io as io
import skimage.color as color
import skimage.morphology as morphology
import skimage.feature as feature
import skimage.measure as measure
import skimage.transform as transform
import numpy as np
import math

from matplotlib import pyplot as plt
# 1. 转换为灰度图像
img2 = color.rgb2gray(img)
#io.imshow(img2)
# 2. Canny边缘检测并膨胀
img3 = feature.canny(img2, sigma=3)
img4 = morphology.dilation(img3)
#io.imshow(img4)
# 3. 标记并筛选区域
label_img = measure.label(img4)
regions = measure.regionprops(label_img)

fig, ax = plt.subplots()
#ax.imshow(img, cmap=plt.cm.gray)

def in_bboxes(bbox, bboxes):
    for bb in bboxes:
        minr0, minc0, maxr0, maxc0 = bb
        minr1, minc1, maxr1, maxc1 = bbox
        if minr1 >= minr0 and maxr1 <= maxr0 and minc1 >= minc0 and maxc1 <= maxc0:
            return True
    return False

bboxes = []
for props in regions:
    y0, x0 = props.centroid
    minr, minc, maxr, maxc = props.bbox
    
    if maxc - minc > img4.shape[1] / 7 or maxr - minr < img4.shape[0] / 3:
        continue
        
    bbox = [minr, minc, maxr, maxc]
    if in_bboxes(bbox, bboxes):
        continue
        
    if abs(y0 - img4.shape[0] / 2) > img4.shape[0] / 4:
        continue
        
    bboxes.append(bbox)
    
    bx = (minc, maxc, maxc, minc, minc)
    by = (minr, minr, maxr, maxr, minr)
    #ax.plot(bx, by, '-r', linewidth=2)

# 4. 提取单个字符图像
bboxes = sorted(bboxes, key=lambda x: x[1])
chars = []
for bbox in bboxes:
    minr, minc, maxr, maxc = bbox
    ch = img2[minr:maxr, minc:maxc]
    chars.append(ch)
    #io.imshow(ch)
    #plt.show()

'''字符识别'''
DATASET_DIR = 'dataset/carplate'
#classes = os.listdir(DATASET_DIR + "/ann/")
classes=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
         '川', '鄂', '赣', '甘', '贵', '桂', '黑', '沪', '冀', '津', '京', '吉', '辽',
         '鲁', '蒙', '闽', '宁', '青', '琼', '陕', '苏', '晋', '皖', '湘', '新',
         '豫', '渝', '粤', '云', '藏', '浙']
num_classes = len(classes)
img_rows, img_cols = 20, 20

if K.image_data_format() == 'channels_first':
    input_shape = [1, img_rows, img_cols]
else:
    input_shape = [img_rows, img_cols, 1]

    
model_char = Sequential()
model_char.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=input_shape))
model_char.add(Conv2D(64, (3, 3), activation='relu'))
model_char.add(MaxPooling2D(pool_size=(2, 2)))
model_char.add(Dropout(0.25))
model_char.add(Flatten())
model_char.add(Dense(128, activation='relu'))
model_char.add(Dropout(0.5))
model_char.add(Dense(num_classes, activation='softmax'))

model_char.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

model_char.load_weights("char_cnn/char_cnn.h5")


def extend_channel(data):
    if K.image_data_format() == 'channels_first':
        data = data.reshape(data.shape[0], 1, img_rows, img_cols)
    else:
        data = data.reshape(data.shape[0], img_rows, img_cols, 1)
        
    return data

chars2 = []
for ch in chars:
    chars2.append(transform.resize(ch, [img_rows, img_cols]))
    
chars2 = np.stack(chars2)

ys = np.unique(classes)

p_test = model_char.predict_classes(extend_channel(chars2))

#print(' '.join([ys[p_test[i]] for i in range(len(p_test))]))
final=''.join([classes[p_test[i]] for i in range(len(p_test))])
print(final)