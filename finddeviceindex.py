import pyaudio
p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

p.get_device_info_by_index(2)

for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print( "Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

device_info = p.get_device_info_by_index(2)
print(device_info)


