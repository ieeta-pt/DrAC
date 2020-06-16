# Vocabularies

The vocabulary used in the system was created based on the RXNorm provided by the UMLS, which are the following files:
- MRCONSO.RRF for extracting the concepts
- MRSTY.RRF for extracting the semantic in the concepts

The system will execute and create the vocabulary files to add in the Neji system. However, this creation requires the RXNorm terms from the MRCONSO.RRF file. The filter can be done using the following command (in Linux systems):
```sh
cat MRCONSO.RRF | grep RXNORM > rxnorm.tsv
```

These files must be added here in this directory to run the system or configured the new location in the Settings.ini file. To access these files, please request their access at https://www.nlm.nih.gov/research/umls/index.html