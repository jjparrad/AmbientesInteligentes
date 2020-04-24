#AudioAnalysis crea el modelo de machine learning para hallar la valencia, el modelo se encuentra ubicado en data/models

#hallarVariablesMulti.py crea un archivo de excel con nombre datos.xlsx apartir de la carpeta audios ubicada en ../audios/audiosEtiquetados

python3 hallarVariablesMulti.py

#hallarVariablesUnico.py crear un archivo excel con nombre <audio>.xlsx apartir de 1 audio suministrado por linea de comandos que debe de estar ubicado en la misma carpeta, luego si queremos predecir ese valor, le borramos el valor de la emocion y lo copiamos al reconocedor para ser usado alli.

python3 hallarVariablesUnico.py <audio.wav>

#no tengo ni idea que es argument
