
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
				out = open("{}{}_{}.tsv".format(location, vocName, tui), "w", encoding='utf8')
				for cuiTui in vocabularies[vocName][tui]:
					listOfConcepts = vocabularies[vocName][tui][cuiTui]
					tmpLine = "{}\t".format(cuiTui)
					for concept in listOfConcepts:
						tmpLine += concept + "|"
					tmpLine = tmpLine[:-1] + "\n"
					out.write(tmpLine)
				out.close()

	def writeAnnotations(nejiAnnotations, location):
		"""
		This method writes the neji annotations by dataset.
		Since the system performs calls for each note to the neji server, which takes a while, the annotations are stored in disk
		for reuse during the system development.
		The output of this file has the following structure:
			file name|concept|neji code|inital span
		Example:
			100035|date|UMLS:C2740799:T129:DrugsBank|10
		:param nejiAnnotations: Dict with the neji annotations, key is the dataset (train or test), value is another dict containing the
		files name as key and a list of annotations. The annotations have the following structure: date|UMLS:C2740799:T129:DrugsBank|10
			{
				"train":{
					"file name"":["annotation"]
				}
				"test":{...}
			}
		:param location: Directory to write the annotations
		"""
		#for dataset in nejiAnnotations:
		out = open("{}{}_nejiann.tsv".format(location, "train"), "w", encoding='utf8')
		for fileName in nejiAnnotations["train"]:
			for ann in nejiAnnotations["train"][fileName]:
				out.write("{}|{}\n".format(fileName, ann))
		out.close()

