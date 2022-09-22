import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import librosa
import librosa.display
import scipy
from scipy import fftpack
from scipy import signal
from sklearn.tree import DecisionTreeClassifier  # Import Decision Tree Classifier
# Import train_test_split function
from sklearn.model_selection import train_test_split
# Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics
import csv


audio_data = "/home/benjas/Documents/IoT/IAE/audios_recording_01b.wav"

data_raw,  sample_rate = librosa.load(audio_data)
print(f'Sample frequency:{sample_rate} Hz')

Ts = 1/sample_rate
N = data_raw.shape[0]  # Numero de muestras
t = np.arange(0, Ts*N, Ts)  # Vector de tiempos

plt.figure(figsize=(14, 5))
librosa.display.waveshow(data_raw, sr=sample_rate)

data = data_raw.astype(np.float32)
plt.show()

# Normalization
data = (data - data.min())
data = data / (data.max() - data.min())
data = 2 * (data - data.mean())

# Fast Fourier Transforms
# Sample rate generation
sample_freq = fftpack.fftfreq(data.size, d=Ts)

# Calculate the fft
signal_fft = fftpack.fft(data)

idx = np.where(sample_freq >= 0)

freqs = sample_freq[idx]

power = np.abs(signal_fft)[idx]

plt.figure(figsize=(14, 5))
plt.plot(freqs, power)
plt.ylabel('Power', fontsize=14)
plt.xlabel('Frequency [Hz]', fontsize=14)
plt.show()

# Filters
# 4 KHZ

# Nyquist frecuency
f_nyq = sample_rate/2

# Butterworth
wp = 2000


# wp band pass  [Hz] ws = band stop gpass = attenuation in pass band [dB] gstop = attenuation in stop band [dB]
order, wn = scipy.signal.buttord(
    wp=2000, ws=2500, gpass=3, gstop=40, analog=False, fs=sample_rate)

# Filter design
b, a = scipy.signal.butter(order, wn, btype='lowpass',
                           analog=False, fs=sample_rate)

# Signal filter
data_filt_2k = scipy.signal.lfilter(b, a, data)

# with open('decisionTree.csv', 'w') as f:
#writer = csv.writer(f)
#writer.writerows(map(lambda x: [x], data_filt_2k))


# Tree decision
