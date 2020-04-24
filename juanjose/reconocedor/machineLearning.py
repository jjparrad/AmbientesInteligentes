import sklearn # modelos de ml
from sklearn.model_selection import train_test_split #para dividir en test y train
from sklearn.naive_bayes import GaussianNB #modelo naives bayes
from sklearn.metrics import accuracy_score #presicion
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
    feature_names = sheet.row_values(0,1,6)
    i = 1
    features = []
    while i < sheet.nrows:
        features.append(sheet.row_values(i,1,6))
        i += 1


    # dividimos los datos, el 66% para entrenamiento y el resto para tests
    train, test, train_labels, test_labels = train_test_split(features, labels, test_size = 0.33, random_state = 42)

    # inicializamos el clasificador ( modelo de ML )
    gnb = GaussianNB()

    # entrenamos el clasificador
    print("entrenando modelo...")
    model = gnb.fit(train, train_labels)

    # guardamos el clasificador
    filename = 'modelo_emociones_eafit.sav'
    pickle.dump(model, open(filename, 'wb'))
    print("modelo guardado como < modelo_emociones_eafit.sav >")

    # hacemos predicciones con los datos de test
    preds = gnb.predict(test)
    print(preds)

    # Evaluamos la precision comparando el test con las predicciones sacadas.
    print("precision de = ", accuracy_score(test_labels, preds))


def predecir(excel_file):
    # cargamos los datos de excel
    loc = excel_file
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0) 
    sheet.cell_value(0, 0)

    # organizamos los datos para ser enviados al modelo
    i = 1
    features = []
    while i < sheet.nrows:
        features.append(sheet.row_values(i,1,6))
        i += 1

    # cargamos el modelo
    filename = 'modelo_emociones_eafit.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    # hacemos la prediccion
    result = loaded_model.predict(features)
    print(result)

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