
class Writer():
	def writeMatrix(annotations):
		pass

	def writeVocabularies(vocabularies, location):
		"""
		This method writes the vocabularies in an location.
		:param vocabularies: Dict containing all the vocabularies, key is the vocabulary name value is the dict with the vocabulary
			{
				"fileName":
				{
					"TUI_Name":
					{
						"UMLS:CUI:TUI:Name":[List of concepts]
					}
				},
				...
			}
		:param location: It is the location to write all the vocabularies.
		"""
		for vocName in vocabularies:
			for tui in vocabularies[vocName]:
				out = open("{}{}_{}.tsv".format(location, vocName, tui), "w")
				for cuiTui in vocabularies[vocName][tui]:
					listOfConcepts = vocabularies[vocName][tui][cuiTui]
					tmpLine = "{}\t".format(cuiTui)
					for concept in listOfConcepts:
						tmpLine += concept + "|"
					tmpLine = tmpLine[:-1] + "\n"
					out.write(tmpLine)
				out.close()