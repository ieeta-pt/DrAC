import argparse
import sys
import configparser
from DatasetReader import DatasetReader

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
	if (args.vocabulary and args.annotate) or \
		(not args.vocabulary and not args.annotate):
		return False
	if args.annotate:
		if "dataset" not in settings:
			return False
		if "directory" not in settings["dataset"] or "name" not in settings["dataset"]:
			return False
	return True

def vocabularyCreationMode(settings):
	print("Vocabulary creation mode!")

def annotationMode(settings):
	print("Annotation mode!")
	clinicalNotes = DatasetReader().readClinicalNotes(settings["dataset"]["directory"],settings["dataset"]["name"])

def main():
	args = help()
	settings = readSettings(args.settings)
	if validateSettings(settings, args):
		if args.vocabulary:
			vocabularyCreationMode(settings)

		if args.annotate:
			annotationMode(settings)
	else:
		print("The settings are not defined correctly. Please confirm all the necessary parameters in the documentation!")
		help(show=True)
		exit()

if __name__ == '__main__':
	main()