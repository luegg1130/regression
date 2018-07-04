import sys
import csv
import numpy as np
import math

train_addr = 'D:/work/AI/python/Predict_PM2.5/Regression/train.csv'
test_addr = 'D:/work/AI/python/Predict_PM2.5/Regression/test.csv'

#read data
train_data = []
for i in range(18):
    train_data.append([])

txt = open(train_addr, 'r', encoding='big5', newline='')
rows = csv.reader(txt , delimiter=",")

n_row = 0
for row in rows:
    if(n_row != 0):
        for idx in range(3, 27):
            if(row[idx] != 'NR'):
                train_data[(n_row-1)%18].append(float(row[idx]))
            else:
                train_data[(n_row-1)%18].append(0)
    n_row = n_row + 1

txt.close()

#parse data to (x,y)
x = []
y = []
for mon in range(12):
    for data_m in range(471):
        x.append([])
        for data_type in range(18):
            for hr in range(9):
                x[mon*471+data_m].append(train_data[data_type][mon*480+data_m+hr])
        y.append(train_data[9][mon*480+data_m+9])
x = np.array(x)
y = np.array(y)

#add bias
x = np.concatenate((np.ones((x.shape[0], 1)), x), axis=1)

#init weight & hyperparams
w = np.zeros(len(x[0]))
l_rate = 10
repeat = 10000

x_t = x.transpose()
s_gra = np.zeros(len(x[0]))
#start learning
for i in range(repeat):
    hypo = np.dot(x, w)
    loss = y - hypo
    cost = np.sum(loss ** 2) / len(x)
    s_cost = math.sqrt(cost)
    gra = np.dot(x_t, loss)
    s_gra += gra ** 2
    ada = np.sqrt(s_gra)
    w = w + l_rate * (gra / ada)
    print('iteration: %d | cost: %f  ' %(i, cost))


#save model
np.save('D:/work/AI/python/Predict_PM2.5/Regression/model.npy', w)
#load model
w = np.load('D:/work/AI/python/Predict_PM2.5/Regression/model.npy')

#read test data
test = []
n_row = 0
txt = open(test_addr, 'r', encoding='big5', newline='')
rows = csv.reader(txt, delimiter=",")
for r in rows:
    if(n_row % 18 ==0):
        test.append([])
        for c in range(2, 11):
            test[n_row//18].append(float(r[c]))
    else:
        for c in range(2, 11):
            if(r[c] != 'NR'):
                test[n_row//18].append(float(r[c]))
            else:
                test[n_row//18].append(0)
    n_row = n_row + 1
txt.close()
x_test = np.array(test)

#add bias
x_test = np.concatenate((np.ones((x_test.shape[0], 1)), x_test), axis = 1)

#test
ans = []
for i in range(len(x_test)):
    ans.append(['id_'+str(i)])
    a = np.dot(w, x_test[i])
    ans[i].append(a)

filename = 'D:/work/AI/python/Predict_PM2.5/Regression/result/predict.csv'
txt = open(filename, 'w+')
wt = csv.writer(txt, delimiter=',', lineterminator='\n')
wt.writerow(['id', 'value'])
for i in range(len(ans)):
    wt.writerow(ans[i])
txt.close()











