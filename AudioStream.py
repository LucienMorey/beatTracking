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





'''stream = Stream(sample_rate=44100,
                num_channels=1,
                frame_size=1024*2,
                queue_size=3
                )'''
pa = pyaudio.PyAudio()
stream= pa.open(rate = 44100,
                channels = 1,
                format = pyaudio.paFloat32,
                input = True,
                frames_per_buffer = 2048,
                input_device_index=6)
proc = madmom.audio.signal.FramedSignalProcessor(origin='stream')
plt.show()
while True:
    data = stream.read(1024)
    data = np.fromstring(data ,'float32').astype(np.float32, copy=False)

    fs = madmom.audio.signal.FramedSignal(data, frame_size=2048, hop_size=441, )
    spec = madmom.audio.spectrogram.Spectrogram(fs, frame_size=2048, hop_size=441, fft_size=4096)
    sf = madmom.features.onsets.spectral_flux(spec)
    if sf[1]> 20:
        print(sf)
    '''filt_spec = madmom.audio.spectrogram.FilteredSpectrogram(spec,
                                                             filterbank=madmom.audio.filters.LogFilterbank,
                                                             num_bands=24)
    log_spec = madmom.audio.spectrogram.LogarithmicSpectrogram(filt_spec, add=1)

    size = (1, 3)
    max_spec = maximum_filter(log_spec, size=size)
    diff = np.zeros_like(log_spec)
    diff[1:] = (log_spec[1:] - max_spec[: -1])
    pos_diff = np.maximum(0, diff)
    superflux = np.sum(pos_diff, axis=1)
    print(superflux)'''



