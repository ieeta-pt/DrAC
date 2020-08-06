import json
import requests
import glob
import codecs
import re
from Utils import Utils
from Vocabulary import Vocabulary

#Flags to simplify the organization of theinformation in the list
STRENGTH = 0
DOSAGE = 1
ROUTE = 2
#QUANTITY = 3
SPAN = 3


# Group of variables adapted from MedXN to use in regexes
DOSAGE_FORM   = "tablet|tab|capsule|caplet|cap|pill|lozenge|packet|patch|puff|squirt|gel|softgel"
EXTENDED_DF   = "extended release enteric coated capsule|12 hour extended release capsule|24 hour extended release capsule|extended release enteric coated tablet|12 hour extended release tablet|24 hour extended release tablet|16 hour transdermal patch|24 hour transdermal patch|72 hour transdermal patch|mucous membrane topical solution|sustained release buccal tablet|soap topical bar|enteric coated capsule|extended release capsule|augmented topical cream|orderable drug form|augmented topical gel|gas for inhalation|metered dose inhaler|dry powder inhaler|solution for injection|suspension for injection|augmented topical lotion|augmented topical ointment|biweekly transdermal patch|weekly transdermal patch|medicated bar soap|medicated liquid soap|ophthalmic irrigation solution|extended release suspension|enteric coated tablet|extended release tablet|toothpaste dental toothpaste|prefilled applicator|chewable bar|topical cake|oral capsule|liquid cleanser|ear cream|eye cream|nasal cream|ophthalmic cream|oral cream|otic cream|rectal cream|topical cream|vaginal cream|buccal film|cutaneous foam|oral foam|rectal foam|topical foam|vaginal foam|inhalation gas|eye gel|nasal gel|ophthalmic gel|oral gel|rectal gel|topical gel|urethral gel|vaginal gel|chewing gum|drug implant|nasal inhalant|nasal inhaler|nasal jelly|ophthalmic jelly|oral jelly|rectal jelly|vaginal jelly|cleanser liquid|topical lotion|topical oil|ear ointment|eye ointment|nasal ointment|ophthalmic ointment|oral ointment|otic ointment|rectal ointment|topical ointment|vaginal ointment|medicated pad|oral paste|transdermal patch|drug pellet|cutaneous powder|inhalant powder|inhalation powder|oral powder|rectal powder|topical powder|vaginal powder|vaginal ring|mouthwash rinse|oral rinse|medicated shampoo|bar soap|ophthalmic sol|cutaneous solution|inhalant solution|inhalation solution|injectable solution|intramuscular solution|intraperitoneal solution|intravenous solution|irrigation solution|nasal solution|ophthalmic solution|oral solution|otic solution|rectal solution|topical solution|mucosal spray|nasal spray|oral spray|powder spray|rectal spray|topical spray|vaginal spray|oral strip|rectal suppositories|vaginal suppositories|rectal suppository|urethral suppository|vaginal suppository|injectable suspension|intramuscular suspension|intrathecal suspension|intravenous suspension|nasal suspension|ophthalmic suspension|oral suspension|otic suspension|rectal suspension|prefilled syringe|buccal tablet|chewable tablet|disintegrating tablet|gastro-resistant tablet|oral tablet|sublingual tablet|vaginal tablet|enteric-coated tablet|medicated tape|oral troche|bar|beads|cake|caplet|caps|capsule|cement|cream|crystal|disk|douche|elixir|enema|flake|foam|gargle|gas|gel|granule|inhalant|jelly|liquid|lotion|lozenge|mouthwash|mouthwash/rinse|oil|ointment|pack|paste|patch|pellet|powder|pudding|salve|solid|solution|spray|suppositories|suppository|suspension|syrup|tablet|toothpaste|troche|unguent|wafer"
ALL_FORM      = EXTENDED_DF + "|" + DOSAGE_FORM + "|" + "tab|pill|packet|puff|squirt|softgel|nebulizer|neb|supplementation|supplement|aerosol|emulsion|implant|injection|shampoo|soap|cream|elixir|enema|gel|inhalant|liquid|lotion|ointment|powder|solution|spray|suppository|syrup|gttae|gtts"
DURATION_UNIT = "hours|hour|hrs|days|day|weeks|week|months|month|mons|mon|years|year|yrs|yr"
STR_NUM       = "half|one|two|three|four|five|six|seven|eight|nine|ten|twelve"
MEAL          = "breakfast|lunch|dinner|supper|meals|meal"
DAYTIME       = "am|pm|a\\.m\\.|p\\.m\\.|morning|afternoon|noon|evening|night|daytime|nighttime|bedtime|h\\.s\\.|hs"
DAYS          = "monday|mon|tuesday|tues|wednesday|wed|thursday|thurs|friday|fri|saturday|sat|sunday|sun|day|mondays|tuesdays|wednesdays|thursdays|fridays|saturdays|sundays"
TIME_UNIT     = "hour|hr|h|minute|min|hours|hrs|minutes|mins"
DAY_UNIT      = "day|d|week|wk|month|mon|days|weeks|wks|months|mons"
PER_UNIT      = "(?:(?:a|one|per)(?:\\s+|-)(?:day|week|wk|month|mon))|nightly|daily|weekly|monthly"
ASNEED        = "as necessary|as needed|as-needed|as directed|as-directed|prn|p\\.r\\.n\\."
NUMBER        = "(?:half|one three|one fourth|one|two|three|four|five|six|seven|eight|nine|ten|\\d/\\d|\\d\\.\\d|\\d+)(?:(?: |-)?(?:-|to)(?: |-)?(?:half|one three|one fourth|one|two|three|four|five|six|seven|eight|nine|ten|\\d/\\d|\\d\\.\\d|\\d+))?"
DECIMAL_NUM   = "(?:\\d+,)?\\d+(?:\\.\\d+)?(?:(?: |-)?(?:-|to)(?: |-)?(?:\\d+,)?\\d+(?:\\.\\d+)?)?"
FREQ_LATIN    = "tid|bd|bid|bis|qd|qhs|qad|qam|qpm|qds|qh|qid|qqh|od|t\\.i\\.d\\.|b\\.d\\.|b\\.i\\.d.|q\\.d\\.|q\\.h\\.s\\.|q\\.a\\.d\\.|q\\.a\\.m\\.|q\\.p\\.m\\.|q\\.d\\.s\\.|q\\.h\\.|q\\.i\\.d\\.|q\\.q\\.h\\.|o\\.d\\."
ROUTE_REG     = "subcutaneously|sq|intervenous|intervenously|injected|transdermal|gastric|duodental|skin|pv|topical|topically|vaginally|po|p\\.o\\.|mouth|oral|orally|rectally|anally|pr|p\\.r\\.|ou|o\\.u\\.|iv|nostril|intramuscular"
STRENGTH_UNIT = "mg/dl|mg/ml|g/l|milligrams|milligram|mg|grams|gram|g|micrograms|microgram|mcg|meq|iu|cc|units|unit|tablespoons|tablespoon|teaspoons|teaspoon"
		
