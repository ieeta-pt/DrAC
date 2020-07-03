import json
import requests
import glob
import codecs
import re
from Utils import Utils
from Vocabulary import Vocabulary

#Flags to simplify the organization of theinformation in the list
STRENGHT = 0
DOSAGE = 1
ROUTE = 2
#QUANTITY = 3
SPAN = 3

class Annotator():
	def annotate(clinicalNotes):
		"""
		This method annotates the clinical notes in the dataset using Neji with the vocabularies created.
		:param clinicalNotes: Dict of clinical notes with the following structure
			{
				"train":{
					"file name"":{
						"cn": "clinical note",
						"annotation":{
							"id":("concept",[(span,span), ...])
						},
						"relation":{
							"id": (annId1, ("concept","type",[(span,span), ...]))
						}
					}
				}
				"test":{...}
			}
		:return: Dict with the neji annotations, key is the dataset (train or test), value is another dict containing the
		files name as key and a list of annotations. The annotations have the following structure: date|UMLS:C2740799:T129:DrugsBank|10
			{
				"train":{
					"file name"":["annotation"]
				}
				"test":{...}
			}
		"""
		url = "https://bioinformatics.ua.pt/nejiws/annotate/Drugs/annotate"
		headers = {'Content-Type': 'application/json; charset=UTF-8'}
		annotations = {}
		annotations["train"] = {}
		for fileName in clinicalNotes["train"]:
			print(fileName)
			try:
				text = clinicalNotes["train"][fileName]["cn"]
				payload = json.dumps({"text": "%s" % text.lower()}, ensure_ascii=True).encode('utf-8')
				response = requests.request("POST", url, data=payload, headers=headers)
				results = json.loads(response.text)
				results = results['entities']
				annotations["train"][fileName] = []
				for ann in results:
					ann = tuple(ann.split("|"))
					annotations["train"][fileName].append(ann)
			except Exception as e:
				print(e)
		return annotations

	def readNejiAnnotations(location):
		"""
		This method reads the neji annotations done previously.
		The file contant has the following structure:
			file name|concept|neji code|inital span
		Example:
			100035|date|UMLS:C2740799:T129:DrugsBank|10
		:param location: Directory to write the annotations
		:return: Dict with the neji annotations, key is the dataset (train or test), value is another dict containing the
		files name as key and a list of annotations. The annotations have the following structure: date|UMLS:C2740799:T129:DrugsBank|10
			{
				"train":{
					"file name"":["annotation"]
				}
				"test":{...}
			}
		"""
		nejiAnnFiles = sorted(glob.glob('{}*nejiann.tsv'.format(location)))
		ann = {}
		for file in nejiAnnFiles:
			dataset = file.split("/")[-1].split("_")[0]
			ann[dataset] = {}
			with codecs.open(file, 'r', encoding='utf8') as fp:
				annotations = fp.read().strip().split("\n")
				for annotation in annotations:
					#file name|concept|neji code|inital span
					data = annotation.split("|")
					fileName = data[0]
					nejiann = tuple(data[1:])
					if fileName not in ann[dataset]:
						ann[dataset][fileName] = []
					ann[dataset][fileName].append(nejiann)
		return ann

	def posProcessing(clinicalNotes, nejiAnnotations, vocabularies):
		"""
		:param clinicalNotes: Dict of clinical notes with the following structure (but only the "cn" from each file will be used)
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
		:param nejiAnnotations: Dict with the annotations, key is the dataset (train or test), value is another dict containing the
		files name as key and a list of annotations. The annotations have the following structure: date|UMLS:C2740799:T129:DrugsBank|10
			{
				"train":{
					"file name"":["annotation"]
				}
				"test":{...}
			}
		:param vocabularies: Vocabularies to be used in the post processing
		:return: Dict with the drug and strenght/dosage/quantity/route/span (list) present in each file, by dataset.
			{
				"train":{
					"file name"":{
						("concept", annSpan):[strenght, dosage, route, quantity]
					}
				}
				"test":{...}
			}
		"""
		voc = Vocabulary.readPostProcessingVoc(vocabularies)
		annotations = {}
		for dataset in nejiAnnotations:
			annotations[dataset] = {}
			for file in nejiAnnotations[dataset]:
				annotations[dataset][file] = {}
				clinicalNote = clinicalNotes[dataset][file]["cn"]
				annotation = sorted(nejiAnnotations[dataset][file], key=lambda x: int(x[2]))
				annotation = Utils.cleanConceptBegin(annotation)
				disambiguatedAnn = Utils.disambiguate(annotation)
				filteredAnn = Annotator._filter(disambiguatedAnn, Utils.getVocListWithoutGroup(voc["all"]))#voc["black-list"]))
				if len(filteredAnn) > 0:
					sentences = Utils.getSentencesByAnnotation(clinicalNote, filteredAnn)

					readedSpans = []
					for (annConcept, annCode, annSpan) in filteredAnn:
						results = [None, None, None, None]
						if annSpan in readedSpans:
							continue
						readedSpans.append(annSpan)
						
						if int(annSpan) not in sentences:
							continue 
						results[ROUTE] = Annotator._annotateRoute(sentences[int(annSpan)], voc["route-complex"], voc["route"])

						#if "fluids" in annConcept.lower():
						#	print(file, results[ROUTE], annSpan, sentences[int(annSpan)])

						if results[ROUTE] != None:
							filterAnn = [(concept, code, span) for (concept, code, span) in annotation if span == annSpan and concept is not None]
							if len(filterAnn) > 1:
								drug, dosage = Utils.mergeAnnsToGetStrength(filterAnn)
								# if "docusate sodium" in annConcept.lower(): print(drug, dosage)
								if drug:
									results[STRENGHT] = dosage
							else:
								drug = filterAnn[0][0]

							# if "docusate sodium" in annConcept.lower(): print(drug)

							##if results[STRENGHT] == None:
							##	results[STRENGHT] = Annotator._annotateStrenght(drug, sentence, voc["strenght"])
							##results[DOSAGE] = Annotator._annotateDosage(drug, sentence, voc["all"])
							#results[QUANTITY] = Annotator._annotateQuantity(filterAnn[0], sentence, results[ROUTE])
							
							#results[SPAN] = [annSpan]

							annotations[dataset][file][(drug, annSpan)] = results

		return annotations
	
	def _filter(annotations, vocList):
		"""
		This method filters the annotations by removing the concepts in the voc[black-list]
		:param annotations: This are the disambiguated annotations following the same format (see posProcessing method for more details)
		:param voc: The vocabulary with the concepts to remove
		:return: The annotations filtered using the same format as the input
		"""
		results = []
		for ann in annotations:
			if ann[0] not in vocList:
				results.append(ann)
		return results

	def _annotateRoute(sentence, complexVoc, voc):
		"""
		This method annotates the drug route in the setence that the concept was found.
		:param sentence: The list of 10 or less word that are after the concept
		:param complexVoc: The vocabulary of routes with more than one word, list of tuples (concept, type)
		:param voc: The vocabulary to use in a list of tuples (concept, type)
		:return: Tuple with Route or None and route span counter
		"""
		route = []
		for entry, group in complexVoc:
			search = " {} ".format(entry.lower())
			if search in " ".join(sentence):
				return entry

		for entry, group in voc:
			search = entry.lower()
			if search in sentence:
				if "other" in group:
					group = "zzzz" #To be the last option in the list
				route.append((entry, group))
		if len(route) > 1:
			route = sorted(route, key=lambda e: (e[1], -len(e[0])))
			return route[0][0]
		if len(route) == 1:
			return route[0][0]
		return None

	def _annotateQuantity(concept, sentence, route):
		#NOT USED
		return None

	def _annotateStrenght(concept, sentence, strenght):
		sentence = "teste 500/200 mg per day"
		DECIMAL_NUM   = "(?:\\d+,)?\\d+(?:\\.\\d+)?(?:(?: |-)?(?:-|to)(?: |-)?(?:\\d+,)?\\d+(?:\\.\\d+)?)?"
		STRENGTH_UNIT = "mg/dl|mg/ml|g/l|milligrams|milligram|mg|grams|gram|g|micrograms|microgram|mcg|meq|iu|cc|units|unit|tablespoons|tablespoon|teaspoons|teaspoon"
		strength = re.compile(r"\b(%s/)?(%s)(\s+|-)?(%s)\b" %(DECIMAL_NUM, DECIMAL_NUM, STRENGTH_UNIT), re.IGNORECASE)
		x = strength.search(sentence)
		if x:
			#print(dir(x.groupdict))
			#print(x.groups())
			pass
		return None

	def _annotateDosage(concept, sentence, strenght):
		"""
		:return: The dosage/quantity of the drug taken by the patient
			two tablets -> 2
		"""
		DECIMAL_NUM   = "(?:\\d+,)?\\d+(?:\\.\\d+)?(?:(?: |-)?(?:-|to)(?: |-)?(?:\\d+,)?\\d+(?:\\.\\d+)?)?"
		volume = re.compile(r"\b(%s)\s+(ml)\b" %DECIMAL_NUM, re.IGNORECASE)
		x = volume.search(sentence)
		if x:
			pass
			#print(dir(x.groupdict))
			#print(x.groups())
			#['__class__', '__copy__', '__deepcopy__', '__delattr__', '__dir__', '__doc__', 
			#'__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', 
			#'__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', 
			#'__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', 
			#'__subclasshook__', 'end', 'endpos', 'expand', 'group', 'groupdict', 'groups', 
			#'lastgroup', 'lastindex', 'pos', 're', 'regs', 'span', 'start', 'string']



			#		"concept":
			#patient:[strenght, dosage, route, [annSpann]]
			#patient:[5mg, 2, route, [annSpann]]
		return None