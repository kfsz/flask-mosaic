from flask import Flask, render_template, abort, request, jsonify, send_file
from PIL import Image
from io import BytesIO, StringIO
from random import shuffle
import requests
import math
import re

app = Flask(__name__)

def create_mosaic(img_loc, size):
    '''Create mosaic using images from given urls and size.'''
    # create empty image
    fill_color = 'black'
    mozaic = Image.new('RGB', size, fill_color)
    
    image_number = len(img_loc)
    odd_image = False
    
    # basic mosaic layout creation
    if image_number >= 3:
        rows = image_number//2
        columns =  2
        if image_number%2 == 1:
            odd_image = True
    else:
        rows = image_number
        columns =  1
    
    # switch rows with columns (image placement) depending
    # on wherever is more free space available
    if size[1] > size[0]:
        rows, columns = columns, rows

    # create image restrictions
    horizontal_change = size[0]//rows
    vertical_change = size[1]//columns
    
    # adjust image restrictions when creating mosaic
    # with odd number of images
    if odd_image:
        if horizontal_change > vertical_change:
            horizontal_change = size[0]//(rows+1)
            rows += 1
        else:
            vertical_change = size[1]//(columns+1)
            columns += 1
  
    current = 0
    current_row = 0
    current_column = 0
    
    for i in range(0, size[0], horizontal_change):
        current_row = 0
        current_column += 1
        for j in range(0, size[1], vertical_change):
        
            # check if out of bounds
            if j + vertical_change > size[1]:
                break
                
            # load and open image
            try:
                file_url = img_loc.pop(0)
            except IndexError:
                break
            response = requests.get(file_url)
            img = Image.open(BytesIO(response.content))

            current_row += 1            
            current += 1
            
            # resize images based on free space available
            if odd_image and current==image_number and horizontal_change > vertical_change:
                img = img.resize((horizontal_change, vertical_change*2), Image.ANTIALIAS)
            elif (current_column == rows-1 and current+columns>image_number and
                  (horizontal_change <= vertical_change or
                   current+columns>image_number+1)): # special case for 7 pic mosaic
                   # with stretched image and still empty space at the bottom
                img = img.resize((horizontal_change*2, vertical_change), Image.ANTIALIAS)
            else:
                img = img.resize((horizontal_change, vertical_change), Image.ANTIALIAS)
            mozaic.paste(img, (i,j))
    
    return mozaic
    
def serve_pil_image(pil_img):
    '''Send image from Flask.'''
    #size = 2048, 2048
    #pil_img = pil_img.resize(size, Image.ANTIALIAS)
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=90)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')
    
@app.route('/mozaika', methods=['GET'])
def mosaic():
    '''Basic endpoint for getting mosaic image.'''
    # get parameters
    random = request.args.get('losowo')
    size = request.args.get('rozdzielczosc')
    images = request.args.get('zdjecia')
    
    # check if number of supplied images is correct
    print(images)
    if images:
        images = images.split(sep=',')
        if images is False or len(images) > 8:
            return abort(400)
    else:
        return abort(400)
  
    # size validation and processing
    if size and re.match(r"[1-9][0-9]*x[1-9][0-9]*", size):
        size = size.split(sep='x')
        size = [int(i) for i in size]
    else:
        size = (2048, 2048)
    
    # randomize
    if random and random==str(1):
        shuffle(images)
        
    mosaic = create_mosaic(images, size)
    return serve_pil_image(mosaic)
    

if __name__ == '__main__':
    app.run()