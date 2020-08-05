import glob
import codecs

class DatasetReader():
	def readClinicalNotes(directory, datasetName):
		"""
		Reads the clinical notes in the dataset. For new datasets, it is necessary to implement a new reader in this file.
		The new reader must follow the same output structure as current readers. Then, the system will work properly since
		the return of this method always follows the same structure.
		:param directory: root directory of the dataset
		:param datasetName: dataset name, used to identify which reader method should be used
		:return: Dict of clinical notes with the following structure
			{
				"train":{
					"file name"":{
						"cn": "clinical note",
						"annotation":{
							"id":("concept","type",[(span,span), ...])
						},
						"relation":{
							"id": (annId1, ("concept","type",[(span,span), ...]))
						}
					}
				}
				"test":{...}
			}
		"""
		if datasetName == "2018_track2":
			return DatasetReader._reader2018Track2(directory)
		elif datasetName == "2009":
			return DatasetReader._reader2009(directory)
		elif datasetName == "examples":
			return DatasetReader._readerExamples(directory)
		else:
			raise("There are no readers defined for this dataset. Please implement it or use one of the already existing readers!")
		return None

	def _reader2018Track2(directory):
		"""
		This private method reads the dataset from N2C2 2018 Track 2 on Medication Extraction and ADE
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
						"id": (annId1, ("concept","type",[(span,span), ...]))
					}
				"""
				fileName = file.split("/")[-1].split(".")[0]
				cn[dataset][fileName]["annotation"] = {}
				cn[dataset][fileName]["relation"] = {}
				tmpStrength = {}
				with codecs.open(file, 'r', encoding='utf8') as fp:
					clinicalNote = fp.read().split("\n")
					for line in clinicalNote:
						#T1	Reason 10179 10197	recurrent seizures
						if line.startswith("T"):
							data = line.split("\t")
							ann = data[1].replace(";", " ").split(" ")
							annType = ann[0]
							if ann[0].startswith("Drug") or \
								ann[0].startswith("Strength") or \
								ann[0].startswith("Dosage") or \
								ann[0].startswith("Route"):
								span = []
								for s in ann[1:]:
									span.append(int(s))
									
							if ann[0].startswith("Drug"):
								cn[dataset][fileName]["annotation"][data[0]] = (data[2], annType, span)
							elif ann[0].startswith("Strength") or ann[0].startswith("Dosage") or ann[0].startswith("Route"):
								tmpStrength[data[0]] = (data[2], annType, span)

					for line in clinicalNote:
						#R9	Strength-Drug Arg1:T11 Arg2:T6
						if line.startswith("R"):
							data = line.split("\t")
							ann = data[1].split(" ")
							if "Strength-Drug" in ann[0] or "Dosage-Drug" in ann[0] or "Route-Drug" in ann[0]:
								annType = ann[0]
								drugId = ann[2].split(":")[1]
								infoTuple = tmpStrength[ann[1].split(":")[1]]
								cn[dataset][fileName]["relation"][data[0]] = (drugId, infoTuple)
		return cn

	def _reader2009(directory):
		"""
		This private method reads the dataset from I2B2 2009 challenge on medication extraction
		:param directory: Root directory for the dataset
		:return: Dict similar to the method readClinicalNotes
		"""
		cn = {}
		cn["train"] = {}
		allCNs = sorted(glob.glob('{}train.test.released.8.17.09/*'.format(directory)))
		for file in allCNs:
			fileName = file.split("/")[-1]
			cn["train"][fileName] = {}
			with codecs.open(file, 'r', encoding='utf8') as fp:
				cn["train"][fileName]["cn"] = fp.read()

		allAnn = sorted(glob.glob('{}converted.noduplicates.sorted/*.{}'.format(directory, "m")))
		for file in allAnn:
			"""
				"annotation":{
					"id":("concept","type",[(span,span), ...])
				},
				"relation":{
					"id": (annId1, ("concept","type",[(span,span), ...]))
				}
			"""
			fileName = file.split("/")[-1].split(".")[0]
			cn["train"][fileName]["annotation"] = {}
			cn["train"][fileName]["relation"] = {}
			tmpStrength = {}

			#m="ace inhibitor" 149:6 149:7||do="nm"||mo="nm"||f="nm"||du="nm"||r="nm"||ln="narrative"
			#1.medication name and its offset (marker “m”) 
			#2.dosage and its offset (marker “do”) 
			#3.mode/route of administration and its offset (marker “mo”)
			idx = 0
			relIdx = 0
			with codecs.open(file, 'r', encoding='utf8') as fp:
				annotations = fp.read().split("\n")
				for line in annotations:
					data = line.split("||")
					conceptData = data[0].split('"')
					if len(conceptData) > 2:
						concept = conceptData[1]
						firstSpan = conceptData[2].strip().split()[0]
						span = getSpan2019(cn["train"][fileName]["cn"], firstSpan)
						cn["train"][fileName]["annotation"][str(idx)] = (concept, "Drug", span)
						
						dosageData = data[1].split('"')
						dosage = dosageData[1]
						if dosage != "nm":
							dosageSpan = []
							if len(dosageData) > 2:
								dosageSpan = getSpan2019(cn["train"][fileName]["cn"], dosageData[2])
							cn["train"][fileName]["relation"][str(relIdx)] = (str(idx), (dosage,"Strength",dosageSpan))
							relIdx += 1

						routeData = data[2].split('"')
						route = routeData[1]
						if route != "nm":
							routeSpan = []
							if len(routeData) == 2:
								routeSpan = getSpan2019(cn["train"][fileName]["cn"], routeData[2])
							cn["train"][fileName]["relation"][str(relIdx)] = (str(idx), (route,"Route",routeSpan))
							relIdx += 1

						idx += 1
		return cn

	def _readerExamples(directory):
		"""
		This private method reads the example dataset provided in the repository
		:param directory: Root directory for the dataset
		:return: Dict similar to the method readClinicalNotes
		"""
		cn = {}
		cn["train"] = {}
		allCNs = sorted(glob.glob('{}*'.format(directory)))
		for file in allCNs:
			fileName = file.split("/")[-1].split(".")[0]
			cn["train"][fileName] = {}
			with codecs.open(file, 'r', encoding='utf8') as fp:
				cn["train"][fileName]["cn"] = fp.read()
		return cn



def getSpan2019(cn, spanText):
	"""
	This method converts the span annotation line/word into character span
	:param cn: Original clinical note text
	:param spanText: Original span text (i.e. 5:2 means line 5, word 2)
	:return: List containing the character span
	"""
	lines = cn.split("\n")
	try:
		lineToReach = int(spanText.split(":")[0])
		wordToReach = int(spanText.split(":")[1])
	except:
		return []

	lineCount = 0
	span = 0
	for line in lines:
		lineCount += 1
		if lineCount < lineToReach:
			span += len(line) + 1 #\n
		else:
			words = line.split()
			wordCount = 0
			for word in words:
				if wordCount < wordToReach:
					span += len(word) + 1 #space
				else:
					return [span]
				wordCount += 1
	return []