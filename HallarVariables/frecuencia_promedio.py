import librosa as lb
import matplotlib.pyplot as plt
import numpy as np
from librosa import display
from scipy.fft import fft
from scipy.io import wavfile
import xlsxwriter

# Hay algunas frecuencias que se producen más veces o con más fuerza que las demás
# Las que se producen por encima del TOLERANCIA% de la muestra son las que se toman en cuenta para determinar la media
# 85 es un buen valor pero esto es solo algo inical luego toca experimentar con más valores a ver cuál da mejor resultado
TOLERANCIA = 85

# Nombre del archivo al cual se le va a sacar la frecuencia
filepath = "00.wav"


# Sacar las samples del mp3 o wav
# Las samples son amplitud en tiempo, no son importantes en sí, hay que transformarlas
samples, sampling_rate = lb.load(filepath, sr=8000, mono=True, offset=0.0, duration=None)


# Mostrar amplitudes

plt.figure()
lb.display.waveplot(y=samples, sr=sampling_rate)
plt.xlabel("Tiempo en segundos")
plt.ylabel("Amplitud")
plt.show()


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
    return xf, magn

# tol es el porcentaje de selección 
def datos_significantes(x, y, tol):
    data = []
    lim = np.percentile(y, tol)
    for i in range(len(y)):
        if y[i] >= lim:
            data.append(x[i])
    return data


xfr, yma = fft_plot(samples, 8000)
data = datos_significantes(xfr, yma, TOLERANCIA)
media = np.mean(data)
print ("frecuencia = " , media)


# nombre del archivo sin el .wav
fileName = filepath[:-4]

# creamos la tabla y la hoja de excel
print ('creando archivo en excel...')
workbook = xlsxwriter.Workbook(fileName+'.xlsx')
worksheet = workbook.add_worksheet(fileName)

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
row = 1

# copiamos la frecuencia en la col 1
col = 1
worksheet.write(row, col, media)

# copiamos la amplitud en la col 2
col = 2
worksheet.write(row, col, 'xx.xx')

# copiamos el tiempo en la col 3
col = 3
Fs, x = wavfile.read(filepath)
worksheet.write(row, col, len(x)/Fs)

# copiamos el wavelength en la col 5
col = 5
waveLenth = 340 / media
worksheet.write(row, col, waveLenth)

#cerramos la tabla de excel
workbook.close()

print ('Archivo de excel creado con nombre ' + fileName + '.xlsx')