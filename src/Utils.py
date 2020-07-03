import re

drugRegex = re.compile("[^\d]+(?=( \d+))", re.IGNORECASE)

def hasNumbers(inputString):
	return bool(re.search(r'\d', inputString))

def startsWithNumbers(inputString):
	return inputString[:1].isdigit() 

class Utils():
	# def mergeAnnsToGetStrength(filterAnn):
	# 	sub = ""
	# 	concepts = set()
	# 	for con in filterAnn:
	# 		concepts.add(con[0])
	# 	concepts = list(concepts)
	# 	if len(concepts) == 2:
	# 		concept1 = concepts[0]
	# 		concept2 = concepts[1]
	# 		if concept1 in concept2:
	# 			sub = concept2.replace(concept1, "").strip()
	# 			drug = concept1
	# 			if concept2 in concept1:
	# 			sub = concept1.replace(concept2, "").strip()
	# 			drug = concept2
	# 	elif len(concepts) > 2:
	# 		print("More than 2 in _mergeAnns (Unusual, but check)")
	# 	if startsWithNumbers(sub):
	# 		return drug, sub
	# 	return None, None

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
				match = drugRegex.search(concept2)
				if match is None:
					drug = concept2
					sub = None
				else:
					drug = match[0]
					sub = concept2.replace(drug, "").strip()
			elif concept2 in concept1:
				match = drugRegex.search(concept1)
				if match is None:
					drug = concept1
					sub = None
				else:
					drug = match[0]
					sub = concept1.replace(drug, "").strip()
			return drug, sub

		elif len(concepts) > 2:
			print("More than 2 in _mergeAnns (Unusual, but check)")
		return None, None

	def getSentencesByAnnotation(clinicalNote, annotation):
		"""
		This method returns the teen (or less) words after the concepts annotated (inclusivly)
		If there is another concept in the teen words, the set is interrupted and the new words
		are associated to this new concept.
		:param clinicalNote: The clinical note to process without any pre-processing
		:param annotation: The neji annotation with the following structure: (annConcept, annCode, annSpan)
		:return: Dict with key the span of the concept and value a list of words that followed the concept.
		"""
		result = {}
		MAX = 16 #means 15
		LAST = False
		readedSpans = set()
		for (annConcept, annCode, annSpan) in annotation:
			readedSpans.add(int(annSpan))
		readedSpans = list(readedSpans)
		readedSpans.sort()

		span = 0
		currentConceptSpan = readedSpans[0]
		nextConceptSpan = readedSpans[1]
		readedSpansCounter = 1
		counter = 0
		clinicalNote = clinicalNote.replace("\n", " ")
		for word in clinicalNote.split(" "):
			if span >= nextConceptSpan and nextConceptSpan <= span+len(word):
				readedSpansCounter += 1
				currentConceptSpan = nextConceptSpan
				if not LAST:
					counter = 0
				if readedSpansCounter >= len(readedSpans):
					LAST = True
				else:
					nextConceptSpan = readedSpans[readedSpansCounter]

			if 	(span >= currentConceptSpan and span < nextConceptSpan and counter < MAX) or \
				(LAST and counter < MAX):
				if currentConceptSpan not in result:
					result[currentConceptSpan] = []
				result[currentConceptSpan].append(word.lower())
				counter += 1
			span += len(word) + 1
		return result

	def getVocListWithoutGroup(voc):
		"""
		This method creates a list of concepts from a vocabulary and removes the group.
		:param voc: List of tuples (concept, group)
		:return: List of concepts
		"""
		results = []
		for entry, group in voc:
			results.append(entry)
		return results

	def disambiguate(annotation):
		"""
		This method disambiguates annotations by giving more priority to the RXNorm concepts
		:param annotation: The annotation received from neji: dict with the annotations, key is the dataset (train or test), value is another dict containing the
		files name as key and a list of annotations. The annotations have the following structure: date|UMLS:C2740799:T129:DrugsBank|10
			{
				"train":{
					"file name"":["annotation"]
				}
				"test":{...}
			}
		:return: The annotations following the same format as the input withou overlap spans
		"""
		overlapsDict = {}
		overlapList = []
		results = []
		index = 1
		for ann in annotation:
			if ann in overlapList:
				continue
			notOverlaped =  True 
			startSpan = int(ann[2])
			endSpan = startSpan + len(ann[0])
			annSpanRange = range(startSpan, endSpan)
			for annNext in annotation[index:]:
				startSpanNext = int(annNext[2])
				endSpanNext = startSpanNext + len(annNext[0])
				annSpanNextRange = range(startSpanNext, endSpanNext)
				if len(set(annSpanRange).intersection(annSpanNextRange)) > 0:
					if startSpan not in overlapsDict:
						overlapsDict[startSpan] = []
					overlapsDict[startSpan].append(annNext)
					notOverlaped = False
					overlapList.append(annNext)
			if notOverlaped:
				results.append(ann)
			else:
				overlapsDict[startSpan].append(ann)
			index += 1

		for overlaps in overlapsDict:
			tmpAnn = overlapsDict[overlaps][0]
			for ann in overlapsDict[overlaps]:
				if len(ann[0]) > len(tmpAnn[0]):
					tmpAnn = ann
			results.append(tmpAnn)
		return results