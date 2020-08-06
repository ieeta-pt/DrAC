from Tables.DrugExposure import DrugExposure
from Tables.Note import Note
from Tables.NoteNLP import NoteNLP

class Harmonizer():
	def harmonize(matrix, usagiOutput, clinicalNotes):
		"""
		This method is used in the system's Migration mode and 1) harmonizes the concepts in the matrix to their standard definition,
		2) migrates harmonized data into the OMOP CDM schema
		The mappings used for the harmonization procedure must be previously validated in the Usagi tool, before being used in this method.
		:param matrix: matrix with extracted information from the annotation component
		:param usagiOuput: CSV file with concept mappings that were validated and exported from Usagi
		:param clinicalNotes: Dict of clinical notes with the following structure (but only the "cn" from each file will be used)
		:return values: the tables to be migrated into the OMOP CDM data schema
			{
				"train":{
					"file name"":{
						"cn": "clinical note",
						"annotation":{
							"id":("concept","type",[(span,span), ...])
						},
						"relation":{
							"id": (annId1, ("concept","type",[(span,span), ...]))
						}
					}
				}
				"test":{...}
			}
		"""
		headers = matrix[0]
		stdConcepts = Harmonizer._harmonizedConcepts(usagiOutput) #dict
		data = matrix[1:]
		values = {}
		counter = 0
		noteCounter = 0
		values["drug_exposure"] = []
		values["note"] = []
		values["note_nlp"] = []
		for rawD in data:#x is a list (raw in the matrix)
			pid = rawD[0]
			idx = 0
			text = clinicalNotes["train"][pid]["cn"].replace("\n", "\\n")
			note = Note(note_id = noteCounter,
						person_id = pid,
						note_text = text,
						note_datetime = "",
						encoding_concept_id = "32678",
						language_concept_id = "42065925",
						note_type_concept_id = "44814645", #NOTE code
						note_class_concept_id = "")
			values["note"].append(note)

			for cell in rawD:
				if idx > 0: #ignore first
					if len(cell) == 0:
						pass
					else:
						concept = headers[idx]
						data = cell.split("|")
						quantity = data[1].lower()
						route = data[2].lower()
						if concept not in stdConcepts or route not in stdConcepts:
							pass
						else:
							stdConcept, stdClass = stdConcepts[concept]
							stdRoute, stdRouteClass = stdConcepts[route]
							elem = DrugExposure(drug_exposure_id = counter,
												person_id = pid,
												drug_concept_id = stdConcept,
												drug_exposure_start_datetime = "",
												drug_type_concept_id = "32426",#NLP Derivated
												route_concept_id = stdRoute,
												drug_source_concept_id = stdClass,
												quantity = quantity,
												drug_source_value = concept,
												route_source_value = route)
							values["drug_exposure"].append(elem)
							elemNLP = NoteNLP(	note_nlp_id = counter,
												note_id = noteCounter,
												nlp_date = "",
												section_concept_id = "44814645", #NOTE code
												lexical_variant = concept,
												note_nlp_concept_id = stdClass,
												note_nlp_source_concept_id = stdConcept)
							values["note_nlp"].append(elemNLP)
							counter += 1
				idx +=1
			noteCounter += 1
		return values

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
			stdConcepts[data[1]] = (data[5],data[13])
		return stdConcepts