class Annotator():
	def annotate(clinicalNotes):
		"""
		This method annotates the clinical notes in the dataset using Neji with the vocabularies created.
		:param clinicalNotes: Dict of clinical notes with the following structure
			{
				"train":{
					"file name"":{
						"cn": "clinical note",
						"annotation":{
							"id":("concept",[(span,span), ...])
						},
						"relation":{
							"id": (annId1, ("concept","type",[(span,span), ...]))
						}
					}
				}
				"test":{...}
			}
		:return: Dict with the Neji annotations, key is the dataset (train or test), value is another dict containing the
		files name as key and a list of annotations. The annotations have the following structure: date|UMLS:C2740799:T129:DrugsBank|10
			{
				"train":{
					"file name"":["annotation"]
				}
				"test":{...}
			}
		"""
		url = "https://bioinformatics.ua.pt/nejiws/annotate/Drugs/annotate"
		headers = {'Content-Type': 'application/json; charset=UTF-8'}
		annotations = {}
		annotations["train"] = {}
		for fileName in clinicalNotes["train"]:
			print(fileName)
			try:
				text = clinicalNotes["train"][fileName]["cn"]
				payload = json.dumps({"text": "%s" % text.lower()}, ensure_ascii=True).encode('utf-8')
				response = requests.request("POST", url, data=payload, headers=headers)
				results = json.loads(response.text)
				results = results['entities']
				annotations["train"][fileName] = []
				for ann in results:
					ann = tuple(ann.split("|"))
					annotations["train"][fileName].append(ann)
			except Exception as e:
				print(e)
		return annotations

	def readNejiAnnotations(location):
		"""
		This method reads previous Neji annotations that have been stored.
		The file content has the following structure:
			file name|concept|neji code|inital span
		Example:
			100035|date|UMLS:C2740799:T129:DrugsBank|10
		:param location: Directory with the annotation files to be read
		:return: Dict with the neji annotations, key is the dataset (train or test), value is another dict containing the
		files name as key and a list of annotations. The annotations have the following structure: date|UMLS:C2740799:T129:DrugsBank|10
			{
				"train":{
					"file name"":["annotation"]
				}
				"test":{...}
			}
		"""
		nejiAnnFiles = sorted(glob.glob('{}*nejiann.tsv'.format(location)))
		ann = {}
		for file in nejiAnnFiles:
			dataset = file.split("/")[-1].split("_")[0]
			ann[dataset] = {}
			with codecs.open(file, 'r', encoding='utf8') as fp:
				annotations = fp.read().strip().split("\n")
				for annotation in annotations:
					#file name|concept|neji code|inital span
					data = annotation.split("|")
					fileName = data[0]
					nejiann = tuple(data[1:])
					if fileName not in ann[dataset]:
						ann[dataset][fileName] = []
					ann[dataset][fileName].append(nejiann)
		return ann

	def postProcessing(clinicalNotes, nejiAnnotations, vocabularies):
		"""
		:param clinicalNotes: Dict of clinical notes with the following structure (but only the "cn" from each file will be used)
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
		:param nejiAnnotations: Dict with the annotations, key is the dataset (train or test), value is another dict containing the
		files name as key and a list of annotations. The annotations have the following structure: date|UMLS:C2740799:T129:DrugsBank|10
			{
				"train":{
					"file name"":["annotation"]
				}
				"test":{...}
			}
		:param vocabularies: Vocabularies to be used in the post processing
		:return: Dict with the drug and strength/dosage/route/span (list) present in each file, by dataset.
			{
				"train":{
					"file name"":{
						("concept", annSpan):[strength, dosage, route]
					}
				}
				"test":{...}
			}
		"""
		voc = Vocabulary.readPostProcessingVoc(vocabularies)
		annotations = {}
		for dataset in nejiAnnotations:
			annotations[dataset] = {}
			for file in nejiAnnotations[dataset]:
				annotations[dataset][file] = {}
				clinicalNote = clinicalNotes[dataset][file]["cn"]
				annotation = sorted(nejiAnnotations[dataset][file], key=lambda x: int(x[2]))
				annotation = Utils.cleanConceptBegin(annotation)
				disambiguatedAnn = Utils.disambiguate(annotation)
				filteredAnn = Annotator._filter(disambiguatedAnn, Utils.getVocListWithoutGroup(voc["all"]))#voc["black-list"]))
				if len(filteredAnn) > 0:
					sentences = Utils.getSentencesByAnnotation(clinicalNote, filteredAnn)

					readSpans = []
					for (annConcept, annCode, annSpan) in filteredAnn:
						results = [None, None, None, None]
						if annSpan in readSpans:
							continue
						readSpans.append(annSpan)
						
						if int(annSpan) not in sentences:
							continue 

						results[ROUTE] = Annotator._annotateRoute(sentences[int(annSpan)], voc["route-complex"], voc["route"])

						if results[ROUTE] != None:
							filterAnn = [(concept, code, span) for (concept, code, span) in annotation if span == annSpan and concept is not None]
							if len(filterAnn) > 1:
								drug, strength = Utils.mergeAnnsToGetStrength(filterAnn)
								if drug:
									results[STRENGTH] = strength
							else:
								drug = filterAnn[0][0]

							sentence = ' '.join(sentences[int(annSpan)])
							if results[STRENGTH] == None:
								results[STRENGTH] = Annotator._annotateStrength(sentence)
							results[DOSAGE] = Annotator._annotateDosage(sentence)

							annotations[dataset][file][(drug, annSpan)] = results

		return annotations
	
	def _filter(annotations, vocList):
		"""
		This method filters the annotations by removing the concepts in the vocabularies present in vocList
		:param annotations: These are the disambiguated annotations following the same format (see postProcessing method for more details)
		:param vocList: List of vocabularies with the concepts to remove
		:return: The annotations filtered using the same format as the input
		"""
		results = []
		for ann in annotations:
			if ann[0] not in vocList:
				results.append(ann)
		return results

	def _annotateRoute(sentence, complexVoc, voc):
		"""
		This method annotates the drug route in the sentence where the concept was found.
		:param sentence: The list of 15 or less words that are after the concept
		:param complexVoc: The vocabulary of routes with more than one word, list of tuples (concept, type)
		:param voc: The vocabulary to use in a list of tuples (concept, type)
		:return: Tuple with Route or None and route span counter
		"""
		route = []
		for entry, group in complexVoc:
			search = " {} ".format(entry.lower())
			if search in " ".join(sentence):
				return entry

		for entry, group in voc:
			search = entry.lower()
			if search in sentence:
				if "other" in group:
					group = "zzzz" #To be the last option in the list
				route.append((entry, group))
		if len(route) > 1:
			route = sorted(route, key=lambda e: (e[1], -len(e[0])))
			return route[0][0]
		if len(route) == 1:
			return route[0][0]
		return None

	def _annotateStrength(sentence):
		"""
		This method uses Regexes to detect the presence of strength information in the input sentence
		:param sentence: sentence to search for strength information
		:return: string with detected strength information if such content exists, returns None otherwise
		"""
		strengthList = [
			re.compile(r"\b(%s/)?(%s)(\s+|-)?(%s)\b"        %(DECIMAL_NUM, DECIMAL_NUM, STRENGTH_UNIT), re.IGNORECASE),
			re.compile(r"\b\d+\s?(-|to)\s?\d+(\s|-)?(%s)\b" %STRENGTH_UNIT, re.IGNORECASE),
			re.compile(r"\b(%s)\s+(to\s+(%s)\s+)?(%s)\b"    %(STR_NUM, STR_NUM, STRENGTH_UNIT), re.IGNORECASE)
		]
		for regex in strengthList:
			x = regex.search(sentence)
			if x:
				return x.group(0)
		return None

	def _annotateDosage(sentence):
		"""
		This method uses Regexes to detect the presence of dosage information in the input sentence
		:param sentence: sentence to search for dosage information
		:return: The dosage of the drug taken by the patient if such content exists, returns None otherwise
		"""
		dosageList = [
			re.compile(r"\b(%s)\s+(at a time|dose of)\b"                        %NUMBER, re.IGNORECASE),
			re.compile(r"\b(%s)\s+(%s)(s|es)?\b"                                %(NUMBER, ALL_FORM), re.IGNORECASE),
			re.compile(r"\b(%s)\s+(%s/)?(%s)(\s|-)?(%s)\s+(%s)(s|es)?\b"        %(NUMBER, DECIMAL_NUM, DECIMAL_NUM, STRENGTH_UNIT, ALL_FORM), re.IGNORECASE),
			re.compile(r"\b(%s)\s+(%s)(\s|-)?(times|time)\s+(%s)\b"             %(NUMBER, NUMBER, PER_UNIT), re.IGNORECASE),
			re.compile(r"\b(%s)\s+(after|before|following|with|w/|at)\s+(%s)\b" %(NUMBER, MEAL), re.IGNORECASE),
			re.compile(r"\b(%s)\s+(in|on|at|during)\s+(the\s+)?(%s)(\W|$)"      %(NUMBER, DAYTIME), re.IGNORECASE),
			re.compile(r"\b(%s)\s+(each|every|on)\s+(%s)\b"                     %(NUMBER, DAYS), re.IGNORECASE),
			re.compile(r"\b(%s)\s+every\s+(%s)\s+(%s|%s)\b"                     %(NUMBER, NUMBER, TIME_UNIT, DAY_UNIT), re.IGNORECASE),
			re.compile(r"\b(%s)\s+(q|q\.) ?(\d ?(to|-) ?)?\d? ?(%s|%s)\b"       %(NUMBER, TIME_UNIT, DAY_UNIT), re.IGNORECASE),
			re.compile(r"\b(%s)\s*(%s)(\W|$)"                                   %(NUMBER, FREQ_LATIN), re.IGNORECASE),
			re.compile(r"\b(%s)\s+(once|twice)(\s|-)(%s)\b"                     %(NUMBER, PER_UNIT), re.IGNORECASE),
			re.compile(r"\b(%s)(\s+|-)(%s)\b"                                   %(NUMBER, PER_UNIT), re.IGNORECASE),
			re.compile(r"\b(%s)\s+(%s)(\W|$)"                                   %(NUMBER, ASNEED), re.IGNORECASE),
			re.compile(r"\b(%s)/(%s)\b"                                         %(NUMBER, DAY_UNIT), re.IGNORECASE),
			re.compile(r"\b(%s)\s+(%s)\b"                                       %(NUMBER, ROUTE_REG), re.IGNORECASE),
			re.compile(r"\b(%s)\s+(%s)\s+(\S+\s+){0,1}(%s)\b"                   %(STRENGTH_UNIT, NUMBER, ROUTE_REG), re.IGNORECASE)
		]
		for regex in dosageList:
			x = regex.search(sentence)
			if x:
				for entry in x.groups():
					if entry is not None:
						if entry.isnumeric():
							return entry
		return None