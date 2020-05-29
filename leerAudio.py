import pyaudio
import wave

# Esta variable determina el número de archivos de 4segs que se van a generar
NUM_WAVS = 3

# Estas variables de abajo es mejor dejarlas quietas
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)


for segmento in range(0, NUM_WAVS):
    print("Grabando segmento " + str(segmento))

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    wf = wave.open(WAVE_OUTPUT_FILENAME + str(segmento) + '.wav', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    # ACÁ TOCA PONER LA PARTE DEL CÓDIGO QUE LEE WAVs
    # LO DE METER EL WAV QUE SE ACABA DE GENERAR EN EL MODELO

    print("Segmento " + str(segmento) + " grabado correctamente")

stream.stop_stream()
stream.close()
p.terminate()