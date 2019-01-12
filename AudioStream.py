import matplotlib.pyplot as plt
import numpy as np
import pyaudio
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import struct
from scipy.ndimage.filters import maximum_filter
import sys
import time
import madmom

from madmom.audio.signal import Stream





stream = Stream(sample_rate=44100,
                num_channels=1,
                frame_size=1024*2
                )
proc = madmom.audio.signal.FramedSignalProcessor(origin='stream')
while True:
    data = stream.next()
    fs = proc.process(data)
    spec = madmom.audio.spectrogram.Spectrogram(fs, frame_size=2048, hop_size=200, fft_size=4096)
    filt_spec = madmom.audio.spectrogram.FilteredSpectrogram(spec,
                                                             filterbank=madmom.audio.filters.LogFilterbank,
                                                             num_bands=24)
    log_spec = madmom.audio.spectrogram.LogarithmicSpectrogram(filt_spec, add=1)
    size = (1, 3)
    max_spec = maximum_filter(log_spec, size=size)
    diff = np.zeros_like(log_spec)
    diff[1:] = (log_spec[1:] - max_spec[: -1])
    pos_diff = np.maximum(0, diff)
    superflux = np.sum(pos_diff, axis=1)

    print(superflux)


