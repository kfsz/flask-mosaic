import pytest

from main import *

class TestImage(object):

    test_image_url = "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"
    test_default_size = (2048, 2048)
    
    image = create_mosaic([test_image_url], test_default_size)
    image_diffrent_size = create_mosaic([test_image_url], (1000, 9999))
    image_double = create_mosaic([test_image_url, test_image_url], test_default_size)
    
    def test_existence(self):
        assert self.image
        
    def test_size(self):    
        assert self.image.size == self.test_default_size
        
    def test_size_change(self):    
        assert self.image_diffrent_size.size == (1000, 9999)       
        
    def test_image_diffrence(self):
        assert self.image_double != self.image
        
    def test_no_url(self):
        with pytest.raises(Exception):
            image = create_mosaic([], test_default_size)
            
    def test_not_url(self):
        with pytest.raises(Exception):
            image = create_mosaic(["no_url_here"], test_default_size)
            
    def test_no_size(self):
        with pytest.raises(Exception):
            image = create_mosaic(test_image_url)
            