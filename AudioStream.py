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
       # self.init_plots()

    def init_plots(self):
        # x variables for plotting
        x = np.arange(0, 2 * self.CHUNK, 2)
        xf = np.linspace(0, self.RATE, self.CHUNK)

        # create matplotlib figure and axes
        self.fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))


        # create a line object with random data
        self.line, = ax1.plot(x, np.random.rand(self.CHUNK), '-', lw=2)

        
        # format waveform axes
        ax1.set_title('AUDIO WAVEFORM')
        ax1.set_xlabel('samples')
        ax1.set_ylabel('volume')

        plt.setp(
            ax1, yticks=[0, 128, 255],
            xticks=[0, self.CHUNK, 2 * self.CHUNK],
        )
        plt.setp(ax2, yticks=[0, 1], )

        # format spectrum axes
        ax2.set_xlim(20, self.RATE / 2)





if __name__ == '__main__':
    mystream = AudioStream()


    fig, ax = plt.subplots()
    x = np.arange(0, 2 * mystream.CHUNK, 2)
    line, = ax.plot(x, np.random.rand(mystream.CHUNK))
    ax.set_ylim(0, 255)
    ax.set_xlim(0, 2 * mystream.CHUNK)
    plt.show(block=False)
    while True:
        data = mystream.stream.read(mystream.CHUNK)
        data_int = np.array(struct.unpack(str(2 * mystream.CHUNK) + 'B', data), dtype='b')[::2] + 128
        line.set_ydata(data_int)
        fig.canvas.draw()
        fig.canvas.flush_events()






