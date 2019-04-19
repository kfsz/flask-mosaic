# flask-mosaic

App creates mosaic based on images supplied from urls.  
  
Basic endpoint -
`http://127.0.0.1:5000/mozaika`
  
Available parameters - as specified by task  

Example usage -
`http://127.0.0.1:5000/mozaika?losowo=1&&rozdzielczosc=1400x1200&&zdjecia=https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/StSophiaChurch-Sofia-10.jpg/640px-StSophiaChurch-Sofia-10.jpg,https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Old_house_-_Sofia_-_2.jpg/530px-Old_house_-_Sofia_-_2.jpg,https://upload.wikimedia.org/wikipedia/commons/c/ce/Mladost3.jpg,https://upload.wikimedia.org/wikipedia/commons/c/cb/Borisova_gradina_autumn.jpg,https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Independence_Square_(23997057638).jpg/640px-Independence_Square_(23997057638).jpg,https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Sofia_(15326483440).jpg/640px-Sofia_(15326483440).jpg,https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Sofia_(37536243674).jpg/562px-Sofia_(37536243674).jpg`

## Installation

#### Create and activate virtual enviroment

#### Install required packages
`pip install -r requirements.txt`

### Run tests
`pytest`

### Run the app
`python main.py`



