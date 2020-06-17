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
		:return: todo
		"""
		url = "https://bioinformatics.ua.pt/nejiws/annotate/Disorders/annotate"
		headers = {'Content-Type': 'application/json; charset=UTF-8'}
		for fileName in clinicalNotes["train"]:
			text = clinicalNotes["train"][fileName]["cn"]
			payload = json.dumps({"text": "%s" % text.lower()}, ensure_ascii=True).encode('utf-8')
			response = requests.request("POST", url, data=payload, headers=headers)
			results = json.loads(response.text)
			print(results)
			results = results['entities']
			print(results)
		return None