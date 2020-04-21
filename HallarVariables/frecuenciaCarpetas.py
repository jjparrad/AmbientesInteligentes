import librosa as lb
import matplotlib.pyplot as plt
import numpy as np
from librosa import display
from scipy.fft import fft
from scipy.io import wavfile
import xlsxwriter
from pyAudioAnalysis import audioTrainTest as aT
import os 




# Transformador de Fourier
def fft_plot(audio, sr):
    n = len(audio)
    T = 1/sr
    yf = fft(audio)
    xf = np.linspace(0.0, 1.0/(2.0*T), n//2)
    fig, ax = plt.subplots()
    magn = 2.0/n * np.abs(yf[0:n//2])
    ax.plot(xf, magn)
    plt.grid()
    plt.xlabel("Frecuencia")
    plt.ylabel("Magnitud")
    plt.close()
    return xf, magn

# tol es el porcentaje de selección 
def datos_significantes(x, y, tol):
    data = []
    lim = np.percentile(y, tol)
    for i in range(len(y)):
        if y[i] >= lim:
            data.append(x[i])
    return data


# etiquetamos la emocion segun el nombre del audio
def etiquetar_emocion(filepath):
    if 'anger' in filepath:
        emocion = 1
    elif 'disgust' in filepath:
        emocion = 2
    elif 'fear' in filepath:
        emocion = 3
    elif 'happiness' in filepath:
        emocion = 4
    elif 'sadness' in filepath:
        emocion = 5
    elif 'surprise' in filepath:
        emocion = 6
    else: # emocion neutral
        emocion = 0 

    return emocion



# guardamos todos los audios de la carpeta objetivo ( audiosEtiquetados ) en un arreglo
files = []
for dirname, dirnames, filenames in os.walk('./audiosEtiquetados'):
    # print path to all subdirectories first.
    for subdirname in dirnames:
        files.append(os.path.join(dirname, subdirname))

    # print path to all filenames.
    for filename in filenames:
        files.append(os.path.join(dirname, filename))


# Hay algunas frecuencias que se producen más veces o con más fuerza que las demás
# Las que se producen por encima del TOLERANCIA% de la muestra son las que se toman en cuenta para determinar la media
# 85 es un buen valor pero esto es solo algo inical luego toca experimentar con más valores a ver cuál da mejor resultado
TOLERANCIA = 85


# creamos la tabla y la hoja de excel
print ('creando archivo en excel...')
workbook = xlsxwriter.Workbook('datos.xlsx')
worksheet = workbook.add_worksheet('hoja0')

# creamos los labels con las variables en la fila 0
row = 0
col = 0
worksheet.write(row, col, 'Emocion');
worksheet.write(row, col+1, 'Freq');
worksheet.write(row, col+2, 'Amplitud');
worksheet.write(row, col+3, 'Tiempo');
worksheet.write(row, col+4, 'Valence');
worksheet.write(row, col+5, 'Wavelength'); # 340 / freq (HZ)
worksheet.write(row, col+6, 'Subject');


# iteramos por cada audio
i = 0
while i < len(files):
    # Nombre del archivo al cual se le va a sacar la frecuencia
    filepath = files[i]

    # Sacar las samples del mp3 o wav
    # Las samples son amplitud en tiempo, no son importantes en sí, hay que transformarlas
    samples, sampling_rate = lb.load(filepath, sr=8000, mono=True, offset=0.0, duration=None)

    # hallamos la frecuencia
    xfr, yma = fft_plot(samples, 8000)
    data = datos_significantes(xfr, yma, TOLERANCIA)
    media = np.mean(data)


    # hallamos la valencia usando el modelo de ML de svmSpeechEmotion
    valorValencia, nombreVariable = aT.file_regression(filepath, "data/models/svmSpeechEmotion", "svm")

    #nombre del archivo sin el .wav
    fileName = filepath[:-4]

    # inicializamos el row
    row = i + 1

    # copiamos la emocion en la col 0
    col = 0
    emocion = etiquetar_emocion(filepath)
    worksheet.write(row, col, emocion)

    # copiamos la frecuencia en la col 1
    col = 1
    worksheet.write(row, col, media)

    # copiamos la amplitud en la col 2
    col = 2
    worksheet.write(row, col, 0)

    # copiamos el tiempo en la col 3
    col = 3
    Fs, x = wavfile.read(filepath)
    worksheet.write(row, col, len(x)/Fs)

    # copiamos la valencia en la col 2
    col = 4
    worksheet.write(row, col, valorValencia[0])

    # copiamos el wavelength en la col 5
    col = 5
    waveLenth = 340 / media
    worksheet.write(row, col, waveLenth)

    i += 1




#cerramos la tabla de excel
workbook.close()
print ('Archivo de excel creado con nombre ' + 'datos.xlsx')
