# Results

The `results/` folder is used as the preset directory for storing output files generated when running the system pipeline.
The default files provided in the repository resulted from running the system with the documents provided in [`examples/`](https://github.com/bioinformatics-ua/DrAC/tree/master/dataset/examples).
The resulting list of default files includes:
- `DRUG_EXPOSURE.csv` - CSV file with the content for the Drug Exposure table ready to be loaded into the OMOP CDM database;
- `NOTE.csv` - CSV file with the content for the Note table ready to be loaded into the OMOP CDM database;
- `NOTE_NLP.csv` - CSV file with the content for the Note NLP table ready to be loaded into the OMOP CDM database;
- `inputForUsagi.csv` - Input file to be used in Usagi for mapping validation;
- `mappings.csv` - File containing all Usagi mappings in a format that is editable by the tool (this file is additional, not necessary);
- `train_matrix.tsv` - Matrix file containing extracted information obtained from the annotation module;
- `train_nejiann.tsv` - File containing saved Neji annotations;
- `usagiExport.csv` - File exported from Usagi after validating the mappings between extracted concepts and concepts from the standard vocabularies.

NOTE: `mappings.csv` and `usagiExport.csv` are different files as `mappings.csv` contains all mappings in an editable format, whereas `usagiExport.csv` only contains approved mappings.
The ETL procedures used in this system only require the `usagiExport.csv` file.
