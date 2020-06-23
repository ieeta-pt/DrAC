from Tables.BaseTable import BaseTable
from sqlalchemy import create_engine
import pandas as pd
import glob

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
		:return: Dict with both matrix
		"""
		allMatrix = {}
		for dataset in annotations:#We created two matrix (test and train)
			matrix = Writer._buildMatrix(annotations[dataset])
			allMatrix[dataset] = matrix
			out = open("{}{}_matrix.tsv".format(location, dataset), "w", encoding='utf8')
			for line in matrix:
				tmpLine = ""
				for entry in line:
					tmpLine += entry + "\t"
				tmpLine = tmpLine[:-1] + "\n"
				out.write(tmpLine)
			out.close()
		return allMatrix

	def _buildMatrix(annotations):
		"""
		This private method create the matrix with all the information extracted
		:param annotations: Dict with the drug and dosage/strength present in each file.
			{
				"file name":{
					"concept":[dosage, quantity, route, [annSpann]]
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
				if concept not in matrix[0] and concept is not None:
					matrix[0].append(concept)
		#Collect measurements
		index = 0
		for file in annotations:
			index += 1
			matrix.append([file]+["" for i in range(len(matrix[0]))])
			for concept in annotations[file]:
				if concept is not None:
					conceptsInfo = annotations[file][concept]
					cell = ""
					for entry in conceptsInfo:
						if entry and isinstance(entry, str):
							cell += entry + "|"
					if len(cell) > 0:
						cell = cell[:-1]
					conPos = matrix[0].index(concept)
					matrix[index][conPos] = cell
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

	def writeVocabularies(dbSettings, ohdsiVocabularies):
		"""
		THis method reads the OHDSI Vocabulaires in CSV files and write them in the database
		:param dbSettings: Dict with all the fields to connect with the database (settings["database"])
		:param ohdsiVocabularies: Location of the OHDSI Vocabularies
		"""
		#I may need to change this due to huge files see: https://pythondata.com/working-large-csv-files-python/
		engine = create_engine(dbSettings["datatype"]+"://"+dbSettings["user"]+":"+dbSettings["password"]+"@"+dbSettings["server"]+":"+dbSettings["port"]+"/"+dbSettings["database"])
		vocabulariesFiles = glob.glob('{}*.{}'.format(ohdsiVocabularies, "csv"))
		if not vocabulariesFiles:
			print("The directory does not have any vocabularies to read")
		for file in vocabulariesFiles:
			table = file.split("/")[-1].split(".")[0].lower()
			print("Loading {} table...".format(table))
			fileContent = pd.read_csv(file, na_values='null', sep="\t")
			fileContent.to_sql(table, engine, if_exists 	= 'replace',
												 index 		= False,
												 schema 	= dbSettings["schema"],
												 dtype 		= BaseTable.getDataTypesForSQL(table))
