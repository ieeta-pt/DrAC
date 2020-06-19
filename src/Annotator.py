import json
import requests
import glob
import codecs

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
					annotations["train"][fileName].append(ann)
			except Exception as e:
				print(e)
		print("TO DO: Validate the annotation structure")
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

	def posProcessing(nejiAnnotations):
		return nejiAnnotations