
class Writer():
	def writeMatrix(annotations, location):
		"""
		This method writes the matrix with all the information extracted
		First column: Patient id
		Remaining columns: medications
		:param annotations: Dict with the drug and dosage/strength present in each file, by dataset. Drugs without strength will have the value yes
			{
				"train":{
					"file name":{
						"concept":"dosage/strength/yes"
					}
				}
				"test":{...}
			}
		:param location: It is the location to write the matrix.
		"""
		for dataset in annotations:#We created two matrix (test and train)
			matrix = Writer._buildMatrix(annotations[dataset])
			out = open("{}{}_matrix.tsv".format(location, dataset), "w", encoding='utf8')
			for line in matrix:
				tmpLine = ""
				for entry in line:
					tmpLine += entry + "\t"
				tmpLine = tmpLine[:-1] + "\n"
				out.write(tmpLine)
			out.close()

	def _buildMatrix(annotations):
		"""
		This private method create the matrix with all the information extracted
		:param annotations: Dict with the drug and dosage/strength present in each file.
			{
				"file name":{
					"concept":"dosage/strength/yes"
				}
			}
		:return: List of lists creating the matrix
			[["fileName","concept1","concept2","concept3",...]
			 ["fileID1", "dosage", "", "",...]]
		"""
		matrix = [["fileName"]]
		#Create matrix headers
		for file in annotations:
			for concept in annotations[file]:
				if concept not in matrix[0]:
					matrix[0].append(concept)
		#Collect measurements
		index = 0
		for file in annotations:
			index += 1
			matrix.append([file]+["" for i in range(len(matrix[0]))])
			for concept in annotations[file]:
				dosage = annotations[file][concept].replace("\t", " ")#just in case
				conPos = matrix[0].index(concept)
				matrix[index][conPos] = dosage
		return matrix

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
				out.write("{}|{}|{}|{}\n".format(fileName, ann[0],ann[1],ann[2]))
		out.close()

