from geoinfo import GeoInfo
from datetime import datetime, time, date, timedelta
from pyspark import SparkContext, SparkConf	
import math	


def criaData(strDate):
	strDate = toAscii(strDate)
	myDate = date(int(strDate[4:8]), int(strDate[2:4]), int(strDate[0:2]))
	myTime = time(int(strDate[8:10]), int(strDate[10:12]), int(strDate[12:14]))
	return datetime.combine(myDate, myTime)
	
def toAscii(stri):
	stres = stri.encode('ascii','ignore')
	return stres.translate(None, "/: \\")
		
	
def convNumerico(strNum):
	return float(strNum.replace(",", "."))
		
		
def calcDistancia(x1, y1, x2, y2):
	return getDistanceFromLatLonInKm(x1, y1, x2, y2)
	
def getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2):
	R = 6371 #Radius of the earth in km
	dLat = deg2rad(lat2-lat1)  #deg2rad below
	dLon = deg2rad(lon2-lon1) 
	a = math.sin(dLat/2) * math.sin(dLat/2) + \
		math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) * \
		math.sin(dLon/2) * math.sin(dLon/2)
		
	c = 2 * math.atan2(math.pow(a, 0.5), math.pow(1-a, 0.5))
	d = R * c #Distance in km
	return d
	

def deg2rad(deg):
	return math.radians(deg)
		

if __name__ == "__main__":
	sc = SparkContext(appName = "Problema4")
	
	dataset = sc.textFile("/home/julio/prob4/dados.txt")
	
	result = dataset.map(lambda x: x[2:-2])\
					.map(lambda x: x.split('","'))\
					.map(lambda x: map(lambda y: y.split('":"'), x))\
					.map(lambda x: GeoInfo(x[0][1], convNumerico(x[1][1]), convNumerico(x[2][1]), criaData(x[3][1]), x[4][1]))\
					.map(lambda x: ((x.veiculo, x.linha), (x.lat, x.lon, x.dthr, 0, timedelta())))
					

	fAggregate = lambda x, y: (y[0], y[1], y[2], x[3] + calcDistancia(x[0], x[1], y[0], y[1]), x[4] + x[2] - y[2])
	result = result.reduceByKey(fAggregate)\
					.map(lambda x: ((toAscii(x[0][0]), toAscii(x[0][1])), (x[1][3], x[1][4].total_seconds())))
					
	print(result.collect())
	result.saveAsTextFile("res-prob4")
	
	sc.stop()
	
