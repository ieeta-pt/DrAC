import codecs

class Vocabulary():
	def create(vocSettings):
		"""
		This method creates the vocabularies to insert in the Neji annotator.
		We created more than one vocabulary, for different purposes
		:param vocSettings: Dict of settings for the vocabularies 
		:return: Dict with all the vocabularies, key is the file name and the value is a list of entries.
	 		{
				"fileName":[list of vocabularies to write],
				...
			}
		"""
		vocabularies = {}
		print(vocSettings["rxnorm"])
		vocabularies["UMLS_RXNorm"] = Vocabulary._createRXNorm(vocSettings["rxnorm"], vocSettings["mrsty"])
		#...
		return vocabularies

	def _createRXNorm(rxnorm, mrsty):
		voc = {}#key UMLS:CUI:T200:Drugs value list
		with codecs.open(rxnorm, 'r', encoding='utf8') as fp:
			for line in fp:
				line = line.strip().lower().split("|")
				cui = line[0]
				desc = line[14]
				if cui not in voc:
					voc[cui] = []
				voc[cui].append(desc)
		return voc


