import matplotlib.pyplot as plt
import numpy as np
import pyaudio
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import struct
from scipy.fftpack import fft
import sys
import time
import madmom

from madmom.audio.signal import Stream


class AudioStream(object):
    def __init__(self):

        # stream constants
        self.CHUNK = 1024 * 2
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.pause = False

        # stream object
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            output=True,
            frames_per_buffer=self.CHUNK,
        )


if __name__ == '__main__':
    stream = Stream(sample_rate=44100,
                    num_channels=1,
                    frame_size=1024*2
                    )
    proc = madmom.audio.signal.FramedSignalProcessor(origin='stream')
    data = stream.next()
    fs = proc.process(data)
    spec = madmom.audio.spectrogram.Spectrogram(fs, frame_size=2048, hop_size=200, fft_size=4096)

    plt.imshow(spec[:, :200].T, aspect='auto', origin='lower')

    plt.show()

    while True:
        spec = madmom.audio.spectrogram.Spectrogram(fs, frame_size=2048, hop_size=200, fft_size=4096)

        plt.imshow(spec[:, :200].T, aspect='auto', origin='lower')

