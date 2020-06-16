
class Writer():
	def writeMatrix(annotations):
		pass

	def writeVocabularies(vocabularies, location):
		"""
		This method writes the vocabularies in an location.
		:param vocabularies: Dict containing all the vocabularies, key is the vocabulary name value is the dict with the vocabulary
			{
				"fileName":{"UMLS:CUI:TUI":[List of concepts]},
				...
			}
		:param location: It is the location to write all the vocabularies.
		"""
		for vocName in vocabularies:
			out = open("{}{}.tsv".format(location, vocName), "w")
			for cuiTui in vocabularies[vocName]:
				listOfConcepts = vocabularies[vocName][cuiTui]
				tmpLine = "{}\t".format(cuiTui)
				for concept in listOfConcepts:
					tmpLine += concept + "|"
				tmpLine = tmpLine[:-1] + "\n"
				out.write(tmpLine)
			out.close()