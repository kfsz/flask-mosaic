from flask import Flask, render_template, abort, request, jsonify, send_file
from PIL import Image
from io import BytesIO, StringIO
import requests
import math
# dunno if re should be used
import re

# ' to " later
# https://stackoverflow.com/questions/38421160/combine-multiple-different-images-from-a-directory-into-a-canvas-sized-3x6
# hmmmmmmmmmmmmmmmmmmmm
app = Flask(__name__)


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
    
    # total size is fucked up, as it assumes horizontal == vertical - FIX
    total_size = size[0] * size[1]
    total_size = total_size/image_number
    total_size = int(math.sqrt(total_size))
    
    horizontal_change = total_size
    vertical_change = total_size
    print("horizontal_change " + str(horizontal_change))
    print("vertical_change " + str(vertical_change))
    
    for i in range(0, size[0], horizontal_change):
        for j in range(0, size[1], vertical_change):
            # check if out of bounds - shouldn't be needed - remove
            if j + vertical_change > size[1]:
                pass
            try:
                filepath = img_loc.pop(0)
            except IndexError:
                break
            response = requests.get(filepath)
            img = Image.open(BytesIO(response.content))
            img = img.resize((horizontal_change, vertical_change), Image.ANTIALIAS)
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
    
    print(images)
    print(len(images))
    
    img = create_img(images, size)
    return serve_pil_image(img)
    

if __name__ == '__main__':
    app.run()