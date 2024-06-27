from typing import Literal
from PIL import Image
from pillow_heif import register_heif_opener


register_heif_opener() 

VALID_IMAGE_FORMATS = ['jpg', 'jpeg', 'png']


def convert_heif(filename, format: Literal['jpg', 'jpeg', 'png']):
    assert format.lower() in VALID_IMAGE_FORMATS
    
    splits = filename.split('.')
    tar = '.'.join(splits[:-1]) + '.' + format.upper()
    img = Image.open(filename)
    img.convert('RGB').save(tar)


def heif_to_jpg(filename):
    convert_heif(filename, format='jpg')
    
    
def heif_to_png(filename):
    convert_heif(filename, format='png')
