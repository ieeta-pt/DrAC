# OMOP CDM Tables
In this directory, there are the python files used in the system to automatically create the OMOP CDM Tables required to receive the information extracted. However, the tables for the standard vocabularies are not created by the system.
This system creates and fills the following tables:
- Person
- Visit_occurrence
- Drug_Exposure
- Note
- Note_NLP

In order to have the standard OHDSI vocabularies in your system, you must download them from the official repository available at https://athena.ohdsi.org