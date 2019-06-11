import os
import sys
import PIL 
from PIL import Image
import image_slicer
import numpy as np

NUM_TILES = 7166

path = "c:\\Users\\16102\\Documents\\CS50\\Final_Project"
os.chdir(path)

# load source images
try:
    source_dir = "source_images"
    sources = os.listdir(os.path.join(path, source_dir))
except:
    print("Unable to load source images")
    sys.exit()

# create a grid
input_image = "input_image.jpg"
grid = image_slicer.slice(input_image, NUM_TILES, save=False)
tile_w, tile_h = grid[0].image.size

# resize each source image to tile size
for source in sources:
    if source.lower().endswith((".jpg", ".png", ".jpeg")):
        source_img = Image.open(os.path.join(path, source_dir, source))
        resized = source_img.resize((tile_w, tile_h))
        
        # create outfile 
        shrunk_dir = "shrunk_sources"
        if not os.path.exists(shrunk_dir):
            os.mkdir(shrunk_dir)
        
        outfile = os.path.join(path, shrunk_dir, '%s_shrunk.jpg' % source[:-4])
        resized.save(outfile)  