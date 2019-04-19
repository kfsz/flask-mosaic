import pytest

from main import *

class TestWebApp():

    app = app.test_client()
    
    test_image_url = "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"
    test_default_size = (2048, 2048)
    
    def to_string(self, size):
        return str(size[0]) + "x" + str(size[1])
     
    def test_main(self):
        response = self.app.get('/')
        assert response.status_code == 404
        
    def test_no_image(self):
        response = self.app.get('/mozaika')
        assert response.status_code == 400
        
    def test_basic_request(self):
        response = self.app.get('/mozaika?' + "zdjecia=" + self.test_image_url)
        assert response.status_code == 200
        
    def test_wrong_url(self):
        response = self.app.get('/mozaika?' + "zdjecia=" + "not_a_url")
        assert response.status_code == 400
        
    def test_no_url(self):
        response = self.app.get('/mozaika?' + "zdjecia=")
        assert response.status_code == 400
        
    def test_too_many_urls(self):
        request = "zdjecia="
        for i in range(10):
            request += self.test_image_url + "&&"
        response = self.app.get('/mozaika?' + "request")
        assert response.status_code == 400
        
    def test_accept_random(self):
        response = self.app.get('/mozaika?' + "zdjecia=" + self.test_image_url + "&&losowe=1")
        assert response.status_code == 200

    def test_accept_size(self):
        response = self.app.get('/mozaika?' + "zdjecia=" + self.test_image_url + "&&rozdzielczosc=1920x1080")
        assert response.status_code == 200 
    
    def test_return_image(self):
        response = self.app.get('/mozaika?' + "zdjecia=" + self.test_image_url)
        img = Image.open(BytesIO(response.data))        
        assert img
        
    def test_image_default_size(self):
        response = self.app.get('/mozaika?' + "zdjecia=" + self.test_image_url)
        img = Image.open(BytesIO(response.data))        
        assert img.size == self.test_default_size
        
    def test_image_changed_size(self):
        size = (1000, 1000)
        response = self.app.get('/mozaika?' + "zdjecia=" + self.test_image_url + "&&rozdzielczosc=" + self.to_string(size))
        img = Image.open(BytesIO(response.data))        
        assert img.size == size
        
    def test_wrong_size_diregard(self):
        response = self.app.get('/mozaika?' + "zdjecia=" + self.test_image_url + "&&rozdzielczosc=1920*1080")
        img = Image.open(BytesIO(response.data))        
        assert img.size == self.test_default_size
    