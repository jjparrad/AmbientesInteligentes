#entrear en el ambiente virtual de python, desde la carpeta < reconocedor >

source bin/activate

# Entrenar el modelo

python3 machineLearning.py -train "excel con datos de entrenamiento"

# Correr el modelo

python3 machineLearning.py -predict "excel el o los datos que se quieren predecir"
