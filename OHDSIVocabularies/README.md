# OHDSI Vocabularies

This directory must have the OHDSI standard vocabularies. In order to download them, go to the official repository available [here](https://athena.ohdsi.org) and select the following vocabularies:

- Snomed
- RXNorm

After selecting the vocabularies, extract their CSV files and save them in this directory. It possible to store the OHDSI vocabulary files in a different directory, however it is necessary to change the `ohdsi` directory in the settings file accordingly.

These vocabularies can then be loaded into the database as described [here](https://github.com/bioinformatics-ua/DrAC/blob/master/src/README.md#load-ohdsi-vocabularies), and be also used as a database for the Usagi tool during the [harmonisation procedure](https://github.com/bioinformatics-ua/DrAC/blob/master/src/README.md#usagi).
