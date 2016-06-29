from PIL import Image
import os

# Read image
im = Image.open('ps0-1-a-2.png')
# Display image
im.show()

# Image size
(width, height) = im.size

print ('hi')