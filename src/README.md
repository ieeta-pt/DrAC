# Using the system
Introdutory text

## Before start
### Settings
Settings structure Explain

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
