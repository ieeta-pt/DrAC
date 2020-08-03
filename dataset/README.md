# Datasets

## Public datasets
This system was validated using two public datasets:
- 2018 n2c2 Track on ADE and Medication Extraction Challenge: Contains clinical notes and annotation files with the identification of medications and their respective dosage, strength, route of administration, duration and reason, as well as adverse drug events (ADE).
	- train/ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; _Contains discharge summaries (.txt) and annotation files (.ann)_ 
	- test/ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_Contains discharge summaries (.txt) and annotation files (.ann)_
	- test_data_Task2/ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_NOT USED_ 
	- test_data_Tasks1&3/ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_NOT USED_ 	
	
- 2009 i2b2 Track on Medication Extraction: Contains discharge summaries and annotation files with the identification of medications and their respective dosage, route of administration, frequency and duration.
	- train.test.released.8.17.09/ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_Contains discharge summary files_
	- converted.noduplicates.sorted/ &nbsp; _Contains annotation files_

These datasets are public but have controlled access. To use them, please request their access at:
https://portal.dbmi.hms.harvard.edu/projects/n2c2-nlp/


## Example dataset
To test the pipeline using dummy discharge summaries, three discharge summary samples are provided in `Examples/`.

## Initial steps

Before running the system, it is necessary to:

- Add the datasets in this directory

&nbsp;&nbsp;&nbsp;**OR**

- Configure the new dataset directory in the Settings.ini file.

