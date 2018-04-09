class GeoInfo:
	def __init__(self, veiculo, lat, lon, dthr, linha):
		self.veiculo = veiculo
		self.lat = lat
		self.lon = lon
		self.dthr = dthr
		self.linha = linha
		
	def __repr__(self):
		return self.dthr.__str__()
		
