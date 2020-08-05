import re

drugRegex = re.compile("[^\d]+(?=( \d+))", re.IGNORECASE)

class Utils():
	def mergeAnnsToGetStrength(filterAnn):
		"""
		This method analyses cases where there exist more than one annotation and tries to identify concept overlap.
		Moreover, it tries to identify the presence of drug strength information in the extracted annotation as RxNorm
		annotations can contain this type of information. If the list of annotations contains more than two annotations,
		the method does not analyse the strings and returns None, None
		:param filterAnn: List of annotation tuples with (annConcept, annCode, annSpan)
		:return: two strings, a first one containing the drug mention and a second one with the strength component of
		 the string, if present. Otherwise, the second element is instead returned as None.
		"""
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
			print("More than 2 concepts in _mergeAnns (Unusual, but check)")
		return None, None

	def getSentencesByAnnotation(clinicalNote, annotation):
		"""
		This method returns the 15 (or less) words after the annotated concept (inclusively)
		If there is another concept in the returned words, the set is interrupted and the new words
		are associated to this new concept.
		:param clinicalNote: The clinical note to process without any pre-processing
		:param annotation: The Neji annotation with the following structure: (annConcept, annCode, annSpan)
		:return: Dict with as key the span of the concept and as value a list of words that follow the concept.
		"""
		result = {}
		AFTER = 16 #means 15
		BEFORE = 2 #Before mention
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

			if 	(span >= currentConceptSpan and span < nextConceptSpan and counter < AFTER) or \
				(LAST and counter < AFTER):
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
		This method disambiguates annotations by giving more priority to RxNorm annotations.
		:param annotation: The annotation received from Neji which is a dict with the annotations,
		where the key is the dataset (train or test), value is another dict containing the
		files name as key and a list of annotations. The annotations have the following structure: date|UMLS:C2740799:T129:DrugsBank|10
			{
				"train":{
					"file name"":["annotation"]
				}
				"test":{...}
			}
		:return: The annotations following the same format as the input without overlapping spans
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

	def cleanConceptBegin(annotation):
		"""
		This method cleans the beginning of the annotations, for instance when there are symbols such as * before the concept
		:param annotation: List with the annotations for a single clinical note
		:return: The input list with cleaned annotations
		"""
		for idx in range(len(annotation)):
			if not annotation[idx][0][0].isalnum():
				ann = list(annotation[idx])
				ann[0] = ann[0][1:]
				ann[2] = str(int(ann[2])+1)
				ann = tuple(ann)
				annotation[idx] = ann
		return annotation

	def createUniqueConcepts(matrix):
		"""
		This method creates a set containing all the mapped concepts to be then used in Usagi.
		:param matrix: Matrix resulting from the annotation process (List of lists)
		:return: Tuple of lists converted from sets of concepts and routes
		"""
		concepts = set()
		for concept in matrix[0]:
			concepts.add(concept.lower())
		routes = set()
		for data in matrix[1:]:
			for elem in data:
				info = elem.split("|")
				if len(info) >= 2:
					routes.add(info[2].lower())
		return list(concepts), list(routes)