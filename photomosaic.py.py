import PIL as pil
from PIL import ImageFilter, ImageFont, ImageDraw, Image
import image_slicer
from image_slicer import join
import numpy as np
import os, sys
from skimage import io
from skimage.transform import resize
import time
import json


path = "c:\\Users\\16102\\Documents\\CS50\\Final_Project"
os.chdir(path)

# number of tiles that will make up the input image
NUM_TILES = 7166


def main():
    start = time.time()
    # input file name
    input_image = "input_image.jpg"
    
    # load list of source images
    try:
        source_dir = "shrunk_sources"
        sources = os.listdir(os.path.join(path, source_dir))
    except:
        print("Unable to load source images")
        sys.exit()
    
    # create an image grid 
    grid = image_slicer.slice(input_image, NUM_TILES, save=False)

    # calculate average rbg from tiles, save in dictionary
    avg_tile_rgb = average_tile_rbg(grid)
    
    # calculate average rbg from source images
    avg_source_rgb = average_source_rgb(sources) 
    
    # match source to input tile
    match_dict = match_source(avg_tile_rgb, avg_source_rgb)
    
    # replace tiles with match
    for tile in grid:
        match = match_dict[tile]
        match_img = Image.open(os.path.join(path, source_dir, match))
        tile.image = match_img
           
    # sew together to make mosaic and crop
    mosaic = join(grid)
       
    # save mosaic
    mosaic.save('photomosaic.jpg')
    end = time.time()
    print(end-start)
    

def average_tile_rbg(grid):
    tile_values = {}

    # grab rgb value of each tile
    for tile in grid:
        tile_img = tile.image.convert('RGB')
        width, height = tile_img.size


        # average each pixel
        r, g, b = 0, 0, 0
        count = 0
        for w in range(0, width):
            for h in range(0, height, 20): 
                pixlr, pixlg, pixlb = tile_img.getpixel((w,h))
                r += pixlr
                g += pixlg
                b += pixlb
                count += 1
                
        tile_values[tile] = (int(r/count), int(g/count), int(b/count))
        
    return tile_values


def average_source_rgb(sources):
    # see if average rgb already in cache
    if os.path.isfile("source_cache.json"):
        with open("source_cache.json", "r") as read_file: 
            source_values = json.load(read_file)
            return source_values
        
    source_values = {}   
    # grab rgb value of each source
    for source in sources:
        source_img = io.imread(os.path.join(path, source_dir, source))       
        array_average = source_img.mean(axis=0).mean(axis=0)
        rgb_average = (int(array_average[0]), int(array_average[1]), int(array_average[2]))

        # save new dictionary value per source {name: average}      
        source_values[source] = rgb_average
    
    cache_dict(source_values, "source")
    return source_values
    
    
def cache_dict(dictionary, name):
    file_name = "%s_cache.json" % name
    if not os.path.isfile(file_name):
        with open(file_name, "w") as write_file:
            json.dump(dictionary, write_file)
            

def match_source(tile_rgb, source_rgb):   
    # tile and source matches
    tile_source_match = {}
    
    # get r,g,b value from each tile
    for tile in tile_rgb:
        source_values = {}
        tile_r, tile_g, tile_b = tile_rgb[tile][0], tile_rgb[tile][1], tile_rgb[tile][2]
       
        # get r,g,b value from each source
        for source in source_rgb:
            source_r, source_g, source_b = source_rgb[source][0], source_rgb[source][1], source_rgb[source][2]
            
            # calculate euclidean distance formula and append to dict
            pyth_value = np.sqrt((tile_r - source_r)**2 + (tile_g - source_g)**2 + (tile_b - source_b)**2)
            source_values[source] = pyth_value 
            
        # check source value closest to tile and append to matched dict
        min_val_name = min(source_values, key = lambda x: source_values.get(x) )
        tile_source_match[tile] = min_val_name

    return tile_source_match 
 
    
if __name__ == "__main__":
    main()
    
    
