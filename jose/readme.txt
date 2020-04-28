#entrar en el ambiente virtual de python, desde esta carpeta

source venv/bin/activate

#instalar la dependencias del requirement.txt

pip install -r requirements

#Popular un excel con datos para ser entrenados

python3 predecir.py -populate "carpeta con audios de entrenamiento"

# Entrenar el modelo

python3 predecir.py -train "excel con datos de entrenamiento"

# Correr el modelo

python3 predecir.py -predict "audio.wav que se quiere predecir"
