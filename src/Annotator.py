import json
import requests
import glob
import codecs
from Utils import Utils
from Vocabulary import Vocabulary

import re
from nltk.tokenize import PunktSentenceTokenizer

#Flags to simplify the organization of theinformation in the list
DOSAGE = 0
QUANTITY = 1
ROUTE = 2
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
		:return: Dict with the drug and dosage/quantity/route/span (list) present in each file, by dataset.
			{
				"train":{
					"file name"":{
						"concept":[dosage, quantity, route, annSpann]
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
				readedSpans = []

				clinicalNote = re.sub(r'\n', ' ', clinicalNote) # re.sub(r'(?![\w ])\n', ' ', clinicalNote)

				# clinicalNote = re.sub(r'[ ]{2,}', '\n', clinicalNote) #THIS RULE IS MORE SPECIFIC AND RUINS THE DIRECT MAPPING FROM SPAN TO ANNOTATION
				# print(clinicalNote)



				clinicalNoteSentencesDict = nltkSentenceSplit(clinicalNote)



				for (annConcept, annCode, annSpan) in annotation:
					results = [None, None, None, None]

					# print("Original annotation: {} {}".format(annConcept, annSpan))
					# print("New annotation: {}".format(clinicalNote[int(annSpan):int(annSpan)+len(annConcept)]))

					if annSpan in readedSpans:
						continue
					readedSpans.append(annSpan)
					# sentence = Utils.getSentence(int(annSpan), clinicalNote)
					initialSpan, sentence = Utils.getSentenceFromSentencesDict(int(annSpan), clinicalNoteSentencesDict)
					# print(sentence[int(annSpan)-int(initialSpan):int(annSpan)-int(initialSpan)+len(annConcept)])
					# print("Original annotation: {} {}".format(annConcept, annSpan))
					# print("New annotation: {}".format(sentence[int(annSpan)-int(initialSpan):int(annSpan)-int(initialSpan)+len(annConcept)]))
					print(file)
					if "docusate sodium" in annConcept.lower():
						print("shit")
						print(initialSpan, annSpan, sentence)
						if "docusate sodium" in sentence.lower():
							print("worked")

					results[ROUTE] = Annotator._annotateRoute(sentence, voc["route"])
					if results[ROUTE] != None:
						filterAnn = [(concept, code, span) for (concept, code, span) in annotation if span == annSpan and concept is not None]
						if len(filterAnn) > 1:
							drug, dosage = Utils.mergeAnnsToGetStrength(filterAnn)
							if drug:
								results[DOSAGE] = dosage
						else:
							drug = filterAnn[0][0]

						if results[DOSAGE] == None:
							results[DOSAGE] = Annotator._annotateDosage(drug, sentence, voc["strenght"])
						results[QUANTITY] = Annotator._annotateQuantity(filterAnn[0], sentence, results[ROUTE])
						results[SPAN] = [annSpan]

						annotations[dataset][file][drug] = results
		return annotations

	def _annotateRoute(sentence, voc):
		"""
		This method annotates the drug route in the setence that the concept was found.
		:param sentence: The sentence to analyze
		:param voc: The vocabulary to use in a list of tuples (concept, type)
		:return: Route or None
		"""
		route = []
		for entry, group in voc:
			search = " {} ".format(entry)
			if search in sentence.lower():
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
		#regex
		return None

	def _annotateDosage(concept, sentence, strenght):
		return None

def nltkSentenceSplit(document):
	sentenceTokenizer = PunktSentenceTokenizer()
	sentences = sentenceTokenizer.span_tokenize(document)
	sentenceDict = dict()

	for beginSpan, endSpan in sentences:
		# print(beginSpan, endSpan, document[beginSpan:endSpan])
		sentenceDict[beginSpan] = document[beginSpan:endSpan]

	return sentenceDict

	# sentences = nltk.sent_tokenize(sentences)
	# return sentences