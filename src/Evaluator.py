
class Evaluator():
	def evaluateNeji(clinicalNotes, nejiAnnotations):
		"""
		This method evaluates the Neji performance to detect drugs. 
		This evaluation only considers if the drug was detecting considering the initial span.
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
							"id": (type, annId1, annId2)
						}
					}
				}
				"test":{...}
			}
		:param nejiAnnotations: Dict with the neji annotations, key is the dataset (train or test), value is another dict containing the
		files name as key and a list of annotations. The annotations have the following structure: date|UMLS:C2740799:T129:DrugsBank|10
			{
				"train":{
					"file name"":["annotation"]
				}
				"test":{...}
			}
		"""
		for dataset in clinicalNotes:
			if dataset not in nejiAnnotations:
				print ("Dataset " + dataset + " not annotated yet!")
				continue
			print("Dataset: " + dataset)
			metrics = {}
			for fileName in clinicalNotes[dataset]:
				if fileName not in nejiAnnotations[dataset]:
					print ("Note " + fileName + " not annotated! Maybe an decoding error during the annotation procedure!")
					continue
				annGSInitialSpan = []
				for annID in clinicalNotes[dataset][fileName]["annotation"]:
					ann = clinicalNotes[dataset][fileName]["annotation"][annID]
					annGSInitialSpan.append(str(ann[2][0]))
				annInitialSpan = []
				for ann in nejiAnnotations[dataset][fileName]:
					annInitialSpan.append(ann[2])
				annInitialSpan = list(set(annInitialSpan))
				metrics[fileName] = Evaluator._calculateIndividualMetrics(annGSInitialSpan, annInitialSpan)
			Evaluator._calculateGlobalMetrics(metrics)

	def _calculateIndividualMetrics(annGSInitialSpan, annInitialSpan):
		"""
		Private method to calculate metrics individually (Precision, Recall, F1-Score) and 
		to provide metrics to global calculation (True positives, False positives, False negatives)
		:param annGSInitialSpan: List of values with the inital span from each Drug annotation
		:param annInitialSpan: List of values with the annotated spans 
		:return: Dict with individual and global metrics
			{
				"individual":(Precision, Recall, F1-Score)
				"global":(True positives, False positives, False negatives)
			}
		"""
		tp = 0
		for value in annGSInitialSpan:
			if value in annInitialSpan:
				tp += 1
		fn = len(annGSInitialSpan) - tp
		fp = len(annInitialSpan) - tp
		precision = tp/(tp+fp)
		recall = tp/(tp+fn)
		f1Score = 2*((precision*recall)/(precision+recall))
		return {
				"individual":(precision, recall, f1Score),
				"global":(tp, fp, fn)
			}

	def _calculateGlobalMetrics(metrics):
		"""
		Private method to calculate global metrics (Precision, Recall, F1-Score) and
		show the best and worst clinical note annotation (F1-score)
		:param metrics: Dict with individual and global metrics
			{
				"file name":{
					"individual":(Precision, Recall, F1-Score)
					"global":(True positives, False positives, False negatives)
				}
			}
		"""
		tp = 0
		fp = 0
		fn = 0
		best = (None, 0)
		worst = (None, 1)
		for file in metrics:
			tp += metrics[file]["global"][0]
			fp += metrics[file]["global"][1]
			fn += metrics[file]["global"][2]
			if metrics[file]["individual"][2] > best[1]:
				best = (file, metrics[file]["individual"][2], metrics[file]["individual"][0], metrics[file]["individual"][1])
			if metrics[file]["individual"][2] < worst[1]:
				worst = (file, metrics[file]["individual"][2], metrics[file]["individual"][0], metrics[file]["individual"][1])
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
