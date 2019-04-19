from flask import Flask, render_template, abort, request, jsonify, send_file
from PIL import Image
from io import BytesIO, StringIO
from random import shuffle
import requests
import math
# dunno if re should be used
import re

# ' to " later
# https://stackoverflow.com/questions/38421160/combine-multiple-different-images-from-a-directory-into-a-canvas-sized-3x6
# hmmmmmmmmmmmmmmmmmmmm
app = Flask(__name__)

# add support for png files! eh, seems to work
# some resolutions don't work

'''
kay, so only 8 images - maybe should be hardcoded for 'best' positions?
1 - x
2 - xx (change if one size bigger?)
3 - xxx (change if one size bigger?)
4 - xx
    xx
5 - Ixx
    Ixx
6 - xxx
    xxx
7 - Ixxx
    Ixxx
8 - xxxx
    xxxx
'''


def create_img(img_loc, size):

    # create empty image
    fill_color = 'white'
    mozaic = Image.new('RGB', size, fill_color)
    
    image_number = len(img_loc)
    # adjust image number to nearest 2x2 or so
    # MAX 8 IMAGES SO 4x2 SHOULD BE BIGGEST?
    
    # img_loc = img_loc[0]
    #horizontal_change = 1000
    #vertical_change = 1000
    
    # right, so calculations
    # change rows and columns naming
    odd_image = False
    if image_number > 3:
        rows = image_number//2
        columns =  2
        if image_number%2 == 1:
            odd_image = True
    else:
        rows = image_number
        columns =  1
    
    # switch size
    if size[1] > size[0]:
        print(rows, columns)
        rows, columns = columns, rows
        print(rows, columns)
    
    print(str(rows) + " xxx " + str(columns))
    # total size is fucked up, as it assumes horizontal == vertical - FIX - to be removed
    total_size = size[0] * size[1]
    total_size = total_size/image_number
    total_size = int(math.sqrt(total_size))
    horizontal_change = total_size
    vertical_change = total_size
    
    # second part of calculations 
    # check which one is bigger
    horizontal_change = size[0]//rows
    vertical_change = size[1]//columns
    
    if odd_image:
        if horizontal_change > vertical_change:
            horizontal_change = size[0]//(rows+1)
        else:
            vertical_change = size[1]//(rows+1)
    
    print("horizontal_change " + str(horizontal_change))
    print("vertical_change " + str(vertical_change))
    
    current = 0
    print("image # is" + str(image_number))
    for i in range(0, size[0], horizontal_change):
        for j in range(0, size[1], vertical_change):
            # check if out of bounds - shouldn't be needed - remove - tho, hmm; floats
            # yea, floats are fucked - tries to show at 0x3999 for 1080x4000
            if j + vertical_change > size[1]:
                break
            try:
                filepath = img_loc.pop(0)
            except IndexError:
                break
            current += 1 # change that into something nicer
            response = requests.get(filepath)
            img = Image.open(BytesIO(response.content))
            # hmmmmmmmmmmmmmmmmmmmm
            if odd_image and current==image_number and horizontal_change >= vertical_change:
                print('lol, here')
                img = img.resize((horizontal_change, vertical_change*2), Image.ANTIALIAS)
            elif odd_image and current==(image_number//2 + 1) and horizontal_change < vertical_change:
                print('lol, there')
                img = img.resize((horizontal_change*2, vertical_change), Image.ANTIALIAS)
                odd_image = 0
            else:
                img = img.resize((horizontal_change, vertical_change), Image.ANTIALIAS)
            print("current " + str(current) + " at " + str(i) + "x" + str(j))
            mozaic.paste(img, (i,j))
    
    return mozaic
    '''
    response = requests.get(img_loc)
    img = Image.open(BytesIO(response.content))
    # fill transparent pixels with white for later jpg conversion
    fill_color = 'white'
    if img.mode in ('RGBA', 'LA'):
        background = Image.new(img.mode[:-1], img.size, fill_color)
        background.paste(img, img.split()[-1])
        img = background
    return img
    '''
    
def serve_pil_image(pil_img):
    #size = 2048, 2048
    #pil_img = pil_img.resize(size, Image.ANTIALIAS)
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=90)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')
    
@app.route('/mozaika', methods=['GET'])
def mosaic():
    random = request.args.get('losowo')
    size = request.args.get('rozdzielczosc')
    images = request.args.get('zdjecia').split(sep=',')
    
    #### RANDOMIZE LIST ORDER IF RANDOM
    
    # size processing
    # dunno, really
    if size and re.match(r"[1-9][0-9]*x[1-9][0-9]*", size):
        size = size.split(sep='x')
        size = [int(i) for i in size]
    else:
        size = (2048, 2048)
    
    # randomize
    if random and random==1:
        shuffle(images)
        
    print(images)
    print(len(images))
    
    img = create_img(images, size)
    return serve_pil_image(img)
    

if __name__ == '__main__':
    app.run()