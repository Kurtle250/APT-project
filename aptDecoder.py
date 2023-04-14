#!/usr/bin/python3

import scipy.io.wavfile as wav
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import json
from aptDbSchema import apt_data

class AptDecoder(apt_data):
    # DSP parameters
    fs, data = None, list()
    data_crop = None
    resample = 1
    # image parameters
    img = None
    img_fh = str()
    wav_fh = str()
    json_output = None

    def __init__(self, wav_fh):
        self.wav_fh = wav_fh
        self.fs, self.data = wav.read(wav_fh)
        self.data_crop = self.data[20 * self.fs:21 * self.fs]
        # self.data = self.data[::self.resample]
        # self.fs = self.fs // self.resample
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
        self.data = self.data[:w * h] // 32 - 32
        self.data = np.reshape(self.data, (h, w))
        self.img = Image.fromarray(self.data)
        print(f"finished decoding {self.wav_fh} ")
        self.img = self.img.resize((w, 3*h))
        plt.imshow(self.img)
        self._save_image()
    def display_image(self) -> None:
        """
        Display's image in matplot lib figure
        :return: None
        """
        plt.show()

    def _save_image(self) -> None:
        """
        Save matplot figure as png
        :return: None
        """
        self.img_fh = "data/images/"+self.wav_fh.split('/')[2].split('.')[0]+".png"
        plt.savefig(self.img_fh)

    def generate_json(self):
        """
        Generating json output, which will be used for passing to db
        :return: Json formatted apt schema for passing to db
        """
        self.json_output = apt_data("2", "HHMMSS", ["XXXX", "XXXX", "XXXX"], "...", self.wav_fh, self.img_fh)
        return json.dumps(self.json_output.aptSchema)
