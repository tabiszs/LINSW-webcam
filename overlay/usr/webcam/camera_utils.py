"""TBW."""
from datetime import datetime
from io import BytesIO
import logging
import os
from time import sleep

import numpy as np
from PIL import Image
import cv2

logger = logging.getLogger(__name__)

def convert_raw_image(raw):
    """TBW."""
    data = cv2.cvtColor(raw, cv2.COLOR_BGR2RGB)
    im = Image.fromarray(data)

    mem_file = BytesIO()
    im.save(mem_file, 'JPEG')
    return mem_file.getvalue()


class SimCam:
    """TBW."""

    counter = 0
    colors = [0.5, 0.75, 1.0]

    @staticmethod
    def simulate_image(w, h, dtype='uint16', shift=0, rgb=False):
        """Generate a 2d array of concentric circles.

        :param int w: the width in pixels
        :param int h: the height in pixels.
        :param str dtype: the pixel value data type
        :param int shift: the number of pixels to shift the final image.
        :param bool rgb: return a RGB (color) array.
        :return: a 2d numpy array of type uint8
        :rtype: ndarray
        """
        dx = 20.0 / w
        dy = 20.0 / h
        x = np.arange(-10, 10, dx)
        y = np.arange(-10, 10, dy)
        xx, yy = np.meshgrid(x, y, sparse=True)
        z = np.sin(xx ** 2 + yy ** 2) / (xx ** 2 + yy ** 2)
        z = np.nan_to_num(z)
        if z.min() < 0:
            z -= z.min()
        if dtype == 'uint16':
            z = (z / z.max()) * ((1 << 12) - 1)
        elif dtype == 'uint8':
            z = (z / z.max()) * ((1 << 8) - 1)
        z = z.astype(dtype)
        if shift > 0:
            z = np.roll(z, shift, axis=1)

        if rgb:
            SimCam.colors = np.array(SimCam.colors)
            SimCam.colors += 0.025
            SimCam.colors %= 1.0
            r = (z.astype(float) * SimCam.colors[0]).astype(dtype)
            g = (z.astype(float) * SimCam.colors[1]).astype(dtype)
            b = (z.astype(float) * SimCam.colors[2]).astype(dtype)
            return np.dstack((r, g, b))
        else:
            return z

    def read(self):
        """TBW."""
        SimCam.counter += 1
        data = SimCam.simulate_image(640, 480,
                                     dtype='uint8',
                                     shift=SimCam.counter,
                                     rgb=True)
        return True, data

    def read_image(self):
        """TBW."""
        ok, raw = self.read()
        return convert_raw_image(raw)


class WebCam(cv2.VideoCapture):
    """TBW."""
    def __init__(self, prop_id=0):
        """TBW."""
        logger.info('camera init')
        self._id = prop_id        
        super().__init__()

    def open(self):
        """ST."""
        logger.info('camera open')
        super().open(self._id)

    def release(self):
        """ST."""
        logger.info('camera release')
        super().release()

    def read(self):
        """TBW."""
        return super().read()

    def read_image(self):
        """TBW."""
        ok, raw = self.read()
        return convert_raw_image(raw)

    def save_image(self, path):
        ret, raw = self.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            pass

        data = cv2.cvtColor(raw, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(data)
        
        date = datetime.now()
        filename = f'image_{date}.jpg'
        pathname = f'{path}/{filename}'
        im.save(pathname, 'JPEG')
        return filename


class UsbCamera(object):

    """ Init camera """
    def __init__(self):
        # select first video device in system
        self.cam = cv2.VideoCapture('/dev/video2')
        # set camera resolution
        self.w = 800
        self.h = 600
        # set crop factor
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.h)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.w)

    def set_resolution(self, new_w, new_h):
        """
        functionality: Change camera resolution
        inputs: new_w, new_h - with and height of picture, must be int
        returns: None ore raise exception
        """
        if isinstance(new_h, int) and isinstance(new_w, int):
            # check if args are int and correct
            if (new_w <= 800) and (new_h <= 600) and \
               (new_w > 0) and (new_h > 0):
                self.h = new_h
                self.w = new_w
            else:
                # bad params
                raise Exception('Bad resolution')
        else:
            # bad params
            raise Exception('Not int value')

    def get_image(self):
        """
        functionality: Gets frame from camera.
        :return: frame
        """
        success, image = self.cam.read()
        if success:
            # scale image
            image = cv2.resize(image, (self.w, self.h))
        else:
            image = np.zeros((self.h, self.w, 3), np.uint8)
            cv2.putText(image, 'No camera', (40, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
        return image

    def get_frame(self):
        image = self.get_image()
        # encoding picture to jpeg
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def save_image(self):
        image = self.get_image()
        date = datetime.now()
        filename = './image_{}.jpg'
        cv2.imwrite(filename.format(date), image)
        return filename.format(date)

if __name__ == "__main__":
    cam = WebCam()
    cam.open()
    path2 = os.path.dirname(os.path.realpath(__file__)) + '/../photos'
    pathname=cam.save_image(path2)
    print(pathname)
    for i in range(100):
        cam.read_image()    
    cam.release()
    print('sleep')
    sleep(2)
    