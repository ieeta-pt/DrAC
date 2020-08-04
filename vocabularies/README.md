# Vocabularies

The vocabulary used in the system was created based on the concepts available in the UMLS, using the following files:

- MRCONSO.RRF for extracting the concepts
- MRSTY.RRF for extracting the UMLS semantic type associated with each concept

To obtain access to the `MRCONSO.RRF` and `MRSTY.RRF` resource files, please request your access [here](https://www.nlm.nih.gov/research/umls/index.html).

To create the necessary vocabulary files from the UMLS, the following command is used (in Linux systems):
```sh
cat MRCONSO.RRF | grep "RXNORM" > RXNORM.csv
cat MRCONSO.RRF | grep "DRUGBANK" > DRUGBANK.csv
cat MRCONSO.RRF | grep "|AOD|" > AOD_unfiltered.csv
```

Despite the specificity of RxNorm and DrugBank dictionaries, the AOD dictionary covers a broader spectrum of concepts. To filter the `AOD_unfiltered.csv` vocabulary file so that it only contains UMLS concepts belonging to the "Chemicals & Drugs" semantic group, the following command must be run (in Linux systems), where all `Txxx` codes correspond to semantic types within the "Chemicals & Drugs" semantic group:
```sh
cat AOD_unfiltered.csv | grep -E "T116|T195|T123|T122|T103|T120|T104|T200|T196|T126|T131|T125|T129|T130|T197|T114|T109|T121|T192|T127" > AOD.csv
```
  
**NOTE:** if the resulting vocabulary files are not stored in `vocabularies/`, it is necessary to configure the `[vocabularies]` variables in Settings.ini with their corresponding paths
