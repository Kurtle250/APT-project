#!/usr/bin/python3

import scipy.io.wavfile as wav
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import json
from apt_dataclass import apt_dataclass

class AptDecoder(apt_dataclass):
    # DSP parameters
    fs, data = None, list()
    data_crop = None
    resample = 4
    # image parameters
    img = None
    img_fh = str()
    wav_fh = str()
    json_output = None

    def __init__(self, wav_fh):
        self.wav_fh = wav_fh
        self.fs, self.data = wav.read(wav_fh)
        self.data_crop = self.data[20 * self.fs:21 * self.fs]
        self.data = self.data[::self.resample]
        self.fs = self.fs // self.resample
        self._hilbert()
        self._frame_image()

    def display_plot(self) -> None:
        """
        Displays plot of sampled audio signal
        :return: None
        """
        plt.figure(figsize=(12, 4))
        plt.plot(self.data_crop)
        plt.xlabel("Samples")
        plt.ylabel("Amplitude")
        plt.title("Signal")
        plt.show()

    def _hilbert(self) -> None:
        """
        Preforms hilbert filter on AM modulated signal to demodulate the signal
        to be further decoded and processed
        :return: None
        """
        analytical_signal = signal.hilbert(self.data)
        amplitude_envelope = np.abs(analytical_signal)
        self.data = amplitude_envelope

    def _frame_image(self) -> None:
        """
        Transforms 1D np array in 2D image
        :return: None
        """
        frame_width = int(0.5 * self.fs)
        w, h = frame_width, self.data.shape[0] // frame_width
        self.img = Image.new('RGB', (w, h))
        px, py = 0, 0
        for p in range(self.data.shape[0]):
            lum = int(self.data[p] // 32 - 32)
            if lum < 0:
                lum = 0
            if lum > 255:
                lum = 255
            self.img.putpixel((px, py), (lum, lum, lum))
            px += 1
            if px >= w:
                if (py % 50) == 0:
                    print(f"Line saved {py} of {h}")
                px = 0
                py += 1
                if py >= h:
                    break

    def display_image(self) -> None:
        """
        Display's image in matplot lib figure
        :return: None
        """
        plt.imshow(self.img)
        plt.show()

    def save_image(self, id: int) -> None:
        """
        Save matplot figure as png
        :return: None
        """
        self.img_fh = "data/images/"+str(id) + '-' + 'NOAA-19.png'
        plt.savefig(self.img_fh)

    def parse_wav_fh(self):
        pass
    def generate_json(self):
        self.json_output = apt_dataclass("2", "HHMMSS", ["XXXX", "XXXX", "XXXX"], "...", self.wav_fh, self.img_fh)
        print(json.dumps(self.json_output.aptSchema))
