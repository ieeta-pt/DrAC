# What is DrAC
DrAC is a system that annotates medication information from clinical notes, harmonises extracted information and migrates it into an OMOP CDM database. The pipeline is divided in two independent components:

- First component: annotates drug information in clinical text and stores extracted information in a matrix structure;
- Second component: harmonises and migrates data into an OMOP CDM database.

The pipeline is divided in two major components to provide the possibility of improving a component without compromising the regular functioning of the other (_e.g._, improve the annotator's extraction mechanisms whilst maintaining the second component unmodified). The proposed pipeline was validated in two different public datasets, as described [here](https://github.com/bioinformatics-ua/DrAC/blob/master/dataset/README.md).

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

2. `[vocabularies]`: section used to define the paths for the dictionaries used in the first component (`umls_rxnorm`, `umls_drugsbank`,`umls_aod`, `tuis`, `output`) and for the second component (`ohdsi`).


### Help
For help, tip:

    $ python main.py -h
    
## First stage
The first stage of the pipeline is responsible for annotating drug information in clinical text and storing all extracted information in a matrix structure.
This stage is divided in the following parts:

### Vocabulary creation
To create vocabulary files for the Neji annotating system, it is firstly necessary to create domain specific vocabulary files following the procedure presented [here](https://github.com/bioinformatics-ua/DrAC/tree/master/vocabularies/README.md)

Once the previous vocabulary files are created, it is necessary to filter and format them to be compliant with Neji. For this, firstly ensure that the variables `umls_rxnorm`, `umls_drugsbank` and `umls_aod` are correctly defined. Then, simply run the following command to create Neji compliant dictionary files.

    $ python main.py -v

After running the above command, three dictionary files will be created in the `output` directory which can then be uploaded to the Neji annotating service.



### Annotation
    $ python main.py -a
    
anotador webservice pode ser mudado se mudarem a variável url na classe `Annotator` do `Annotator.py`
    
or read annotation neji, if already annotated
    
    $ python main.py -a -r
    
the result is a matrix that is saved



### Evaluator

    $ python main.py -e -r
    
or -d for more details
    
    $ python main.py -e -r -d
    
    
    
## Second stage
The second stage of the pipeline is responsible for harmonising information stored in the matrix structure and migrating it into an OMOP CDM database.
This stage is divided in the following parts:

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
