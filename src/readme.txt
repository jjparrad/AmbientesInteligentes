# Create the virtual enviroment to start working on the project, instruccions about how to do it in the link below

	https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/

# Install dependencies to run the project

	pip install -r requirements

# Create an excel DB to feed the model, using an existing sound DB, this will convert all audios into excel files, this is optional becouse the project is already trained

	python3 predecir.py -populate "carpeta con audios de entrenamiento"

# Train the model with an excel file, this is optional becouse the project is already trained

	python3 predecir.py -train "excel con datos de entrenamiento"

# Run the model to detect an audio emotion

	python3 predecir.py -predict "audio.wav que se quiere predecir"

# We can also run the model with real time audio using the GUI, it is not as accurate becouse the way we take input sound
	python3 leerAudio.py

# If you have any doubt about how to connect this project to another one, feel free to write me
	josemb125@gmail.com

