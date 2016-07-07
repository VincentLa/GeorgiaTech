from PIL import Image
import os
import numpy as np

def color_planes(im1, im2):
    """(a) Swap the red and blue pixels of image 1
           Output: Store as ps0-2-a-1.png in the output folder
       (b) Create a monochrome image (img1_green) by selecting the green channel of image 1
           Output: ps0-2-b-1.png
       (c) Create a monochrome image (img1_red) by selecting the red channel of image 1
           Output: ps0-2-c-1.png
       (d) Which looks more like what you’d expect a monochrome image to look like? Would you expect a computer vision
           algorithm to work on one better than the other?
           Output: Text response in report ps0_report.pdf
    """
    r, g, b = im1.split()
    ps0_2_a_1 = Image.merge('RGB', (b, g, r))
    ps0_2_a_1.show()
    ps0_2_a_1.save('./output/ps0-2-a-1.png', format='png')

    img1_green = g
    img1_green.save('./output/ps0-2-b-1.png', format='png')

    img1_red = r
    img1_red.save('./output/ps0-2-c-1.png', format='png')


def replacement_pixels(im1, im2):
    """
    Take the center square region of 100 x100 pixels of monochrome version of image 1 and insert them into the
    center of monochrome version of image 2 Output: Store the new image created as ps0-3-a-1.png
    """
    r, img1_mono, b = im1.split()
    r, img2_mono, b = im2.split()

    img1_mono_width = img1_mono.size[0]
    img1_mono_height = img1_mono.size[1]

    img2_mono_width = img2_mono.size[0]
    img2_mono_height = img2_mono.size[1]

    img1_center_region = (img1_mono_width//2 - 50, img1_mono_height//2 - 50, img1_mono_width//2 + 50, img1_mono_height//2 + 50)
    img1_mono_crop = img1_mono.crop(img1_center_region)

    img2_center_region = (img2_mono_width//2 - 50, img2_mono_height//2 - 50, img2_mono_width//2 + 50, img2_mono_height//2 + 50)
    img2_mono.paste(im=img1_mono_crop, box=img2_center_region)
    ps0_3_a_1 = img2_mono
    ps0_3_a_1.save('./output/ps0-3-a-1.png', format='png')


def arithmetic_and_geometric_operations(im1, im2):
    """ a. What is the min and max of the pixel values of img1_green? What is the mean?
           What is the standard deviation? And how did you compute these?
           Output: Text response, with code snippets
        b. Subtract the mean from all pixels, then divide by standard deviation, then multiply
           by 10 (if your image is 0 to 255) or by 0.05 (if your image ranges from 0.0 to 1.0).
           Now add the mean back in.
        Output: ps0‐4‐b‐1.png

        c. Shift img1_green to the left by 2 pixels.
        Output: ps0‐4‐c‐1.png

        d. Subtract the shifted version of img1_green from the original, and save the
           difference image.
        Output: ps0‐4‐d‐1.png
            (make sure that the values are legal when you write the image
            so that you can see all relative differences), text response: What do negative pixel
            values mean anyways?"""
    # Part (a)
    r, img1_green, b = im1.split()
    pixels = np.asarray(img1_green)
    pixels_1d = np.asarray(list(img1_green.getdata()))
    img1_green_min = min(pixels_1d)
    img1_green_max = max(pixels_1d)
    img1_green_mean = sum(pixels_1d)/len(pixels_1d)
    img1_green_std = np.std(pixels_1d)

    print('The min pixel value of img1_green is', img1_green_min)
    print('The max pixel value of img1_green is', img1_green_max)
    print('The mean pixel value of img1_green is', img1_green_mean)
    print('The std pixel value of img1_green is', img1_green_std)

    # Part (b)
    ps0_4_b_1_pixels = np.maximum(np.round((pixels - img1_green_mean) / img1_green_std * 10), 0).astype(int)

    print(ps0_4_b_1_pixels)
    ps0_4_b_1 = Image.fromarray(ps0_4_b_1_pixels)
    ps0_4_b_1.save('./output/ps0-4-b-1.png', format='png')

def noise():
    """ a. Take the original colored image (image 1) and start adding Gaussian noise to the
           pixels in the green channel. Increase sigma until the noise is somewhat visible.

        Output: ps0‐5‐a‐1.png, text response: What is the value of sigma you had to use?

        b. Now, instead add that amount of noise to the blue channel.

        Output: ps0‐5‐b‐1.png
        c. Which looks better? Why?

        Output: Text response"""
    pass


def main():
    # Read image
    im1 = Image.open('./output/ps0-1-a-1.png')
    im2 = Image.open('./output/ps0-1-a-2.png')

    #color_planes(im1, im2)
    #replacement_pixels(im1, im2)
    arithmetic_and_geometric_operations(im1, im2)


if __name__ == '__main__':
    main()
