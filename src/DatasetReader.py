
class DatasetReader():
	def readClinicalNotes(directory, datasetName):
		"""
		Reads the clinical notes in the dataset. For new datasets, it is necessary implement the a new reader in this file.
		Then, the system will work properly since the return of this method follows always the same structure.
		:param directory: root directory of the dataset
		:param datasetName: dataset name, used to indetify which method to use 
		:return: Dict of clinical notes with the following structure
			{
				"train":{
					"dataset":{
						"file name": "clinical note"
					},
					"annotation":{
						"id":[(span,span), ...]
					}
					"relation":{
						"id": (type, annId1, annId2)
					}
				}
				"test":{...}
			}
		"""
		if datasetName == "2018_track2":
			return DatasetReader._reader2018Track2(directory)
		elif datasetName == "2014_track2":
			return DatasetReader._reader2014Track2(directory)
		else:
			raise("There are no reader defined for this dataset, please implement it or used one of the ones already existent!")
		return None

	def _reader2018Track2(directory):
		print("to do")
		print(directory)

	def _reader2014Track2(directory):
		print("to do")
		print(directory)