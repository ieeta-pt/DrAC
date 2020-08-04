# Vocabularies

The vocabulary used in the system was created based on the concepts available in the UMLS, using the following files:

- MRCONSO.RRF for extracting the concepts
- MRSTY.RRF for extracting the UMLS semantic type associated with each concept

To obtain access to the `MRCONSO.RRF` and `MRSTY.RRF` resource files, please request your access [here](https://www.nlm.nih.gov/research/umls/index.html).

## Creating Neji dictionaries

To create the vocabulary files to be added in the Neji annotating system, it is necessary to execute two steps:
- Extract domain specific dictionary files from the UMLS
- Filter and format the dictionary files according to the format required by the Neji annotating system

### Create domain specific dictionaries
To create the necessary vocabulary files from the UMLS, the following command is used (in Linux systems):
```sh
cat MRCONSO.RRF | grep "RXNORM" > RXNORM.csv
cat MRCONSO.RRF | grep "DRUGBANK" > DRUGBANK.csv
cat MRCONSO.RRF | grep "|AOD|" > AOD.csv
```

Despite the specificity of RxNorm and DrugBank dictionaries, the AOD dictionary covers a broader spectrum of concepts. To filter the `UMLS_AOD_AOD.tsv` vocabulary file so that it only contains UMLS concepts belonging to the "Chemicals & Drugs" semantic group, the following command must be run (in Linux systems), where all `Txxx` codes correspond to semantic types within the "Chemicals & Drugs" semantic group:
```sh
cat UMLS_AOD_AOD.tsv | grep -E "T116|T195|T123|T122|T103|T120|T104|T200|T196|T126|T131|T125|T129|T130|T197|T114|T109|T121|T192|T127" > UMLS_AOD_AOD_filtered.tsv
```

### Filter and format dictionaries for Neji

After creating the three dictionary files, simply run the following command to create the Neji compliant dictionary files.

  $ python main.py -v
  
