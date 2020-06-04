import librosa as lb
import matplotlib.pyplot as plt
import numpy as np
from librosa import display
from scipy.fft import fft
import xlsxwriter
from pyAudioAnalysis import audioTrainTest as aT
import sys

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
    #plt.show()
    return xf, magn

# Devuelve las frecuencias menores a 280 y que se presentan más en más del percentil TOL
def datos_significantes(x, y, tol):
    data = []
    x300 = []
    y300 = []

    for i in range(len(y)):
        if x[i] <= 280:
            x300.append(x[i])
            y300.append(y[i])

    lim = np.percentile(y300, tol)
    for i in range(len(y300)):
        if (y300[i] >= lim):
            data.append(x300[i])
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


def findGender(filepath):
    if '1001' in filepath: 
        return 'Male'
    elif '1002' in filepath:
        return 'Female'
    elif '1003' in filepath:
        return 'Female'
    elif '1004' in filepath:
        return 'Female'
    elif '1005' in filepath:
        return 'Male'
    elif '1006' in filepath:
        return 'Female'
    elif '1007' in filepath:
        return 'Female'
    elif '1008' in filepath:
        return 'Female'
    elif '1009' in filepath:
        return 'Female'
    elif '1010' in filepath:
        return 'Female'
    elif '1011' in filepath:
        return 'Male'
    elif '1012' in filepath:
        return 'Female'
    elif '1013' in filepath:
        return 'Female'
    elif '1014' in filepath:
        return 'Male'
    elif '1015' in filepath:
        return 'Male'
    elif '1016' in filepath:
        return 'Male'
    elif '1017' in filepath:
        return 'Male'
    elif '1018' in filepath:
        return 'Female'
    elif '1019' in filepath:
        return 'Male'
    elif '1020' in filepath:
        return 'Female'
    elif '1021' in filepath:
        return 'Female'
    elif '1022' in filepath:
        return 'Male'
    elif '1023' in filepath:
        return 'Male'
    elif '1024' in filepath:
        return 'Female'
    elif '1025' in filepath:
        return 'Female'
    elif '1026' in filepath:
        return 'Male'
    elif '1027' in filepath:
        return 'Male'
    elif '1028' in filepath:
        return 'Female'
    elif '1029' in filepath:
        return 'Female'
    elif '1030' in filepath:
        return 'Female'
    elif '1031' in filepath:
        return 'Male'
    elif '1032' in filepath:
        return 'Male'
    elif '1033' in filepath:
        return 'Male'
    elif '1034' in filepath:
        return 'Male'
    elif '1035' in filepath:
        return 'Male'
    elif '1036' in filepath:
        return 'Male'
    elif '1037' in filepath:
        return 'Female'
    elif '1038' in filepath:
        return 'Male'
    elif '1039' in filepath:
        return 'Male'
    elif '1040' in filepath:
        return 'Male'
    elif '1041' in filepath:
        return 'Male'
    elif '1042' in filepath:
        return 'Male'
    elif '1043' in filepath:
        return 'Female'
    elif '1044' in filepath:
        return 'Male'
    elif '1045' in filepath:
        return 'Male'
    elif '1046' in filepath:
        return 'Female'
    elif '1047' in filepath:
        return 'Female'
    elif '1048' in filepath:
        return 'Male'
    elif '1049' in filepath:
        return 'Female'
    elif '1050' in filepath:
        return 'Male'
    elif '1051' in filepath:
        return 'Male'
    elif '1052' in filepath:
        return 'Female'
    elif '1053' in filepath:
        return 'Female'
    elif '1054' in filepath:
        return 'Female'
    elif '1055' in filepath:
        return 'Female'
    elif '1056' in filepath:
        return 'Female'
    elif '1057' in filepath:
        return 'Male'
    elif '1058' in filepath:
        return 'Female'
    elif '1059' in filepath:
        return 'Male'
    elif '1060' in filepath:
        return 'Female'
    elif '1061' in filepath:
        return 'Female'
    elif '1062' in filepath:
        return 'Male'
    elif '1063' in filepath:
        return 'Female'
    elif '1064' in filepath:
        return 'Male'
    elif '1065' in filepath:
        return 'Male'
    elif '1066' in filepath:
        return 'Male'
    elif '1067' in filepath:
        return 'Male'
    elif '1068' in filepath:
        return 'Male'
    elif '1069' in filepath:
        return 'Male'
    elif '1070' in filepath:
        return 'Male'
    elif '1071' in filepath:
        return 'Male'
    elif '1072' in filepath:
        return 'Female'
    elif '1073' in filepath:
        return 'Female'
    elif '1074' in filepath:
        return 'Female'
    elif '1075' in filepath:
        return 'Female'
    elif '1076' in filepath:
        return 'Female'
    elif '1077' in filepath:
        return 'Male'
    elif '1078' in filepath:
        return 'Female'
    elif '1079' in filepath:
        return 'Female'
    elif '1080' in filepath:
        return 'Male'
    elif '1081' in filepath:
        return 'Male'
    elif '1082' in filepath:
        return 'Female'
    elif '1083' in filepath:
        return 'Male'
    elif '1084' in filepath:
        return 'Female'
    elif '1085' in filepath:
        return 'Male'
    elif '1086' in filepath:
        return 'Male'
    elif '1087' in filepath:
        return 'Male'
    elif '1088' in filepath:
        return 'Male'
    elif '1089' in filepath:
        return 'Female'
    elif '1090' in filepath:
        return 'Male'
    elif '1091' in filepath:
        return 'Female'
    elif '_' in filepath:
        return 'Female'
    elif 'hombre' in filepath:
        return 'Male'


