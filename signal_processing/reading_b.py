import matplotlib.pyplot as plt
import numpy as np
import wave
import sys


wave_obj = wave.open("/home/benjas/Documents/IoT/IAE/audios_recording_01b.wav", "rb")

#Samples frequency
sample_freq = wave_obj.getframerate()
print(sample_freq)

#Number samples
n_samples =  wave_obj.getnframes()
print(n_samples) 

#Time of audio
t_audio = n_samples/sample_freq
print(t_audio)

#Number of channels
n_channels = wave_obj.getnchannels()
print(n_channels)

#Signal wave
signal_wave = wave_obj.readframes(n_samples)

signal_array = np.frombuffer(signal_wave, dtype= np.int16)
print(signal_array)

#Time at which each sample is taken
times =  np.linspace(0, n_samples/sample_freq, num = n_samples)
#print(times)

plt.figure(figsize =(15,5))
plt.plot(times, signal_array)
plt.ylabel('Signal value')
plt.xlabel('Times (s)')
plt.xlim(0, t_audio)
plt.show()