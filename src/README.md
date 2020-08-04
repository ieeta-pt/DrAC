# What is DrAC
DrAC is a system that annotates medication information from clinical notes, harmonises extracted information and migrates it into an OMOP CDM database. The pipeline is divided in two independent components:

- First component: annotates drug information in clinical text and stores extracted information in a matrix structure;
- Second component: harmonises and migrates data into an OMOP CDM database.

The pipeline is divided in two major components to provide the possibility of improving a component without compromising the regular functioning of the other (_e.g._, improve the annotator's extraction mechanisms whilst maintaining the second component unmodified).

## Before starting
### Settings
The settings file is divided in the following 5 main sections:

```ini
[dataset]
name=< ds_name > 					#Dataset name
directory=../dataset/< ds_name > 	#Dataset name
neji_annotations=../results/
matrix_location=../results/

[vocabularies]
umls_rxnorm=../vocabularies/RXNORM.csv
umls_drugsbank=../vocabularies/DRUGBANK.csv
umls_aod=../vocabularies/AOD.csv
tuis=../vocabularies/MRSTY.RRF
output=../vocabularies/
ohdsi=../OHDSIVocabularies/

[post_vocabularies]
description=../vocabularies/DrugDescription.tsv
abrev=../vocabularies/Abreviations.tsv
black_list=../vocabularies/BlackList.tsv

[database]
datatype=< datatype >       #Server type (i.e., Postgres or other)
server=< server >           #Server location (i.e., localhost or other)
database=< database >       #Database name to be used
schema=< schema >           #Database schema
port=< port >               #Port of the database server
user=< user >               #User to access the database server
password=< password >       #Password to access the database server

[harmonisation]
usagi_input=../results/inputForUsagi.csv
usagi_output=../results/usagiExport.csv
dataset=< ds_type >         #Dataset to process (i.e., train, test or other)
matrix=../results/train_matrix.tsv
```

1. `[dataset]`: section used to define the name of the dataset on which the pipeline should be run (_e.g._, `name=2018_track2`), the path for the respective dataset (_e.g._, `directory=../dataset/2018_track2/`), the path where Neji annotations should be saved, and the path where the matrix with annotated information should be saved.

2. `[vocabularies]`: section used to define the name

### Help
For help, tip:

    $ python main.py -h
    
## First stage
datasets more info [here](https://github.com/bioinformatics-ua/DrAC/blob/master/dataset/README.md)

### Vocabulary creation
Explain the vocabulary creation
more info [here](https://github.com/bioinformatics-ua/DrAC/tree/master/vocabularies/README.md)

    $ python main.py -v
    
### Annotation
    $ python main.py -a
    
or read annotation neji, if already annotated
    
    $ python main.py -a -r

### Evaluator

    $ python main.py -e -r
    
or -d for more details
    
    $ python main.py -e -r -d
    
## Second stage
### Load OHDSI Vocabularies
    $ python main.py -o
    
more info [here](https://github.com/bioinformatics-ua/DrAC/blob/master/OHDSIVocabularies/README.md)
    
### Usagi
    $ python3 main.py -a -r -u

    mappings

<p align="center"><img src="https://github.com/bioinformatics-ua/DrAC/blob/master/images/UsagiConf.png" alt="UsagiConf"  border="0" /></p>

link para o repositorio Usagi

### Migrate
Creates the CSV file only
    
    $ python main.py -a -r -m

Creates the CSV file and migrates info to BD
    
    $ python main.py -a -r -m -l

results more info [here](https://github.com/bioinformatics-ua/DrAC/blob/master/results/README.md)
