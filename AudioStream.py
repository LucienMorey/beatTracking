import matplotlib.pyplot as plt
import numpy as np
import pyaudio
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import struct
from scipy.fftpack import fft
import sys
import time


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
    mystream = AudioStream()
    fig, ax = plt.subplots()
    x = np.arange(0, 2 * mystream.CHUNK, 2)
    line, = ax.plot(x, np.random.rand(mystream.CHUNK))
    ax.set_ylim(0, 255)
    ax.set_xlim(0, 2 * mystream.CHUNK)
    fig.canvas.draw()
    plt.show(block=False)
    while True:
        data = mystream.stream.read(mystream.CHUNK)
        data_int = np.array(struct.unpack(str(2 * mystream.CHUNK) + 'B', data), dtype='b')[::2] + 128
        line.set_ydata(data_int)
        ax.draw_artist(ax.patch)
        ax.draw_artist(line)
        fig.canvas.flush_events()
