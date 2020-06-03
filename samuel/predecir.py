import sys
sys.path.insert(1, 'clasificador') # insert at 1, 0 is the script path (or '' in REPL)
import hallarVariablesUnico as clasificador
import hallarVariablesMulti as clasificadorMulti
sys.path.insert(1, 'reconocedor') # ESTO ES PARA ENTRAR EN UNA CARPETA CON EL IMPORT
import machineLearning as reconocedor

if __name__ == "__main__":
    action = str(sys.argv[1])
    input_file = str(sys.argv[2])
    if (action == '-predict'):
        #temp = []
        #temp = clasificador.hallarVariables(input_file)
        excel_file = clasificador.hallarVariables(input_file)
        #excel_file = temp[0]
        excel_file += '.xlsx'
        #emocion = temp[1]
        reconocedor.predecir(excel_file)
    elif (action == '-populate'):
        input_folder = input_file
        clasificadorMulti.hallarVariables(input_folder)
    elif (action == '-train'):
        reconocedor.train_model(input_file)
    else:
        print('comando invalido: -predict -> predecir un audio wav; -populate -> crear un archivo excel con una carpeta de audios; -train -> entrenar el modelo con un archivo excel')