# Vocabularies

The vocabulary used in the system was created based on the concepts available in the UMLS, which are the following files:
- MRCONSO.RRF for extracting the concepts
- MRSTY.RRF for extracting the semantic in the concepts

The system will execute and create the vocabulary files to add in the Neji system. However, in order to optimize this creation, it is necessary to filter the UMLS vocabulary. The filter can be done using the following command (in Linux systems):
```sh
cat MRCONSO.RRF | grep "RXNORM" > RXNORM.csv
cat MRCONSO.RRF | grep "DRUGBANK" > DRUGBANK.csv
cat MRCONSO.RRF | grep "|AOD|" > AOD.csv
```

These files must be added here in this directory to run the system or configured the new location in the Settings.ini file. To access these files, please request their access at https://www.nlm.nih.gov/research/umls/index.html