# hallar la amplitud
def condensar_amplitud(x):
    data = []
    for amp in x:
        if amp > 0:
            data.append(amp)
    return np.mean(data)




def hallarVariables(file):

    filepath = file
    
    # Hay algunas frecuencias que se producen más veces o con más fuerza que las demás
    # Las que se producen por encima del TOLERANCIA% de la muestra son las que se toman en cuenta para determinar la media
    # 85 es un buen valor pero esto es solo algo inical luego toca experimentar con más valores a ver cuál da mejor resultado
    TOLERANCIA = 85

    # Sacar las samples del mp3 o wav
    # Las samples son amplitud en tiempo, no son importantes en sí, hay que transformarlas
    samples, sampling_rate = lb.load(filepath, sr=8000, mono=True, offset=0.0, duration=None)

    # hallamos la frecuencia
    xfr, yma = fft_plot(samples, 8000)
    data = datos_significantes(xfr, yma, TOLERANCIA)
    media = np.mean(data)
    mediana = np.median(data)

    # hallamos la amplitud
    amplitud = condensar_amplitud(samples)

    # hallamos la valencia usando el modelo de ML de svmSpeechEmotion
    arregloValenciaArousal, nombreVariable = aT.file_regression(filepath, "data/models/svmSpeechEmotion", "svm")

    #nombre del archivo sin el .wav
    
    fileName = filepath[:-4]
    try:
        (fileName.rindex('/'))
        nameStart = fileName.rindex('/') + 1
        fileName = fileName[nameStart:]
    except:
        fileName = fileName

    # creamos la tabla y la hoja de excel
    print ('Creating Excel file...')

    workbook = xlsxwriter.Workbook(fileName+'.xlsx')
    worksheet = workbook.add_worksheet(fileName)

    # creamos los labels con las variables en la fila 0
    row = 0
    col = 0
    worksheet.write(row, col, 'Emocion')
    worksheet.write(row, col+1, 'Freq')
    worksheet.write(row, col+2, 'Amplitud')
    worksheet.write(row, col+3, 'Tiempo')
    worksheet.write(row, col+4, 'Valence')
    worksheet.write(row, col+5, 'Arousal')
    worksheet.write(row, col+6, 'Gender')
    worksheet.write(row, col+7, 'median')
    worksheet.write(row, col+8, 'Subject')
    row = 1

    # copiamos la emocion en la col 0
    col = 0
    emocion = etiquetar_emocion(filepath)
    worksheet.write(row, col, emocion)

    # copiamos la frecuencia en la col 1
    col = 1
    worksheet.write(row, col, media)

    # copiamos la amplitud en la col 2
    col = 2
    worksheet.write(row, col, amplitud)

    # copiamos el tiempo en la col 3
    col = 3
    tiempo = lb.get_duration(filename=filepath )
    worksheet.write(row, col, tiempo)

    # copiamos la valencia en la col 4
    col = 4
    worksheet.write(row, col, arregloValenciaArousal[1])

    # copiamos el arousal en la col 5
    col = 5
    worksheet.write(row, col, arregloValenciaArousal[0])

    # copiamos el genero en la col 6
    col = 6
    checkGender = findGender(filepath)
    gender = 1 if "Male" in checkGender else 0
    worksheet.write(row, col, gender)

    # copiamos el wavelength en la col 7
    #col = 7
    #waveLenth = 340 / media
    #worksheet.write(row, col, waveLenth)

    # copiamos la mediana de la frecuencia en la col 7
    col = 7
    worksheet.write(row, col, mediana)

    # copiamos el nombre del file en la col 8
    col = 8
    worksheet.write(row, col, fileName)


    #cerramos la tabla de excel
    workbook.close()
    print ('Excel created with name: ' + fileName + '.xlsx')
    return fileName
    #return ans


if __name__ == "__main__":
    # Nombre del archivo al cual se le va a sacar la frecuencia
    input_file = str(sys.argv[1])
    excel_file_name = hallarVariables(input_file)
