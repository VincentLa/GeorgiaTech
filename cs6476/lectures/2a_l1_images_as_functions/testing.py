from PIL import Image
import numpy as np
import os

# Read image
im = Image.open('ps0-1-a-1.png')
im2 = Image.open('ps0-1-a-2.png')
# Display image
im.show()

# Image size
# (width, height) tuple
size = im.size

print(size)

# Getting RGB Values
pixels = list(im.getdata())

# Accessing a specific pixel
print(im.getpixel((100,100)))

# Cropping an image
# Starts Top Left, Top Right, Bottom Right, Bottom Left
box_crop = (100, 150, 500, 300)
im_crop = im.crop(box_crop)
im_crop.show()

# Adding images together.
# http://stackoverflow.com/questions/524930/numpy-pil-adding-an-image
im1arr = np.asarray(im)
im2arr = np.asarray(im2)

im1arrF = im1arr.astype('float')
im2arrF = im2arr.astype('float')

print(im1arrF + im2arrF)

additionF = np.minimum(im1arrF + im2arrF, 256)
addition = additionF.astype('uint8')

resultImage = Image.fromarray(addition)
resultImage.show()

#Blending Images
blended_im = Image.blend(im, im2, 0.5)
blended_im.show()
