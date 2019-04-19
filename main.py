from flask import Flask, abort, request, send_file
from PIL import Image
from io import BytesIO
from random import shuffle
import requests
import re

app = Flask(__name__)


def create_mosaic(image_locations, size):
    """Create mosaic using images from given urls and size."""
    # create empty image
    mozaic = Image.new("RGB", size, "black")

    image_number = len(image_locations)
    odd_image = False

    # basic mosaic layout creation
    if image_number >= 3:
        columns = image_number // 2
        rows = 2
        if image_number % 2 == 1:
            odd_image = True
    else:
        columns = image_number
        rows = 1

    # switch columns with rows (image placement) depending
    # on wherever is more free space available
    if size[1] > size[0]:
        columns, rows = (rows, columns)

    # size for individual images
    horizontal_length = size[0] // columns
    vertical_length = size[1] // rows

    # adjust image size for images
    # when mozaic has odd number of images
    if odd_image:
        if horizontal_length > vertical_length:
            horizontal_length = size[0] // (columns + 1)
            columns += 1
        else:
            vertical_length = size[1] // (rows + 1)
            rows += 1

    current = 0
    current_column = 0

    for i in range(0, size[0], horizontal_length):

        current_column += 1
        for j in range(0, size[1], vertical_length):

            # check if out of bounds
            if j + vertical_length > size[1]:
                break

            # get next url
            try:
                file_url = image_locations.pop(0)
            except IndexError:
                break

            # load and open image
            try:
                response = requests.get(file_url)
                img = Image.open(BytesIO(response.content))
            except:
                raise

            current += 1

            # resize images based on free space available
            if odd_image and current == image_number and horizontal_length > vertical_length:
                img = img.resize((horizontal_length, vertical_length * 2), Image.ANTIALIAS)
            elif current_column == columns - 1 and (
                (horizontal_length <= vertical_length and current + rows > image_number)
                or current + rows > image_number + 1
            ):  # last one is special case for 7 pic mosaic
                # with stretched last image and still empty space at the bottom
                img = img.resize((horizontal_length * 2, vertical_length), Image.ANTIALIAS)
            else:
                img = img.resize((horizontal_length, vertical_length), Image.ANTIALIAS)
            mozaic.paste(img, (i, j))

    return mozaic


def serve_pil_image(pil_img):
    """Send image from Flask."""
    # write and send image
    img_io = BytesIO()
    pil_img.save(img_io, "JPEG", quality=90)
    img_io.seek(0)
    return send_file(img_io, mimetype="image/jpeg")


@app.route("/mozaika", methods=["GET"])
def mosaic():
    """Basic endpoint for getting mosaic image."""
    # get parameters
    random = request.args.get("losowo")
    size = request.args.get("rozdzielczosc")
    images = request.args.get("zdjecia")

    # check if number of supplied images is correct
    if images:
        images = images.split(sep=",")
        if len(images) > 8:
            return abort(400)
    else:
        return abort(400)

    # size validation and processing
    if size and re.match(r"[1-9][0-9]*x[1-9][0-9]*", size):
        size = size.split(sep="x")
        size = [int(i) for i in size]
    else:
        size = (2048, 2048)

    # randomize
    if random and random == str(1):
        shuffle(images)

    # create mosaic, abort if urls were not valid
    try:
        mosaic = create_mosaic(images, size)
    except:
        return abort(400)

    return serve_pil_image(mosaic)


if __name__ == "__main__":
    app.run()
