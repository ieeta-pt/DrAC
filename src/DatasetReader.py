import glob
import codecs

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
					"file name"":{
						"cn": "clinical note",
						"annotation":{
							"id":("concept",[(span,span), ...])
						},
						"relation":{
							"id": (type, annId1, annId2)
						}
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
		"""
		This private method reads the dataset from N2C2 2018 Track 2
		:param directory: Root directory for the dataset
		:return: Dict similar to the method readClinicalNotes
		"""
		cn = {}
		for dataset in ["train", "test"]:
			cn[dataset] = {}
			allCNs = sorted(glob.glob('{}{}/*.{}'.format(directory, dataset, "txt")))
			for file in allCNs:
				fileName = file.split("/")[-1].split(".")[0]
				cn[dataset][fileName] = {}
				with codecs.open(file, 'r', encoding='utf8') as fp:
					cn[dataset][fileName]["cn"] = fp.read()

			allAnn = sorted(glob.glob('{}{}/*.{}'.format(directory, dataset, "ann")))
			for file in allAnn:
				"""
					"annotation":{
						"id":("concept","type",[(span,span), ...])
					},
					"relation":{
						"id": (type, annId1, annId2)
					}
				"""
				fileName = file.split("/")[-1].split(".")[0]
				cn[dataset][fileName]["annotation"] = {}
				cn[dataset][fileName]["relation"] = {}
				with codecs.open(file, 'r', encoding='utf8') as fp:
					for line in fp.read().split("\n"):
						#T1	Reason 10179 10197	recurrent seizures
						if line.startswith("T"):
							data = line.split("\t")
							ann = data[1].replace(";", " ").split(" ")
							if ann[0].startswith("Drug"):
								annType = ann[0]
								span = []
								for s in ann[1:]:
									span.append(int(s))
								cn[dataset][fileName]["annotation"][data[0]] = (data[2], annType, span)
						#R1	Reason-Drug Arg1:T1 Arg2:T3
						elif line.startswith("R"):
							pass
		return cn

	def _reader2014Track2(directory):
		print("to do")
		print(directory)