import json
import requests
import glob
import codecs
from Utils import Utils

#Flags to simplify the organization of theinformation in the list
DOSAGE = 0
QUANTITY = 1
ROUTE = 2
SIG = 3

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

	def posProcessing(clinicalNotes, nejiAnnotations):
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
		:return: Dict with the drug and dosage/quantity/route/sig (list) present in each file, by dataset.
			{
				"train":{
					"file name"":{
						"concept":[dosage, quantity, route, sig]
					}
				}
				"test":{...}
			}
		"""
		annotations = {}
		for dataset in nejiAnnotations:
			annotations[dataset] = {}
			for file in nejiAnnotations[dataset]:
				annotations[dataset][file] = {}
				clinicalNote = clinicalNotes[dataset][file]["cn"]
				annotation = sorted(nejiAnnotations[dataset][file], key=lambda x: int(x[2]))
				readedSpans = []

				for (annConcept, annCode, annSpan) in annotation:
					results = [None, None, None, None]
					if annSpan in readedSpans:
						continue
					readedSpans.append(annSpan)
					filterAnn = [(concept, code, span) for (concept, code, span) in annotation if span == annSpan]
					if len(filterAnn) > 1:
						drug, dosage = Utils.mergeAnnsToGetStrength(filterAnn)
						if drug:
							results[DOSAGE] = dosage
							
					sentence = Utils.getSentence(int(annSpan), clinicalNote)
					results[ROUTE] = Annotator._annotateRoute(filterAnn[0], sentence)
					results[QUANTITY] = Annotator._annotateQuantaty(filterAnn[0], sentence, results[ROUTE])
					results[SIG] = Annotator._identifySig(filterAnn[0], sentence, results[ROUTE], results[QUANTITY])

					if results[DOSAGE] != None or results[QUANTITY] != None or results[ROUTE] != None or results[SIG] != None:
						annotations[dataset][file][drug] = results
		return annotations

	def _annotateRoute(concept, sentence):
		return None

	def _annotateQuantaty(concept, sentence, route):
		return None

	def _identifySig(concept, sentence, route, quantity):
		return None