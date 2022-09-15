import matplotlib.pyplot as plt
import numpy as np
import wave
from scipy.signal import hilbert

FRAME_SIZE = 1024
HOP_LENGTH = 512

wave_obj = wave.open(
    "/home/benjas/Documents/IoT/IAE/audios_recording_01b.wav", "rb")

# Samples frequency
sample_freq = wave_obj.getframerate()
print(sample_freq)

# Number samples
n_samples = wave_obj.getnframes()
print(n_samples)

# Time of audio
t_audio = n_samples/sample_freq
print(t_audio)

# Number of channels
n_channels = wave_obj.getnchannels()
# print(n_channels)

# Signal wave
signal_wave = wave_obj.readframes(n_samples)

signal_array = np.frombuffer(signal_wave, dtype=np.int16)
#signal_final = np.abs(signal_array)
signal_final = signal_array.astype(np.float)**2
print(signal_final)

# Time at which each sample is taken
times = np.linspace(0, n_samples/sample_freq, num=n_samples)
# print(times)

analytic_signal = hilbert(signal_array)
amplitude_envelope_signal = np.abs(analytic_signal)


def amplitude_envelope(signal, frame_size, hop_length):
    amp_envelope = []

    # Calculate AE for eac frame
    for i in range(0, len(signal), hop_length):
        current_frame_amplitude_envelope = max(signal[i:i+frame_size])
        amp_envelope.append(current_frame_amplitude_envelope)
    return np.array(amp_envelope)


ae_signal = amplitude_envelope(signal_array, FRAME_SIZE, HOP_LENGTH)

plt.figure(figsize=(15, 5))
#plt.plot(times, ae_signal)
plt.plot(ae_signal)
plt.ylabel('Signal value')
plt.xlabel('Times (s)')
plt.xlim(0, t_audio)
plt.show()
