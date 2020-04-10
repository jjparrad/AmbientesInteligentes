#Comando para hallar el valence en un .wav

python3 audioAnalysis.py regressionFile -i 'nombre.wav' --model svm --regression data/svmSpeechEmotion



#Comando para generar un excel con la frecuencia, amplitud de onda, duracion en seg

python3 frecuencia.py 'nombre.wav'