import pyaudio # Para leer con microfono
import wave # Para producir wavs
import msvcrt # Para el input de salida
import sys
import tkinter as tk
import threading

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

# Variables de control de la GUI
end = False

def openMic():
    if status.get() == "stopped":

        ##Empezar a grabar
        hiloRead = threading.Thread(target=read)
        hiloRead.start()

        status.set("processing")
        print("openMic()")

def closeMic():
    if status.get() == "processing":
        status.set("stopping")

        ##Parar de grabar
        hiloStop = threading.Thread(target=stop)
        hiloStop.start()
        print("closeMic()")


def read():
    p = pyaudio.PyAudio()
    global end
    end = False
    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

    print("Opening microphone")
    segmento = 1
    wavfile = 0
    while not end:
        print("Recording segment " + str(segmento))

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        filename = WAVE_OUTPUT_FILENAME + str(wavfile) + '.wav'
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
        pred = reconocedor.predecir(excel_file)
        
        #pred = ""
        
        prediction.set(pred)
        print("Segment " + str(segmento) + " successfully recorded")
        segmento += 1
        if wavfile == 1:
            wavfile = 0
        else:
            wavfile = 1

    print("Closing microphone")
    stream.stop_stream()
    stream.close()
    status.set("stopped")
    p.terminate()

def stop():
    global end
    end = True
    prediction.set("stop()")


window = tk.Tk()
global status
status = tk.StringVar()
status.set("stopped")
global prediction
prediction = tk.StringVar()
prediction.set("none")

li = tk.Label(window, text="EMOTION DETECTION")
li.grid(row=0, column=0)


bt = tk.Button(window, command=openMic, text="Open microphone")
bt.grid(row=2, column=0)

bt = tk.Button(window, command=closeMic, text="Close microphone")
bt.grid(row=2, column=1)

li = tk.Label(window, text="Current status:")
li.grid(row=3, column=0)

li = tk.Label(window, textvariable=status)
li.grid(row=3, column=1)

li = tk.Label(window, text="Predicted:")
li.grid(row=5, column=0)

li = tk.Label(window, textvariable=prediction)
li.grid(row=5, column=1)


window.mainloop()

