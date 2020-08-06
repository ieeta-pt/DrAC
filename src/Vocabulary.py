import codecs

class Vocabulary():
	def create(vocSettings):
		"""
		This method creates the vocabularies to insert in the Neji annotator.
		We created more than one vocabulary, for different purposes
		:param vocSettings: Dict of settings for the vocabularies 
		:return: Dict with all the vocabularies, key is the file name, value is a list of entries.
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
		"""
		vocabularies = {}
		cuiToTui = Vocabulary._relationWithCUIandTUI(vocSettings["tuis"])
		vocabularies["UMLS_RxNorm"] = Vocabulary._createSemanticDict(vocSettings["umls_rxnorm"], cuiToTui, "RxNorm")
		#vocabularies["UMLS_All_T200"] = Vocabulary._createAllT200BasedOnRXNorm(vocSettings["rxnorm"])
		vocabularies["UMLS_DrugBank"] = Vocabulary._createSemanticDict(vocSettings["umls_drugbank"], cuiToTui, "DrugBank")
		vocabularies["UMLS_AOD"] = Vocabulary._createSemanticDict(vocSettings["umls_aod"], cuiToTui, "AOD")
		#...
		return vocabularies

	def _relationWithCUIandTUI(tuisFile):
		"""
		This method creates the dict with the relation between CUIs and TUIs
		:param tuisFile: File location to read the relations between CUIs and TUIs
		:return: Dict with the relations, key is the CUI and value is the TUI
			{
				"CUI":("TUI","Name"),
			}
		"""
		cuiToTui = {}
		with codecs.open(tuisFile, 'r', encoding='utf8') as fp:
			for line in fp:
				line = line.strip().split("|")
				cui = line[0]
				tui = line[1]
				name = line[3].replace(" ","_").replace(",","")
				cuiToTui[cui] = (tui, name)
		return cuiToTui

	def _createSemanticDict(filteredUMLS, cuiToTui, name):
		"""
		This private method creates the vocabulary based on the UMLS
		:param filteredUMLS: File location to read filtered UMLS concepts
		:param cuiToTui: Output from the method _relationWithCUIandTUI
		:param name: Vocabulary name to add in Neji
		:return: Dict with the vocabulary ready to be written, key is UMLS:CUI:TUI and value is the list of concepts
			{
				"name":
				{
					"UMLS:CUI:TUI:name":[List of concepts],
				},
			}
		"""
		voc = {}
		with codecs.open(filteredUMLS, 'r', encoding='utf8') as fp:
			for line in fp:
				line = line.strip().split("|")
				cui = line[0]
				desc = line[14].lower()
				if len(desc) >= 3 and cui in cuiToTui:
					cuiName = name#"{}_{}".format(cuiToTui[cui][0], name)
					if cuiName not in voc:
						voc[cuiName] = {}
					cuiTui = "UMLS:{}:{}:{}".format(cui, cuiToTui[cui][0], name)
					if cuiTui not in voc[cuiName]:
						voc[cuiName][cuiTui] = []
					voc[cuiName][cuiTui].append(desc)
		return voc

	def _createAllT200BasedOnRXNorm(rxnorm):
		"""
		This private method creates the vocabulary based on the RxNorm vocabulary without considering
		the TUIs (a default TUI is used for every concept)
		:param rxnorm: File location to read RxNorm concepts
		:return: Dict with the vocabulary ready to be written, key is UMLS:CUI:TUI and value is the list of concepts
			{
				"T200_Drugs":
				{
					"UMLS:CUI:T200:Drugs":[List of concepts],
				},
			}
		"""
		voc = {}
		with codecs.open(rxnorm, 'r', encoding='utf8') as fp:
			for line in fp:
				line = line.strip().split("|")
				cui = line[0]
				desc = line[14].lower()
				cuiTui = "UMLS:{}:T200:Drugs".format(cui)
				if cuiTui not in voc:
					voc[cuiTui] = []
				voc[cuiTui].append(desc)
		return {"T200_Drugs": voc}

	def readPostProcessingVoc(files):
		"""
		This method reads the post processing vocabularies that are in the same format as those used in Neji
		:param files: All the files with the vocabularies defined in the Settings file under the section [post_processing]
		:return: Dict of types of concepts, key is the type (i.e., route, dosage, etc..) and value is list of tuples(concepts, group)
			{
				"route":[("concept", "group")],
				"all":...
			}
		"""
		voc = {}
		voc["all"] = []
		for fileKey in files:
			with codecs.open(files[fileKey], 'r', encoding='utf8') as fp:
				for line in fp:
					line = line.split("\t")
					concType = line[0].split(":")[2].lower()
					group = line[0].split(":")[0].lower()
					if concType not in voc:
						voc[concType] = []
					for concept in line[1].split("|"):
						if len(concept) > 0:
							entry = (concept.strip(), group)
							if entry not in voc["all"]:
								voc["all"].append(entry)
							if entry not in voc[concType]:
								voc[concType].append(entry)
		return voc
