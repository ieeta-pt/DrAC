import collections

class Evaluator():
	def evaluateNeji(clinicalNotes, nejiAnnotations, showDetail=False):
		"""
		This method evaluates the performance of the Neji annotator in the detection of drugs.
		This evaluation only considers if the drug was detected considering the initial span.
		Strength was not evaluated in this method.
		:param clinicalNotes: Dict of clinical notes with the following structure
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
		:param nejiAnnotations: Dict with the Neji annotations, key is the dataset (train or test), value is another dict containing the
		files name as key and a list of annotations. The annotations have the following structure: date|UMLS:C2740799:T129:DrugsBank|10
			{
				"train":{
					"file name"":["annotation"]
				}
				"test":{...}
			}
		:param showDetail: Boolean that when set to True, the system shows all the false positive and false negative annotations
		"""
		for dataset in clinicalNotes:
			if dataset not in nejiAnnotations:
				print ("Dataset " + dataset + " not annotated yet!")
				continue
			print("Dataset: " + dataset)
			metrics = {}
			for fileName in clinicalNotes[dataset]:
				if fileName not in nejiAnnotations[dataset]:
					print ("Note " + fileName + " not annotated! Maybe a decoding error occurred during the annotation procedure!")
					continue
				annGSList = []
				if "annotation" not in clinicalNotes[dataset][fileName]:
					if showDetail:
						print("File " + fileName + " not available in the gold standard!")
				else:
					for annID in clinicalNotes[dataset][fileName]["annotation"]:
						ann = clinicalNotes[dataset][fileName]["annotation"][annID]
						annGSList.append((ann[0], str(ann[2][0])))
					annList = []
					for ann in nejiAnnotations[dataset][fileName]:
						annList.append((ann[0],ann[2]))
					annList = list(set(annList))
					metrics[fileName] = Evaluator._calculateIndividualMetrics(annGSList, annList)
			Evaluator._calculateGlobalMetrics(metrics, showDetail)

	def _calculateIndividualMetrics(annGS, ann):
		"""
		Private method to calculate metrics individually (Precision, Recall, F1-Score) and 
		to provide metrics for the global calculation (True positives, False positives, False negatives)
		:param annGS: List of tuples with the concepts and the inital span for each Drug annotation in the gold standard
		:param ann: List of tuples with the concepts and the inital span for each annotated Drug
		:return: Dict with individual and global metrics
			{
				"individual":(Precision, Recall, F1-Score)
				"global":(True positives, False positives, False negatives)
				"false_negatives": False Negatives
				"false_positives": False Positives
			}
		"""
		falseNegatives = []
		falsePositives = []
		tp = 0

		for concept, span in annGS:
			if len([annConcept for annConcept, annSpan in ann if span == annSpan]) > 0:
				tp += 1
			else:
				falseNegatives.append(concept.lower())

		for concept, span in ann:
			if len([annConcept for annConcept, annSpan in annGS if span == annSpan]) == 0:
				falsePositives.append(concept.lower())

		fn = len(annGS) - tp
		fp = len(ann) - tp
		try:
			precision = tp/(tp+fp)
			recall = tp/(tp+fn)
			f1Score = 2*((precision*recall)/(precision+recall))
		except:
			precision = 0
			recall = 0
			f1Score = 0
		return {
				"individual":(precision, recall, f1Score),
				"global":(tp, fp, fn),
				"false_negatives":falseNegatives,
				"false_positives":falsePositives
			}

	def _calculateGlobalMetrics(metrics, showDetail):
		"""
		Private method to calculate global metrics (Precision, Recall, F1-Score) and
		show the best and worst clinical note annotation (F1-score)
		:param metrics: Dict with individual and global metrics
			{
				"file name":{
					"individual":(Precision, Recall, F1-Score)
					"global":(True positives, False positives, False negatives)
					"false_negatives": False Negatives
					"false_positives": False Positives
				}
			}
		:param showDetail: Boolean that when set to True, the system shows all the false positive and false negative annotations
		"""
		tp = 0
		fp = 0
		fn = 0
		best = (None, 0)
		worst = (None, 1)
		falseNegatives = []
		falsePositives = []
		for file in metrics:
			tp += metrics[file]["global"][0]
			fp += metrics[file]["global"][1]
			fn += metrics[file]["global"][2]
			if metrics[file]["individual"][2] > best[1]:
				best = (file, metrics[file]["individual"][2], metrics[file]["individual"][0], metrics[file]["individual"][1])
			if metrics[file]["individual"][2] < worst[1]:
				worst = (file, metrics[file]["individual"][2], metrics[file]["individual"][0], metrics[file]["individual"][1])
			falseNegatives.extend(metrics[file]["false_negatives"])
			falsePositives.extend(metrics[file]["false_positives"])
		precision = tp/(tp+fp)
		recall = tp/(tp+fn)
		f1Score = 2*((precision*recall)/(precision+recall))
		print("{:20}\t{:20}\t{:20}".format("Precision", "Recall", "F1-Score"))
		print("{:<20}\t{:<20}\t{:<20}".format(precision, recall, f1Score))
		print("\nThe best annotated note was: {}, with the following scores:".format(best[0]))
		print("{:20}\t{:20}\t{:20}".format("Precision", "Recall", "F1-Score"))
		print("{:<20}\t{:<20}\t{:<20}".format(best[2], best[3], best[1]))
		print("\nThe worst annotated note was: {}, with the following scores:".format(worst[0]))
		print("{:20}\t{:20}\t{:20}".format("Precision", "Recall", "F1-Score"))
		print("{:<20}\t{:<20}\t{:<20}".format(worst[2], worst[3], worst[1]))
		if showDetail:
			print("False Negatives")
			print(collections.Counter(falseNegatives))
			print("False Positives")
			print(collections.Counter(falsePositives))
		#if False: #Just to test the impact of the False Negatives in Neji
		#	for concept in set(falseNegatives):
				#UMLS:C0000120:T121:AOD	
		#		print("AdHoc:UNK:UNK:AdHoc\t{}".format(concept))
	
	def evaluateAnnotations(clinicalNotes, annotations, showDetail=False):
		"""
		This method evaluates the final result of the NLP process.
		This evaluation considers the drugs with routes associated, since one pre-requisite of this methodology was to detect
		drugs and routes, mainly due to the OMOP CDM structure having mandatory fields.
		Therefore, this evaluation will compare the detected route and the concept initial span
		This evaluation only considers if the drug was detected considering the initial span.
		Strength and dosage were not evaluated in this method (for now).
		:param clinicalNotes: Dict of clinical notes with the following structure
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
		:param annotation: Dict with the drug and strength/dosage/route (list) present in each file, by dataset.
			{
				"train":{
					"file name"":{
						("concept",annSpan):[strength, dosage, route]
					}
				}
				"test":{...}
			}
		:param showDetail: Boolean that when set to True, the system shows all the false positive and false negative annotations
		"""
		for dataset in clinicalNotes:
			if dataset not in annotations:
				print ("Dataset " + dataset + " not annotated yet!")
				continue
			print("Dataset: " + dataset)
			metrics = {}
			for fileName in clinicalNotes[dataset]:
				if fileName not in annotations[dataset]:
					print ("Note " + fileName + " not annotated! Maybe a decoding error during the annotation procedure!")
					continue
				annGSList = []#(drug, span, route)

				if "relation" not in clinicalNotes[dataset][fileName]:
					if showDetail:
						print("File " + fileName + " not available in the gold standard!")
				else:
					for relID in clinicalNotes[dataset][fileName]["relation"]:
						annID = clinicalNotes[dataset][fileName]["relation"][relID][0]
						rel = clinicalNotes[dataset][fileName]["relation"][relID][1]
						if rel[1].lower() == "route": #Considering only the routes
							ann = clinicalNotes[dataset][fileName]["annotation"][annID]
							route = rel[0]
							annGSList.append((ann[0], str(ann[2][0]), route))
					annList = []#(drug, span, route)
					for ann, annSpan in annotations[dataset][fileName]:
						if ann is None: #the none entries are ignored when the matrix is built, but i need to find the problem
							continue
						rel = annotations[dataset][fileName][(ann, annSpan)][2]
						annList.append((ann, annSpan, rel))
					#print(annGSList)
					#print(annList)
					#print("---")
					metrics[fileName] = Evaluator._calculateIndividualMetricsRel(annGSList, annList, fileName)
			Evaluator._calculateGlobalMetrics(metrics, showDetail)

	def _calculateIndividualMetricsRel(annGS, ann, doc):
		"""
		Private method to calculate metrics individually (Precision, Recall, F1-Score) and 
		to provide metrics for global calculation (True positives, False positives, False negatives)
		considering the relations between routes and drugs
		:param annGS: List of tuples with the concepts and routes for each Drug annotation in the gold standard
		:param ann: List of tuples with the concepts and routes for each Drug annotated
		:return: Dict with individual and global metrics
			{
				"individual":(Precision, Recall, F1-Score)
				"global":(True positives, False positives, False negatives)
				"false_negatives": False Negatives
				"false_positives": False Positives
			}
		"""
		falseNegatives = []
		falsePositives = []
		tp = 0

		for drug, span, route in annGS:
			if len([annConcept for annConcept, annSpan, annRoute in ann if span == annSpan and annRoute.lower() == route.lower()]) > 0:
				tp += 1
			else:
				falseNegatives.append((drug.lower(), route.lower()))

		for annConcept, annSpan, annRoute in ann:
			if len([drug for drug, span, route in annGS if span == annSpan and annRoute.lower() == route.lower()]) == 0:
				falsePositives.append((annConcept.lower(), annRoute.lower()))

		fn = len(annGS) - tp
		fp = len(ann) - tp
		try:
			precision = tp/(tp+fp)
			recall = tp/(tp+fn)
			f1Score = 2*((precision*recall)/(precision+recall))

			if precision > 1 or recall > 1:
				print("The document {} contains annotation issues in the gold standard".format(doc))
				precision = 0
				recall = 0
				f1Score = 0
		except: #This will only affect the individual metrics, in which it will be difficult to find the worst clinical note
			precision = 0
			recall = 0
			f1Score = 0
		return {
				"individual":(precision, recall, f1Score),
				"global":(tp, fp, fn),
				"false_negatives":falseNegatives,
				"false_positives":falsePositives
			}