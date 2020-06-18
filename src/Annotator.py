import json
import requests

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
							"id": (type, annId1, annId2)
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
			text = clinicalNotes["train"][fileName]["cn"]
			payload = json.dumps({"text": "%s" % text.lower()}, ensure_ascii=True).encode('utf-8')
			response = requests.request("POST", url, data=payload, headers=headers)
			results = json.loads(response.text)
			results = results['entities']
			annotations["train"][fileName] = []
			for ann in results:
				annotations["train"][fileName].append(ann)
		return annotations