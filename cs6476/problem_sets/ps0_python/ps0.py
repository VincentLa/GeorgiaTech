from PIL import Image
import os

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


def main():
    # Read image
    im1 = Image.open('./output/ps0-1-a-1.png')
    im2 = Image.open('./output/ps0-1-a-2.png')

    # color_planes(im1, im2)
    replacement_pixels(im1, im2)


if __name__ == '__main__':
    main()
