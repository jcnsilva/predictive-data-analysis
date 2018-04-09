#coding: utf-8

import csv

mydata = [['onibus', 'linha', 'distancia', 'tempo']]

with open('part-00000', 'r') as f:
    for line in f:
        mydata.append(line.translate(None, "(')\n ").split(","))
			
			
with open('prob4data.csv', 'w') as mycsv:
	a = csv.writer(mycsv)
	a.writerows(mydata)
