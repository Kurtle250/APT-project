#!/usr/bin/python3
from dataclasses import dataclass
import scipy.io.wavfile as wav
import scipy.signal as signal
import numpy as np

class SignalProcessing:
    wav_fh: str

    def __init__(self, wav_fh):
        self.data = list()
        self.AM_signal = list()
        SignalProcessing.wav_fh = wav_fh
        self.sample_rate, self.IF_signal = self.read_wav_file(wav_fh)

    def resample(self, decimation=2):
        self.sample_rate = self.sample_rate*(20/53)
        self.data = signal.resample_poly(self.data, 53, 20)

    def check_sampling_rate(self, target_freq: int):
        if(self.sample_rate >= 2*target_freq):
            print("pass nyquist rate ")
        else:
            print("fails nyquist rate and requires interpolation")

    def check_mono_channel(self):
        pass
    def read_wav_file(self, wav_fh) -> None:
        return wav.read(wav_fh)

    def filter_data(self, cutoff_freq: int):
        """
        Preforms Low pass filter on  signal
        :return: None
        """
        # Low-Pass Filter
        taps = signal.firwin(numtaps=101, cutoff=cutoff_freq, fs=self.sample_rate)
        self.data = np.convolve(signal, taps, 'valid')
    def hilbert(self) -> None:
        """
        Preforms hilbert filter on AM modulated signal to demodulate the signal
        to be further decoded and processed
        :return: None
        """
        analytical_signal = signal.hilbert(self.IF_signal)
        self.AM_signal = np.abs(analytical_signal)


    def quantize_signal(self, plow=0.5, phigh=99.5):
        '''
        Convert signal to numbers between 0 and 255.
        '''
        (low, high) = np.percentile(self.AM_signal, (plow, phigh))
        delta = high - low
        data = np.round(255 * (self.AM_signal - low) / delta)
        data[data < 0] = 0
        data[data > 255] = 255
        self.data = data.astype(np.uint8)