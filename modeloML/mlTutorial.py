import sklearn
from sklearn.datasets import load_breast_cancer #db
from sklearn.model_selection import train_test_split #para dividir en test y train
from sklearn.naive_bayes import GaussianNB #modelo naives bayes
from sklearn.metrics import accuracy_score #presicion
import xlsxwriter
import xlrd

#load dataset
data = load_breast_cancer()

#organize data
label_names = data['target_names']
labels = data['target']
feature_names = data['feature_names']
features = data['data']

#look data
# print(label_names)
# print (len(label_names))
# print('Class label = ', labels[0])
# print(feature_names)
# print(features[0])

workbook = xlsxwriter.Workbook('test.xlsx') # NOMBRE DEL ARCHIVO
worksheet = workbook.add_worksheet('hoja1') #NOMBRE DEL ARCHIVO

col = 0
row = 0
for x in (label_names):
    worksheet.write(row, col, x)
    col += 1

col = 0
row = 1
for x_var in (labels):
    worksheet.write(row, col, x_var) 
    row += 1

col = 2
row = 0
for y in (feature_names):
    worksheet.write(row, col, y)
    col += 1

col = 2
row = 1
z = 0
while z < len(features):
    for k in (features[z]):
        worksheet.write(row, col, k) 
        col += 1
    
    col = 2
    z += 1
    row += 1

workbook.close()

loc = ("test.xlsx") 
  
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
  
sheet.cell_value(0, 0) 
  
print(sheet.row_values(0,2,32))
label_names = sheet.row_values(0,0,2)
labels = sheet.col_values(0,1,sheet.nrows)
feature_names = sheet.row_values(0,2,32)
i = 1
features = []
while i < sheet.nrows:
    features.append(sheet.row_values(i,2,32))
    i += 1


#split data
train, test, train_labels, test_labels = train_test_split(features, labels, test_size = 0.33, random_state = 42)

#initialize clasifier# Initialize our classifier
gnb = GaussianNB()

# Train our classifier
model = gnb.fit(train, train_labels)

# Make predictions
preds = gnb.predict(test)
print(preds)

# Evaluate accuracy
print("precicion de = ", accuracy_score(test_labels, preds))