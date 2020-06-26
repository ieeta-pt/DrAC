

def hasNumbers(inputString):
	return bool(re.search(r'\d', inputString))

def startsWithNumbers(inputString):
	return inputString[:1].isdigit() 

class Utils():
	def mergeAnnsToGetStrength(filterAnn):
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

	def getSentence(annSpan, clinicalNote):
		sentences = clinicalNote.replace("\n", ".").split(".")
		spanCounter = 0
		for sentence in sentences:
			spanCounter += len(sentence) + 1
			if spanCounter > annSpan:
				return sentence

	def getSentenceFromSentencesDict(annSpan, clinicalNoteSentenceDict):
		validSpanKey = 0
		for key, _ in clinicalNoteSentenceDict.items():
			if key < annSpan:
				validSpanKey = key
		return validSpanKey, clinicalNoteSentenceDict[validSpanKey]
