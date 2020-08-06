from Tables.DrugExposure import DrugExposure
from Tables.Note import Note
from Tables.NoteNLP import NoteNLP
from Tables.BaseTable import BaseTable
from sqlalchemy import create_engine
import pandas as pd
import glob

class Writer():
	def writeMatrix(annotations, location):
		"""
		This method writes the matrix with all the information extracted and returns a dict with the matrix for each dataset (train and test if they exist)
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
		:param location: It is the location where to write the matrix file.
		:return: Dict with both matrices
		"""
		allMatrix = {}
		for dataset in annotations:#We created two matrices (test and train)
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
					("concept", annSpan):[dosage, quantity, route]
				}
			}
		:return: List of lists creating the matrix
			[["fileName","concept1","concept2","concept3",...]
			 ["fileID1", "dosage", "", "",...]]
		"""
		matrix = [["fileName"]]
		#Create matrix headers
		for file in annotations:
			for concept, span in annotations[file]:
				if concept not in matrix[0] and concept is not None:
					matrix[0].append(concept)
		#Collect measurements
		index = 0
		for file in annotations:
			index += 1
			matrix.append([file]+["" for i in range(len(matrix[0]))])
			for concept, span in annotations[file]:
				if concept is not None:
					conceptsInfo = annotations[file][(concept, span)]
					cell = ""
					for entry in conceptsInfo:
						if entry and isinstance(entry, str):
							cell += entry + "|"
						elif entry is None:
							cell += "|"
					if len(cell) > 0:
						cell = cell[:-1]
					conPos = matrix[0].index(concept)
					matrix[index][conPos] = cell
		return matrix

	def writeVocabularies(vocabularies, location):
		"""
		This method writes the vocabularies in the "location" directory.
		:param vocabularies: Dict containing all the vocabularies, key is the vocabulary name, value is the dict with the vocabulary
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
		:param location: The location where to write all the vocabularies.
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
		This method writes the Neji annotations by dataset. Since the system performs calls for each note to the Neji server,
		which can be a time consuming process, the annotations are stored in the disk so that they can be reused during system development.
		The output of this file has the following structure:
			file name|concept|neji code|inital span
		Example:
			100035|date|UMLS:C2740799:T129:DrugsBank|10
		:param nejiAnnotations: Dict with the Neji annotations, key is the dataset (train or test), value is another dict containing the
		files name as key and a list of annotations. The annotations have the following structure: date|UMLS:C2740799:T129:DrugsBank|10
			{
				"train":{
					"file name"":["annotation"]
				}
				"test":{...}
			}
		:param location: Directory to write the Neji annotations
		"""
		#for dataset in nejiAnnotations:
		out = open("{}{}_nejiann.tsv".format(location, "train"), "w", encoding='utf8')
		for fileName in nejiAnnotations["train"]:
			for ann in nejiAnnotations["train"][fileName]:
				out.write("{}|{}|{}|{}\n".format(fileName, ann[0],ann[1],ann[2]))
		out.close()

	def writeOHDSIVocabularies(dbSettings, ohdsiVocabularies):
		"""
		This method reads the OHDSI Vocabularies in CSV files and write them in the database
		:param dbSettings: Dict with all the fields to establish a connection with the database (settings["database"])
		:param ohdsiVocabularies: Location of the OHDSI Vocabularies
		"""
		#I may need to change this due to huge files see: https://pythondata.com/working-large-csv-files-python/
		engine = create_engine(dbSettings["datatype"]+"://"+dbSettings["user"]+":"+dbSettings["password"]+"@"+dbSettings["server"]+":"+dbSettings["port"]+"/"+dbSettings["database"])
		vocabulariesFiles = glob.glob('{}*.{}'.format(ohdsiVocabularies, "csv"))
		if not vocabulariesFiles:
			print("The directory does not have any vocabularies to read.")
		for file in vocabulariesFiles:
			table = file.split("/")[-1].split(".")[0].lower()
			print("Loading {} table...".format(table))
			fileContent = pd.read_csv(file, na_values='null', sep="\t")
			fileContent.to_sql(table, engine, if_exists 	= 'replace',
												 index 		= False,
												 schema 	= dbSettings["schema"],
												 dtype 		= BaseTable.getDataTypesForSQL(table))

	def writeMigratedDataDB(dbSettings, tables):
		"""
		This method reads the migrated data in CSV files and write them in the database
		:param dbSettings: Dict with all the fields to establish a connection with the database (settings["database"])
		:param tables: Location of the migrated tables (Drug_Exposure, etc.)
		"""
		#I may need to change this due to huge files see: https://pythondata.com/working-large-csv-files-python/
		engine = create_engine(dbSettings["datatype"]+"://"+dbSettings["user"]+":"+dbSettings["password"]+"@"+dbSettings["server"]+":"+dbSettings["port"]+"/"+dbSettings["database"])
		for key in tables:
			file = tables[key]
			table = file.split("/")[-1].split(".")[0].lower()
			print("Loading {} table...".format(table))
			fileContent = pd.read_csv(file, na_values='null', sep="\t")
			fileContent.to_sql(table, engine, if_exists 	= 'replace',
												 index 		= False,
												 schema 	= dbSettings["schema"],
												 dtype 		= BaseTable.getDataTypesForSQL(table))

	def writeUsagiInputs(uniqueConcepts, file):
		"""
		This method reads the unique concepts with their respective routes and writes them in the "file"
		:param uniqueConcepts: Contains entries with unique concepts and respective routes
		:param file: file used to write the list of unique concepts and routes
		"""
		concepts, routes = uniqueConcepts
		out = open(file, "w", encoding='utf8')
		out.write("source\n")
		for concept in concepts:
			out.write(concept+"\n")
		out.write("---\n")
		for route in routes:
			out.write(route+"\n")
		out.close()

	def writeMigratedDataCSV(tables, locations):
		"""
		This method writes the OMOP CDM tables provided in "tables" to the respective directories provided in locations
		:param tables: tables in the OMOP CDM data schema
		:param locations: directories where each table should be saved
		"""
		for table in locations:
			print(table)
			out = open(locations[table], "w", encoding='utf8')

			fileHeaders = ""
			if table == "drug_exposure":
				for x in DrugExposure.columns:
					fileHeaders += "{}\t".format(x)
			elif table == "note":
				for x in Note.columns:
					fileHeaders += "{}\t".format(x)
			elif table == "note_nlp":
				for x in NoteNLP.columns:
					fileHeaders += "{}\t".format(x)


			fileHeaders = fileHeaders[:-1] + "\n"
			out.write(fileHeaders)
			for elem in tables[table]:
				out.write(elem.getRow() + "\n")
			out.close()