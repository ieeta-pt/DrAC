
class DatasetReader():
	def readClinicalNotes(dir, datasetName):
		if datasetName == "2018_track2":
			return DatasetReader._reader2018Track2(dir)
		elif datasetName == "2014_track2":
			return DatasetReader._reader2014Track2(dir)
		else:
			raise("There are no reader defined for this dataset, please implement it or used one of the ones already existent!")
		return None

	def _reader2018Track2(dir):
		pass

	def _reader2014Track2(dir):
		pass