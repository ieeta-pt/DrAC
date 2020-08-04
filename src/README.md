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
name=< ds_name > 		        #Dataset name
directory=../dataset/< ds_name > 	#Dataset name
neji_annotations=../results/            #Path where Neji annotations will be saved
matrix_location=../results/             #Path where the matrix will be saved

[vocabularies]
umls_rxnorm=../vocabularies/RXNORM.csv      #Path for the unformated RxNorm dictionary
umls_drugbank=../vocabularies/DRUGBANK.csv  #Path for the unformated DrugBank dictionary
umls_aod=../vocabularies/AOD.csv            #Path for the unformated AOD dictionary
tuis=../vocabularies/MRSTY.RRF              #Path for the UMLS semantic type mapping file
output=../vocabularies/                     #Output path where the final formated Neji vocabularies will be saved
ohdsi=../OHDSIVocabularies/                 #Output path where the final OHDSIVocabularies will be saved

[post_vocabularies]
description=../vocabularies/DrugDescription.tsv     #Drug description vocabulary used in the post processing stage of the annotator
abrev=../vocabularies/Abreviations.tsv              #List of abbreviations to be used during the post processing stage of the annotator
black_list=../vocabularies/BlackList.tsv            #List of terms to be removed during the post processing stage of the annotator

[database]
datatype=< datatype >       #Server type (i.e., Postgres or other)
server=< server >           #Server location (i.e., localhost or other)
database=< database >       #Database name to be used
schema=< schema >           #Database schema
port=< port >               #Port of the database server
user=< user >               #User to access the database server
password=< password >       #Password to access the database server

[harmonisation]
usagi_input=../results/inputForUsagi.csv    #Path with the input file for Usagi
usagi_output=../results/usagiExport.csv     #Output path to export Usagi validated information
dataset=< ds_type >                         #Dataset to process (i.e., train, test or other)
matrix=../results/train_matrix.tsv          #Path where the matrix with extracted information was saved in the pipeline's annotating stage 
```

1. `[dataset]`: section used to define the name of the dataset on which the pipeline should be run (_e.g._, `name=2018_track2`), the path for the respective dataset (_e.g._, `directory=../dataset/2018_track2/`), the path where Neji annotations should be saved, and the path where the matrix with annotated information should be saved.

2. `[vocabularies]`: section used to define the paths for the dictionaries and paths used in the first component (`umls_rxnorm`, `umls_drugbank`,`umls_aod`, `tuis`, `output`) and for the second component (`ohdsi`).


### Help
For help, tip:

    $ python main.py -h
    
## First stage
The first stage of the pipeline is responsible for annotating drug information in clinical text and storing all extracted information in a matrix structure.
This stage is divided in the following parts:

### Vocabulary creation
To create vocabulary files for the Neji annotating system, it is firstly necessary to create domain specific vocabulary files following the procedure presented [here](https://github.com/bioinformatics-ua/DrAC/tree/master/vocabularies/README.md)

Once the previous vocabulary files are created, it is necessary to filter and format them to be compliant with Neji. For this, firstly ensure that the variables `umls_rxnorm`, `umls_drugbank` and `umls_aod` are correctly defined. Then, simply run the following command to create Neji compliant dictionary files.

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
    
loads more info [here](https://github.com/bioinformatics-ua/DrAC/blob/master/OHDSIVocabularies/README.md) and creates vocabularies in the output directory  
   
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
