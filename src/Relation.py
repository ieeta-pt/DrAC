import re

def hasNumbers(inputString):
	return bool(re.search(r'\d', inputString))

def startsWithNumbers(inputString):
	return inputString[:1].isdigit() 

class Relation():
	def inferRelations(clinicalNotes, annotations):
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
		:param annotations: Dict with the annotations, key is the dataset (train or test), value is another dict containing the
		files name as key and a list of annotations. The annotations have the following structure: date|UMLS:C2740799:T129:DrugsBank|10
			{
				"train":{
					"file name"":["annotation"]
				}
				"test":{...}
			}
		:return: Dict with the drug and dosage/strength present in each file, by dataset. Drugs without strength will have the value yes
			{
				"train":{
					"file name"":{
						"concept":"dosage/strength/yes"
					}
				}
				"test":{...}
			}
		"""
		annWithRelations  = {}
		for dataset in annotations:
			annWithRelations[dataset] = {}
			for file in annotations[dataset]:
				annWithRelations[dataset][file] = {}
				clinicalNote = clinicalNotes[dataset][file]["cn"]
				annotation = sorted(annotations[dataset][file], key=lambda x: int(x[2]))
				readedSpans = []

				for (annConcept, annCode, annSpan) in annotation:
					if annSpan in readedSpans:
						continue
					readedSpans.append(annSpan)
					filterAnn = [(concept, code, span) for (concept, code, span) in annotation if span == annSpan]
					if len(filterAnn) > 1:
						drug, dosage = Relation._mergeAnnsToGetStrength(filterAnn)
						if drug:
							annWithRelations[dataset][file][drug] = dosage
					#to do
		return annWithRelations

	def _mergeAnnsToGetStrength(filterAnn):
		sub = ""
		concepts = set()
		for con in filterAnn:
			concepts.add(con[0])
		concepts = list(concepts)
		if len(concepts) == 2:
			concept1 = concepts[0]
			concept2 = concepts[1]
			if concept1 in concept2:
				sub = concept2.replace(concept1, "").strip()
				drug = concept1
			if concept2 in concept1:
				sub = concept1.replace(concept2, "").strip()
				drug = concept2
		elif len(concepts) > 2:
			print("More than 2 in _mergeAnns (Unusual, but check)")
		if startsWithNumbers(sub):
			return drug, sub
		return None, None
