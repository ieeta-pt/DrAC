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

After creating the vocabularies, it is necessary to filter the UMLS_AOD_AOD.tsv vocabulary to have only the chemical concepts. This can be done using the following command (in Linux systems):
```sh
cat UMLS_AOD_AOD.tsv | grep -E "T116|T195|T123|T122|T103|T120|T104|T200|T196|T126|T131|T125|T129|T130|T197|T114|T109|T121|T192|T127" > UMLS_AOD_AOD_filtered.tsv
```

T's map all semantic types belonging to the Chemicals & Drugs semantic group in UMLS


These files must be added here in this directory to run the system or configured the new location in the Settings.ini file. To access these files, please request their access at https://www.nlm.nih.gov/research/umls/index.html
