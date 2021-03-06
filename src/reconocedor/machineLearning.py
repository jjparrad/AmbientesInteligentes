import sklearn # modelos de ml
from sklearn.model_selection import train_test_split #para dividir en test y train
from sklearn.ensemble import RandomForestClassifier #modelo Random Forest
from sklearn.metrics import accuracy_score #presicion
from sklearn.metrics import confusion_matrix #matriz confusion
from sklearn.metrics import f1_score #f1 score
import xlsxwriter # para copiar en excel
import xlrd # para leer en excel
import argparse # para leer parametros por consola
import pickle # para guardar y importar el modelo

def train_model(excel_file):

    # abrimos excel con la db
    loc = excel_file

    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0) 
    
    sheet.cell_value(0, 0) 
    

    # 
    label_names = sheet.row_values(0,0,1)
    labels = sheet.col_values(0,1,sheet.nrows)
    feature_names = sheet.row_values(0,1,8)
    i = 1
    features = []
    while i < sheet.nrows:
        features.append(sheet.row_values(i,1,8))
        i += 1


    # dividimos los datos, el 66% para entrenamiento y el resto para tests
    train, test, train_labels, test_labels = train_test_split(features, labels, test_size = 0.33, random_state = 42)

    # inicializamos el clasificador ( modelo de ML, Random Forest)
    rf = RandomForestClassifier(n_estimators = 500, random_state = 42)

    # entrenamos el clasificador
    print("Training Model...")
    model = rf.fit(train, train_labels);

    # guardamos el clasificador
    filename = 'modelo_emociones_eafit.sav'
    pickle.dump(model, open(filename, 'wb'))

    print("Model saved as: < modelo_emociones_eafit.sav >")

    # hacemos predicciones con los datos de test
    preds_randomF = rf.predict(test)

    # Evaluamos la precision comparando el test con las predicciones sacadas.
    print("precision = ", accuracy_score(test_labels, preds_randomF))
    print("F1_score = ", f1_score(test_labels, preds_randomF, average='macro'))

    # Matriz de confusion, el 7 son las posibles opciones que tenewmos, 7 emociones.
    print("Matriz de confusion:")
    print(confusion_matrix(test_labels, preds_randomF, labels=range(6)))
   


def predecir(excel_file):
    # cargamos los datos de excel
    loc = excel_file
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0) 
    sheet.cell_value(0, 0)

    # organizamos los datos para ser enviados al modelo
    i = 1
    features = []
    features.append(sheet.row_values(1,1,8))
    print("Frequency: ", features[0][0])
    print("Amplitude: ", features[0][1])
    print("Time: ", features[0][2])
    print("Valence: ", features[0][3])
    print("Arrousal: ", features[0][4])
    print("Gender: ", features[0][5])
    print("Frequency median: ", features[0][6])
    # cargamos el modelo
    filename = 'modelo_emociones_eafit.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    # hacemos la prediccion
    result = loaded_model.predict(features)
    #print(result) #linea original
    newResult = str(result).replace('[', '')
    newResult = newResult.replace(']', '')
    newResult = int(newResult.replace('.', ''))

    ans = ''
    if newResult == 1:
        ans = 'anger'
    elif newResult == 2:
        ans = 'disgust'
    elif newResult == 3:
        ans = 'fear'
    elif newResult == 4:
        ans = 'happiness'
    elif newResult == 5:
        ans = 'sadness'
    elif newResult == 6:
        ans = 'surprise'
    elif newResult == 7:
        ans = 'neutral'
    else:
        ans = 'sin emocion'

    #print(newResult)
    print("Emotion detected: " + ans)
    #return result
    return ans

def parse_arguments():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-train", help="train the algorithm with a <dataset>")
    group.add_argument("-predict", help="make a prediction with a <excel file>")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    
    if args.train:
        print("entrenaremos el modelo con la base de datos:", args.train)
        train_model(args.train)
    elif args.predict:
        print("haremos una prediccion los los valores de:", args.predict)
        predecir(args.predict)
    else:
        print("sin argumentos")
