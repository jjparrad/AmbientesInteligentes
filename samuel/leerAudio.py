import pyaudio # Para leer con microfono
import wave # Para producir wavs
import msvcrt # Para el input de salida
import sys
sys.path.insert(1, 'clasificador') # insert at 1, 0 is the script path (or '' in REPL)
import hallarVariablesUnico as clasificador
import hallarVariablesMulti as clasificadorMulti
sys.path.insert(1, 'reconocedor') # ESTO ES PARA ENTRAR EN UNA CARPETA CON EL IMPORT
import machineLearning as reconocedor
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



print("Abriendo microfono. Oprimir cualquier tecla para salir")
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

    # ACA TOCA PONER LA PARTE DEL CODIGO QUE LEE WAVs
    # LO DE METER EL WAV QUE SE ACABA DE GENERAR EN EL MODELO
    # predecir(filename)
    excel_file = clasificador.hallarVariables(filename)
    excel_file += '.xlsx'
    reconocedor.predecir(excel_file)

    print("Segmento " + str(segmento) + " grabado correctamente")
    segmento += 1

stream.stop_stream()
stream.close()
p.terminate()