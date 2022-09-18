import matplotlib.pyplot as plt
import numpy as np
import librosa
import librosa.display
import scipy
from scipy import fftpack
from scipy import signal


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

# sample frequency of the filtered signal
sample_freq_filtered_signal = fftpack.fftfreq(data_filt_2k.size, d=Ts)

# Calculate the fft
signal_filt_2k_FFT = fftpack.fft(data_filt_2k)


idx_2K = np.where(sample_freq_filtered_signal >= 0)

freqs_2K = sample_freq_filtered_signal[idx_2K]

power_2K = np.abs(signal_filt_2k_FFT)[idx_2K]

plt.figure(figsize=(14, 5))
plt.plot(freqs_2K, power_2K)
plt.ylabel('Power', fontsize=14)
plt.xlabel('Frequency [Hz]', fontsize=14)
plt.show()

# Guardar el archivo de audio
scaled = np.int16(data_filt_2k/np.max(np.abs(data_filt_2k))*32767)
scipy.io.wavfile.write('filtered.wav', sample_rate, scaled)
