import pyaudio # Para leer con micrófono
import wave # Para producir wavs
import msvcrt # Para el input de salida

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



print("Abriendo micrófono. Oprimir cualquier tecla para salir")
segmento = 1
while(not msvcrt.kbhit()):
    print("Grabando segmento " + str(segmento))

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    filename = WAVE_OUTPUT_FILENAME + str(segmento) + '.wav'
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    # ACÁ TOCA PONER LA PARTE DEL CÓDIGO QUE LEE WAVs
    # LO DE METER EL WAV QUE SE ACABA DE GENERAR EN EL MODELO
    # predecir(filename)

    print("Segmento " + str(segmento) + " grabado correctamente")
    segmento += 1

stream.stop_stream()
stream.close()
p.terminate()