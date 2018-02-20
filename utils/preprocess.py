import numpy as np
import os
import glob
from PIL import Image


def load_list(path):
    data_list = sorted(glob.glob(path, '*.png'))
    return data_list


def load_data(image_list, label_list, start, end, patch_size, num_patch_per_image):
    # start~ (end-1)
    image_patch = np.empty([num_patch_per_image * (end - start), patch_size, patch_size], dtype='float32')
    label_patch = np.empty([num_patch_per_image * (end - start), patch_size, patch_size], dtype='float32')
    for i in range(start, end):
        #load image, extract Y component
        temp_image = np.array(Image.open(image_list[i]))
        temp_label = np.array(Image.open(label_list[i]))

        w = temp_image.shape[0]
        h = temp_image.shape[1]
        rand_x = np.random.randint(w - patch_size, size=num_patch_per_image)
        rand_y = np.random.randint(h - patch_size, size=num_patch_per_image)

        for j in range(num_patch_per_image):
            temp_patch_image = temp_image[rand_x[j]:rand_x[j]+patch_size, rand_y[j]:rand_y[j]+patch_size]
            image_patch[num_patch_per_image*(i-start)+j, :, :] = temp_patch_image

            temp_patch_label = temp_label[rand_x[j]:rand_x[j]+patch_size, rand_y[j]:rand_y[j]+patch_size]
            label_patch[num_patch_per_image * (i - start) + j, :, :] = temp_patch_label

    return image_patch[:, :, :, np.newaxis], label_patch[:, :, :, np.newaxis]

def convert_btw_rgb_ycbcr(image, dir):
    if dir:  # rgb 2 ycbcr
        image_ycbcr = image.convert('YCbCr')
        return image_ycbcr
    else:  # ycbcr to rgb
        image_rgb = image.convert('RGB')
        return image_rgb


def crop_input(input, label):
    # crop input(low_resolution image) size to label(high resolution image) size
    h = label.shape[0]
    w = label.shape[1]
    input = input[0:h, 0:w, :]
    return input


def image_label_gen(image_path, label_path):
    image = np.array(convert_btw_rgb_ycbcr(Image.open(image_path), dir=True))
    label = np.array(convert_btw_rgb_ycbcr(Image.open(label_path), dir=True))
    image = crop_input(input=image, label=label)

    return image, label


if __name__ == '__main__':
    image_name = 'house'
    img_path = "sample/{}.jpg".format(image_name)
    upscale_factor = 3