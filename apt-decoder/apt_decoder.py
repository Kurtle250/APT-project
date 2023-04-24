import scipy.io.wavfile as wav
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

class apt_decoder(object):
    # DSP parameters
    fs, data = None,list()
    data_crop = None
    data_ = None
    resample = 4
    # image parameters
    image = None
    def __init__(self,file_handle):
        self.fs, self.data = wav.read(file_handle)
        self.data_crop = self.data[20 * self.fs:21 * self.fs]
        self.data = self.data[::self.resample]
        self.fs = self.fs // self.resample
        self.hilbert()
        self.frame_image()

    def display_plot(self):
        plt.figure(figsize=(12, 4))
        plt.plot(self.data_crop)
        plt.xlabel("Samples")
        plt.ylabel("Amplitude")
        plt.title("Signal")
        plt.show()


    def hilbert(self):
        analytical_signal = signal.hilbert(self.data)
        amplitude_envelope = np.abs(analytical_signal)
        self.data = amplitude_envelope


    def frame_image(self):
        frame_width = int(0.5 * self.fs)
        w, h = frame_width, self.data.shape[0] // frame_width
        self.image = Image.new('RGB', (w, h))
        px, py = 0, 0
        for p in range(self.data.shape[0]):
            lum = int(self.data[p] // 32 - 32)
            if lum < 0: lum = 0
            if lum > 255: lum = 255
            self.image.putpixel((px, py), (0, lum, 0))
            px += 1
            if px >= w:
                if (py % 50) == 0:
                    print(f"Line saved {py} of {h}")
                px = 0
                py += 1
                if py >= h:
                    break

    def display_image(self):
        plt.imshow(self.image)
        plt.show()