#!/usr/bin/python3

import scipy.io.wavfile as wav
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import json
from database.db.aptDbSchema import apt_data

class AptDecoder(apt_data):
    # DSP parameters
    fs, data = None, list()

    resample = 1
    # image parameters
    img = None
    img_fh = str()
    wav_fh = str()
    json_output = None

    def __init__(self, wav_fh):
        self.wav_fh = wav_fh
        self.fs, self.data = wav.read(wav_fh)
        self.data = self.data[::2]
        self.fs = self.fs/2
        #self._filter_data()
        self._hilbert()
        self._frame_image()

    def _filter_data(self,fc):
        # Low-Pass Filter
        taps = signal.firwin(numtaps=101, cutoff=fc, fs=self.fs)
        self.data = np.convolve(signal[:, 0], taps, 'valid')
        self.data = self.data[::2]
        self.fs = self.fs/2
    def display_plot(self,data_crop) -> None:
        """
        Displays plot of sampled audio signal
        :return: None
        """
        plt.figure(figsize=(12, 4))
        plt.plot(data_crop)
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
        self.data = (amplitude_envelope/max(amplitude_envelope))*255
    def _frame_image(self) -> None:
        """
        Transforms 1D np array in 2D image
        :return: None
        """
        self.data = self.data[2350:]
        frame_width = int(0.5 * self.fs)
        w, h = frame_width, self.data.shape[0] // frame_width
        self.data = self.data[:w * h]
        self.data = np.reshape(self.data, (h, w))
        self.data = self.data.astype(np.uint8)
        self.img = Image.fromarray(self.data)
        print(f"finished decoding {self.wav_fh} ")
        self.img = self.img.resize((2*w, 3*h))
        self._save_image()

    def display_image(self) -> None:
        """
        Display's image in matplot lib figure
        :return: None
        """
        plt.imshow(self.img)
        plt.show()

    def _save_image(self) -> None:
        """
        Save matplot figure as png
        :return: None
        """
        self.img_fh = "data/images/"+self.wav_fh.split('/')[2].split('.')[0]+".png"
        print(self.img_fh)
        self.img.save(self.img_fh)

    def generate_json(self):
        """
        Generating json output, which will be used for passing to db
        :return: Json formatted apt schema for passing to db
        """
        self.json_output = apt_data("2", "HHMMSS", ["XXXX", "XXXX", "XXXX"], "...", self.wav_fh, self.img_fh)
        return json.dumps(self.json_output.aptSchema)
