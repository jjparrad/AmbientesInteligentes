import librosa as lb
import matplotlib.pyplot as plt
import numpy as np
from librosa import display
from scipy.fft import fft
import xlsxwriter
from pyAudioAnalysis import audioTrainTest as aT
import os
from statistics import mean




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

# tol es el porcentaje de seleccion 
def datos_significantes(x, y, tol):
    data = []
    lim = np.percentile(y, tol)
    for i in range(len(y)):
        if y[i] >= lim:
            data.append(x[i])
    return data


# etiquetamos la emocion segun el nombre del audio
def etiquetar_emocion(filepath):
    if 'anger' in filepath or 'angry' in filepath:
        emocion = 1
    elif 'disgust' in filepath:
        emocion = 2
    elif 'fear' in filepath:
        emocion = 3
    elif 'happiness' in filepath or 'happy' in filepath:
        emocion = 4
    elif 'sadness' in filepath or 'sad' in filepath:
        emocion = 5
    elif 'surprise' in filepath or 'ps' in filepath:
        emocion = 6
    elif 'neutral' in filepath:
        emocion = 7
    else:
        emocion = 0

    return emocion


# hallar la amplitud
def condensar_amplitud(x):
    data = []
    for amp in x:
        if amp > 0:
            data.append(amp)
    return np.mean(data)



# guardamos todos los audios de la carpeta objetivo ( audiosEtiquetados ) en un arreglo
files = []
for dirname, dirnames, filenames in os.walk('../samuel/audios/audiosEtiquetados'):
    # print path to all subdirectories first.
    for subdirname in dirnames:
        files.append(os.path.join(dirname, subdirname))

    # print path to all filenames.
    for filename in filenames:
        files.append(os.path.join(dirname, filename))


# Hay algunas frecuencias que se producen mas veces o con mas fuerza que las demas
# Las que se producen por encima del TOLERANCIA% de la muestra son las que se toman en cuenta para determinar la media
# 85 es un buen valor pero esto es solo algo inical luego toca experimentar con mas valores a ver cual da mejor resultado
TOLERANCIA = 90


# creamos la tabla y la hoja de excel
print ('creando archivo en excel...')
workbook = xlsxwriter.Workbook('datos.xlsx')
worksheet = workbook.add_worksheet('hoja0')

# creamos los labels con las variables en la fila 0
row = 0
col = 0
worksheet.write(row, col, 'Emocion')
worksheet.write(row, col+1, 'Freq')
worksheet.write(row, col+2, 'Amplitud')
worksheet.write(row, col+3, 'Tiempo')
worksheet.write(row, col+4, 'Valence')
worksheet.write(row, col+5, 'Wavelength') # 340 / freq (HZ)
worksheet.write(row, col+6, 'Subject')

'''
#promedios freq y amplitud
promFrec = {
    "0" : {
        "prom": [],
        "cont": 0
    },
    "1" : {
        "prom": [],
        "cont": 0
    },
    "2" : {
        "prom": [],
        "cont": 0
    },
    "3" : {
        "prom": [],
        "cont": 0
    },
    "4" : {
        "prom": [],
        "cont": 0
    },
    "5" : {
        "prom": [],
        "cont": 0
    },
    "6" : {
        "prom": [],
        "cont": 0
    },
    "7" : {
        "prom": [],
        "cont": 0
    }
}

promAmpli = {
    "0" : {
        "prom": [],
        "cont": 0
    },
    "1" : {
        "prom": [],
        "cont": 0
    },
    "2" : {
        "prom": [],
        "cont": 0
    },
    "3" : {
        "prom": [],
        "cont": 0
    },
    "4" : {
        "prom": [],
        "cont": 0
    },
    "5" : {
        "prom": [],
        "cont": 0
    },
    "6" : {
        "prom": [],
        "cont": 0
    },
    "7" : {
        "prom": [],
        "cont": 0
    }
}
'''
# iteramos por cada audio
i = 0
while i < len(files):
    # Nombre del archivo al cual se le va a sacar la frecuencia
    filepath = files[i]

    # Sacar las samples del mp3 o wav
    # Las samples son amplitud en tiempo, no son importantes en si, hay que transformarlas
    samples, sampling_rate = lb.load(filepath, sr=8000, mono=True, offset=0.0, duration=None)

    # hallamos la frecuencia
    xfr, yma = fft_plot(samples, 8000)
    data = datos_significantes(xfr, yma, TOLERANCIA)
    media = np.mean(data)

    # hallamos la amplitud
    amplitud = condensar_amplitud(samples)

    # hallamos la valencia usando el modelo de ML de svmSpeechEmotion
    try:
        valorValencia, nombreVariable = aT.file_regression(filepath, "data/models/svmSpeechEmotion", "svm")
    except: 
        valorValencia = 'error'
        print ("el error fue en ", filepath)

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
    '''
    promFrec[str(emocion)]["cont"] = promFrec[str(emocion)]["cont"] + 1
    promFrec[str(emocion)]["prom"].append(media)
    '''

    # copiamos la amplitud en la col 2
    col = 2
    worksheet.write(row, col, amplitud)
    '''
    promAmpli[str(emocion)]["cont"] = promAmpli[str(emocion)]["cont"] + 1
    promAmpli[str(emocion)]["prom"].append(amplitud)
    '''

    # copiamos el tiempo en la col 3
    col = 3
    tiempo = lb.get_duration(filename=filepath )
    worksheet.write(row, col, tiempo)

    # copiamos la valencia en la col 4
    col = 4
    worksheet.write(row, col, valorValencia[0])

    # copiamos el wavelength en la col 5
    col = 5
    waveLenth = 340 / media
    worksheet.write(row, col, waveLenth)

    # copiamos el nombre del file en la col 6
    col = 6
    worksheet.write(row, col, fileName)

    i += 1






#cerramos la tabla de excel
workbook.close()

print ('Archivo de excel creado con nombre ' + 'datos.xlsx')
'''
l = 1
while(l < len(promFrec)):
    print(l, "promedio = ", mean(promFrec[str(l)]["prom"]))
    l +=1

l = 1
while(l < len(promAmpli)):
    print(l, "amplitud = ", mean(promAmpli[str(l)]["prom"]))
    l += 1
'''