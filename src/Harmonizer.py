from Tables.DrugExposure import DrugExposure

#Positional flags
#drug_exposure_id = 0
#person_id = 1
#drug_concept_id = 2
#drug_exposure_start_date = 3
#drug_exposure_start_datetime = 4
#drug_exposure_end_date = 5
#drug_exposure_end_datetime = 6
#verbatim_end_date = 7
#drug_type_concept_id = 8
#stop_reason = 9
#refills = 10
#quantity = 11
#days_supply = 12
#sig = 13
#route_concept_id = 14
#lot_number = 15
#provider_id = 16
#visit_occurrence_id = 17
#visit_detail_id = 18
#drug_source_value = 19
#drug_source_concept_id = 20
#route_source_value = 21
#dose_unit_source_value = 22

class Harmonizer():
	def harmonize(matrix, usagiOutput):
		"""
		This method is used in the system's Migration mode and 1) harmonizes the concepts in the matrix to their standard definition,
		2) migrates harmonized data into the OMOP CDM schema, and 3) saves it a CSV file.
		The mappings used for the harmonization procedure must be previously validated in the Usagi tool, before being used in this method.
		:param matrix: matrix with extracted information from the annotation component
		:param usagiOuput: CSV file with concept mappings that were validated and exported from Usagi
		"""
		headers = matrix[0]
		stdConcepts = Harmonizer._harmonizedConcepts(usagiOutput) #dict
		data = matrix[1:]
		listOfValues = []
		counter = 0
		print(headers)
		for rawD in data:#x is a list (raw in the matrix)
			pid = rawD[0]
			idx = 0
			for cell in rawD:
				if idx > 0: #ignore first
					if len(cell) == 0:
						pass
					else:
						concept = headers[idx]
						route = cell.split("|")[2].lower()
						if concept not in stdConcepts or route not in stdConcepts:
							print(idx)
						else:
							stdConcept = stdConcepts[concept]
							stdRoute = stdConcepts[route]

							elem = DrugExposure(drug_exposure_id = counter,
												person_id = pid,
												drug_concept_id = stdConcept,
												drug_exposure_start_datetime = "",
												drug_type_concept_id = "32426",#NLP Derivated
												route_concept_id = stdRoute,
												drug_source_concept_id = ""
												)
							listOfValues.append(elem)
							counter += 1
				idx +=1


		Harmonizer._writeInFile(listOfValues)

	def _harmonizedConcepts(usagiOutput):
		"""
		This method reads the output file from Usagi containing validated concept mappings, and
		creates a dict with the validated concept mappings.
		:param usagiOutput: CSV file with concept mappings that were validated and exported from Usagi
		:return stdConcepts: Dict of validated mappings with the annotated concept as key, and the standard definition as value
		"""
		stdConcepts = {}
		file = open(usagiOutput, 'r') 
		count = 0
		for line in file.readlines():
			if count == 0: #ignore first line
				count += 1
				continue
			data = line.split(",")
			stdConcepts[data[1]] = data[5]
		return stdConcepts

	def _writeInFile(listOfValues):
		"""

		:param
		:return:
		"""
		out = open("../results/DRUG_EXPOSURE.csv", "w", encoding='utf8')
		fileHeaders = ""
		for x in DrugExposure.columns:
			fileHeaders += "{}\t".format(x)
		fileHeaders = fileHeaders[:-1] + "\n"
		out.write(fileHeaders)
		for elem in listOfValues:
			out.write(elem.getRow() + "\n")
		out.close()