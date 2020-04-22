import librosa as lb
import numpy as np

# Nombre del archivo
filepath = "00.wav"


# Sacar las samples del mp3 o wav
# Las samples son amplitud en tiempo

samples, sampling_rate = lb.load(filepath, sr=8000, mono=True, offset=0.0, duration=None)


def condensar_amplitud(x, y):
    data = []
    for amp in y:
        if amp > 0:
            data.append(amp)
    return np.mean(data)


amplitud = condensar_amplitud(samples[0], samples[1])
print("amplitud: ", amplitud)