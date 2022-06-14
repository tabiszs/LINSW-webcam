from datetime import datetime
from io import BytesIO
import logging
import os
from time import sleep

import numpy as np
from PIL import Image

logger = logging.getLogger(__name__)
image_dir = os.path.dirname(os.path.realpath(__file__)) + '/image'

# for i in range(10): # do forever
#     date = datetime.now()
#     path = f'/home/stas/Desktop/LINSW/ex4/tornado-image-streamer/overlay/usr/webcam/image/{date}.jpg'
#     os.system(f'fswebcam --no-banner --jpeg 80 --save {path}')
#     #os.system(f'fswebcam -S 3 --jpeg 80 --save {path}') # uses Fswebcam to take picture
#     #time.sleep(15) # this line creates a 15 second delay before repeating the loop

def convert_raw_image(pathname):
    """TBW."""    
    mem_file = BytesIO()
    im = Image.open(pathname)
    im.save(mem_file, 'JPEG')
    return mem_file.getvalue()

class WebCam:

    def open(self):
        """ST."""
        self._open = True
        logger.info('camera open')

    def release(self):
        """ST."""
        self._open = False
        logger.info('camera release')
    def isOpened(self):
        return self.open

    def read_image(self):
        """TBW."""
        filename = f'tmp.jpg'
        pathname = f'{image_dir}/{filename}'
        os.system(f'fswebcam --no-banner --jpeg 80 --save {pathname}')
        return convert_raw_image(pathname)

    def save_image(self, path):        
        date = datetime.now()
        format = f'{date.year}-{date.month}-{date.day}_{date.hour}:{date.minute}:{date.second}.{date.microsecond}'
        filename = f'img_{format}.jpg'
        pathname = f'{path}/{filename}'
        os.system(f'fswebcam --jpeg 80 --save {pathname}')
        return filename
