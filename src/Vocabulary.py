import codecs

class Vocabulary():
	def create(vocSettings):
		"""
		This method creates the vocabularies to insert in the Neji annotator.
		We created more than one vocabulary, for different purposes
		:param vocSettings: Dict of settings for the vocabularies 
		:return: Dict with all the vocabularies, key is the file name and the value is a list of entries.
	 		{
				"fileName":{"UMLS:CUI:TUI":[List of concepts]},
				...
			}
		"""
		vocabularies = {}
		cuiToTui = Vocabulary._relationWithCUIandTUI(vocSettings["mrsty"])
		vocabularies["UMLS_RXNorm"] = Vocabulary._createRXNorm(vocSettings["rxnorm"], cuiToTui)
		#...
		return vocabularies

	def _relationWithCUIandTUI(mrsty):
		"""
		This method creates the dict with the relation between CUIs ans TUIs
		:param mrsty: File location to read this relation
		:return: Dict with the relations, key is the CUI and value is the TUI
			{
				"CUI":"TUI",
			}
		"""
		cuiToTui = {}
		with codecs.open(mrsty, 'r', encoding='utf8') as fp:
			for line in fp:
				line = line.strip().lower().split("|")
				cui = line[0]
				tui = line[1]
				cuiToTui[cui] = tui
		return cuiToTui

	def _createRXNorm(rxnorm, cuiToTui):
		"""
		This private method creates the vocabulary based on the UMLS RXNorm
		:param rxnorm: File location to read RXNorm concepts
		:param cuiToTui: Output from the method _relationWithCUIandTUI
		:return: Dict with the vocabulary ready to be written, key is UMLS:CUI:TUI and value is the list of concepts
			{
				"UMLS:CUI:TUI":[List of concepts],
			}
		"""
		voc = {}
		with codecs.open(rxnorm, 'r', encoding='utf8') as fp:
			for line in fp:
				line = line.strip().lower().split("|")
				cui = line[0]
				desc = line[14]
				if cui in cuiToTui:
					cuiTui = "UMLS:{}:{}".format(cui, cuiToTui[cui])
					if cuiTui not in voc:
						voc[cuiTui] = []
					voc[cuiTui].append(desc)
		return voc


