# Photomosaic
</p>Create a photomosaic. The program divides an input image into tiles. 
It then fills each tile with source images, selected based on the closest 
matching rgb value to the original color of the tile.</p>

![Image of Generator](/readme_image.png)

## Getting Started
### Prerequisites
- Download modules: Scikit-image, pillow, image_slicer
- shrink.py file 
- A main image (AKA input image) to be divided into tiles
- A folder of source images to fill the tiles (e.g., a folder of puppy images)

### Running
- rename your input image to "input_image"
- rename your source folder to "source_images"
- run shrink.py 
    - Will create a new folder "shrunk_sources"
    - Saves resized copies of your source images to this file
    - Image dimensions will match the tile size
- run photomosaic_CS50.py
    - Calculates average rgb value of each tile 
    - Calculates average rgb of each source image
    - Caches average rgb values of source images to JSON file "source_cache.json"
    - Matches rgb values of source images to tiles using euclidian distance
    - Replaces tile with match
    - Joins tiles into mosaic
    - Saves "photomosaic.jpg" to your folder

### Author
- Matthew Goodman

### Acknowledgments
- Robert Heaton (http://www.robertheaton.com) for the inspiration
- CS50 staff for the incredible course




