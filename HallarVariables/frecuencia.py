from scipy import fft, arange
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import xlsxwriter
from io import BytesIO
import os
import sys


def frequency_sepectrum(x, sf):
    """
    Derive frequency spectrum of a signal from time domain
    :param x: signal in the time domain
    :param sf: sampling frequency
    :returns frequencies and their content distribution
    """
    x = x - np.average(x)  # zero-centering

    n = len(x)
    #print(n)
    k = arange(n)
    tarr = n / float(sf)
    frqarr = k / float(tarr)  # two sides frequency range

    frqarr = frqarr[range(n // 2)]  # one side frequency range

    x = fft(x) / n  # fft computing and normalization
    x = x[range(n // 2)]

    return frqarr, abs(x)


# Sine sample with a frequency of 1hz and add some noise
sr = 32  # sampling rate
y = np.linspace(0, 2*np.pi, sr)
y = np.tile(np.sin(y), 5)
y += np.random.normal(0, 1, y.shape)
t = np.arange(len(y)) / float(sr)

plt.subplot(2, 1, 1)
plt.plot(t, y)
plt.xlabel('t')
plt.ylabel('y')

frq, X = frequency_sepectrum(y, sr)

plt.subplot(2, 1, 2)
plt.plot(frq, X, 'b')
plt.xlabel('Freq (Hz)')
plt.ylabel('|X(freq)|')
plt.tight_layout()



#El audio debe estar en la misma carpeta del codigo
inputFile =  str(sys.argv[1])
print ('Trabajando con archivo ' + inputFile)

here_path = os.path.dirname(os.path.realpath(__file__))
wav_file_name = inputFile #Aqui toca poner el nombre del audio 
wave_file_path = os.path.join(here_path, wav_file_name)
sr, signal = wavfile.read(wave_file_path)

#SI TENEMOS MENOS DE 2 DIMENCIONES, LO CONVERTIMOS A 2 DIMENCIONES
if signal.ndim > 1:
    # use the first channel (or take their average, alternatively)
	y = signal[:, 0]
else:
    # use the first channel (or take their average, alternatively)
	signal = signal.reshape(signal.size, 1)
	y = signal[:, 0]

#y = signal[:, 0]  # use the first channel (or take their average, alternatively)
t = np.arange(len(y)) / float(sr)

plt.figure()
plt.subplot(2, 1, 1)
plt.plot(t, y)
plt.xlabel('t')
plt.ylabel('y')

# FRECUENCIA
frq, X = frequency_sepectrum(y, sr)
data = frq

plt.subplot(2, 1, 2)
plt.plot(frq, X, 'b')
plt.xlabel('Freq (Hz)')
plt.ylabel('|X(freq)|')
plt.tight_layout()
fig = plt

#NOMBRE DEL ARCHIVO SIN EL .WAV
fileName = wav_file_name[:-4]
#CON ESTO SE COPIA EN EXCEL
print ('creando archivo en excel...')
workbook = xlsxwriter.Workbook(fileName+'.xlsx') # NOMBRE DEL ARCHIVO
worksheet = workbook.add_worksheet(fileName) #NOMBRE DEL ARCHIVO
cont = 0
row = 0
col = 0
worksheet.write(row, col, 'Freq');
worksheet.write(row, col+1, 'Amplitud');
worksheet.write(row, col+2, 'Tiempo');
worksheet.write(row, col+3, 'Valence');

row = 1
for x_var in (frq):
    worksheet.write(row, col,     cont) # CONTADOR POR CADA REPETICION COL 0 ( ¿TIEMPO? )
    worksheet.write(row, col + 1, x_var) # VARIABLE A COPIAR ( FRECUENCIA EN ESTE CASO ) COL 1
    row += 1
    cont += 1

col = 2
row = 1
for amplitud in (y):
    worksheet.write(row, col, amplitud) #COPIAMOS LA AMPLITUD ( INTENSIDAD) EN LA COL 2
    row += 1

col = 3
row = 1
Fs, x = wavfile.read(wave_file_path)
worksheet.write(row, col, len(x)/Fs)
workbook.close()

print ('Archivo de excel creado con nombre ' + fileName + '.xlsx')
#f = wave.openfp(wave_file_path, 'r')
#print(f.getframerate())
#plt.show()
