import argparse
import sys
import configparser
from DatasetReader import DatasetReader
from Annotator import Annotator
from Relation import Relation
from Writer import Writer
from Vocabulary import Vocabulary
from Evaluator import Evaluator

def help(show=False):
	parser = argparse.ArgumentParser(description="")
	configs = parser.add_argument_group('System settings', 'The system parameters to run the system in the different modes')
	configs.add_argument('-s', '--settings', dest='settings', \
						type=str, default="../settings.ini", \
						help='The system settings file (default: ../settings.ini)')	

	executionMode = parser.add_argument_group('Execution Mode', 'Choose what is the execution mode!')
	executionMode.add_argument('-v', '--vocabulary', default=False, action='store_true', \
							help='In this mode, the system will create the vocabularies to use in Neju (default: False)')
	executionMode.add_argument('-a', '--annotate', default=False, action='store_true', \
							help='In this mode, the system will annotate the dataset (default: False)')
	executionMode.add_argument('-e', '--evaluate', default=False, action='store_true', \
							help='In this mode, the system will read the annotations and evaluate the dataset without converting it to \
							the matrix (default: False)')

	complementaryMode = parser.add_argument_group('Complementary functions', 'Choose the complementary functions for the execution modes!')
	complementaryMode.add_argument('-r', '--read-ann', default=False, action='store_true', \
							help='This flag is complementary to the --annotate or --evaluate execution mode. With this flag activated, the system \
							will used the neji annotations stored previously (default: False)')
	if show:
		parser.print_help()
	return parser.parse_args()

def readSettings(settingsFile):
	configuration = configparser.ConfigParser()
	configuration.read(settingsFile)
	if not configuration:
		raise Exception("The settings file was not found!")
	return configuration._sections

def validateSettings(settings, args):
	#Ensure the selection of one execution mode, otherwise do not work
	if (args.vocabulary and args.annotate and args.evaluate) or \
		(not args.vocabulary and not args.annotate and not args.evaluate):
		return False

	if args.vocabulary:
		if "vocabularies" not in settings:
			return False
		if 	"umls_rxnorm" not in settings["vocabularies"] or \
			"umls_drugsbank" not in settings["vocabularies"] or \
			"umls_aod" not in settings["vocabularies"] or \
			"tuis" not in settings["vocabularies"] or \
			"output" not in settings["vocabularies"]:
			return False

	if args.annotate or args.evaluate:
		if "dataset" not in settings:
			return False
		if "directory" not in settings["dataset"] or "name" not in settings["dataset"]:
			return False
	return True

def vocabularyCreationMode(settings):
	print("Vocabulary creation mode!")
	vocabularies = Vocabulary.create(settings["vocabularies"])
	Writer.writeVocabularies(vocabularies, settings["vocabularies"]["output"])
	print("Done!")

def annotationMode(settings, read):
	print("Annotation mode!")
	clinicalNotes = DatasetReader.readClinicalNotes(settings["dataset"]["directory"], settings["dataset"]["name"])
	if read:
		nejiAnnotations = Annotator.readNejiAnnotations(settings["dataset"]["neji_annotations"])
	else:
		nejiAnnotations = Annotator.annotate(clinicalNotes)
		Writer.writeAnnotations(nejiAnnotations, settings["dataset"]["neji_annotations"])

	annotations = Relation.inferRelations(nejiAnnotations)
	Writer.writeMatrix(annotations)
	print("Done!")

def evaluationMode(settings, read):
	print("Evaluation mode!")
	clinicalNotes = DatasetReader.readClinicalNotes(settings["dataset"]["directory"], settings["dataset"]["name"])
	if read:
		nejiAnnotations = Annotator.readNejiAnnotations(settings["dataset"]["neji_annotations"])
	else:
		nejiAnnotations = Annotator.annotate(clinicalNotes)
	Evaluator.evaluateNeji(clinicalNotes, nejiAnnotations)
	print("Done!")

def main():
	args = help()
	settings = readSettings(args.settings)
	if validateSettings(settings, args):
		if args.vocabulary:
			vocabularyCreationMode(settings)

		if args.annotate:
			annotationMode(settings, args.read_ann)

		if args.evaluate:
			evaluationMode(settings, args.read_ann)
	else:
		print("The settings are not defined correctly. Please confirm all the necessary parameters in the documentation!")
		help(show=True)
		exit()

if __name__ == '__main__':
	main()