import os

from PIL import Image
from . import landmass

def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    height_map_path = os.path.join(script_dir, 'resource/Maldives.png')
    height_map = Image.open(os.path.join(script_dir, 'resource/Maldives.png'))
