import numpy as np
import struct
from scipy.ndimage.filters import maximum_filter
import sys
import time
import madmom
import pyaudio
from madmom.audio.signal import Stream

FRAME_SIZE = 2048
HOP_SIZE = 441
FPS = None
NUM_FRAMES = None
DEVICE_INDEX = 2
SAMPLE_RATE = 44100
NUM_CHANNELS = 1
DTYPE = np.float32

class Stream(madmom.audio.signal.Stream):
    def __int__(self,
                sample_rate=SAMPLE_RATE,
                num_channels=NUM_CHANNELS,
                dtype=DTYPE,
                input_device_index = DEVICE_INDEX,
                frame_size=FRAME_SIZE,
                hop_size=HOP_SIZE,
                fps=FPS):

        # set attributes
        self.sample_rate = sample_rate
        self.num_channels = 1 if None else num_channels
        self.dtype = dtype
        self.input_device_index = input_device_index
        if frame_size:
            self.frame_size = int(frame_size)
        if fps:
            # use fps instead of hop_size
            hop_size = self.sample_rate / float(fps)
        if int(hop_size) != hop_size:
            raise ValueError(
                'only integer `hop_size` supported, not %s' % hop_size)
        self.hop_size = int(hop_size)
        # init PyAudio
        self.pa = pyaudio.PyAudio()
        # init a stream to read audio samples from
        self.stream = self.pa.open(rate=self.sample_rate,
                                   channels=self.num_channels,
                                   format=pyaudio.paFloat32,
                                   input=True,
                                   input_device_index = self.input_device_index,
                                   frames_per_buffer=self.hop_size,
                                   start=True)
        # create a buffer
        self.buffer = madmom.audio.signal.BufferProcessor(self.frame_size)
        # frame index counter
        self.frame_idx = 0
        # PyAudio flags
        self.paComplete = pyaudio.paComplete
        self.paContinue = pyaudio.paContinue


if __name__ == '__main__':
    stream = Stream(sample_rate= 32000,
                    num_channels= 1,
                    input_device_index=2)

    proc = madmom.audio.signal.FramedSignalProcessor(origin='stream')
    while True:
        data = stream.next()
        fs = proc.process(data)
        spec = madmom.audio.spectrogram.Spectrogram(fs)
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



