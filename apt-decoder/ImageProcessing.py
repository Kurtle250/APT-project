import numpy as np
from PIL import Image
class ImageProcessing:
    RATE = 20800
    NOAA_LINE_LENGTH = 2080


    def __init__(self, data, sample_rate):
        # initial 1D decoded np.array of data
        self.data = data
        self.fs = sample_rate
        self.img = list()
        #
        self._frame_image()
        self.img.show()


    def _frame_image(self) -> None:
        """
        Transforms 1D np array in 2D image
        :return: None
        """
        #self.data = self.data[4700::]
        frame_width = int(self.fs)
        w, h = frame_width, self.data.shape[0] // frame_width
        self.data = self.data[:w * h]
        self.data = np.reshape(self.data, (h, w))
        self.img = Image.fromarray(self.data)
        self.img = self.img.resize((2*w, 3*h))