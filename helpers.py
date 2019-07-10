#!/usr/bin/env python3

# Imports
from PIL import Image

# Global variables

# Class declarations
class ImageHelper():
    @staticmethod
    def convert_rgba_to_rgb(image, color=(0, 0, 0)):
        background = Image.new('RGB', image.size, color)
        background.paste(image, mask=image.split()[3])
        return background

    @staticmethod
    def convert_any_to_rgb(image):
        bands = image.getbands()
        if bands == ('R', 'G', 'B', 'A'):
            image = ImageHelper.convert_rgba_to_rgb(image)
        elif bands != ('R', 'G', 'B'):
            image = image.convert('RGB')
        return image

    @staticmethod
    def resize_image(image, size):
        if image.size != size:
            image = image.resize(size)
        return image