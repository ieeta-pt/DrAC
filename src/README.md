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
umls_rxnorm=../vocabularies/< rxnorm_file >      #Path for the unformated RxNorm dictionary
umls_drugbank=../vocabularies/< drugbank_file >  #Path for the unformated DrugBank dictionary
umls_aod=../vocabularies/< aod_file >            #Path for the unformated AOD dictionary
tuis=../vocabularies/< mrsty_file >              #Path for the UMLS semantic type mapping file
output=../vocabularies/                          #Output path where the final formated Neji vocabularies will be saved
ohdsi=../OHDSIVocabularies/                      #Output path where the final OHDSIVocabularies will be saved

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
usagi_input=../results/< usagi_in >         #Path with the input file for Usagi
usagi_output=../results/< usagi_out >       #Output path to export Usagi validated information
dataset=< ds_type >                         #Dataset to process (i.e., train, test or other)
matrix=../results/< matrix_file >           #Path where the matrix with extracted information was saved in the pipeline's annotating stage 
```

| Field           | Description |
|-----------------|-------------|
|`[dataset]`|Section used to define the name of the dataset on which the pipeline should be run (_e.g._, `name=2018_track2`), the path for the respective dataset (_e.g._, `directory=../dataset/2018_track2/`), the path where Neji annotations should be saved, and the path where the matrix with annotated information should be saved.|
|`[vocabularies]`|Section used to define the paths for the dictionary files and paths used in the first component (`umls_rxnorm`, `umls_drugbank`,`umls_aod`, `tuis`, `output`) and in the second component (`ohdsi`).|
|`[post_vocabularies]`|Section used to define the paths for additional resource files used in the post processing stage of the annotator.| 
|`[database]`|Section used to define the parameters for creating the database and establishing a connection with it. |
|`[harmonisation]`|Section used to define the necessary paths for the harmonisation procedure, which involves the `matrix` file containing extracted information and Usagi input and output files.| 
    
## First stage: Clinical document annotation
The first stage of the pipeline is responsible for annotating drug information in clinical text and storing all extracted information in a matrix structure.
This stage is divided in the following parts:

### Vocabulary creation
To create vocabulary files for the Neji annotating system, it is firstly necessary to create domain specific vocabulary files following the procedure presented [here](https://github.com/bioinformatics-ua/DrAC/tree/master/vocabularies/README.md)

Once the previous vocabulary files are created, it is necessary to filter and format them to be compliant with Neji. For this, firstly ensure that the variables `umls_rxnorm`, `umls_drugbank` and `umls_aod` are correctly defined. Then, simply run the following command to create Neji compliant dictionary files.

    $ python main.py -v

After running the above command, three dictionary files will be created in the `output` directory which can then be uploaded to the Neji annotation service.

### Annotation
After creating the necessary vocabularies and configuring the Neji annotation web-service (the url for the web-service can be changed in `Annotator.py` by updating the `url` variable in the `Annotator` class), it is possible to annotate the clinical text documents by running the following command:

    $ python main.py -a
    
The resulting Neji annotations are saved in the `neji_annotations` path. Since the process of annotating documents with Neji can take some time, it is possible to reuse previously stored Neji annotations. For that, add the flag `-r` or `--read-ann` to the command:
        
    $ python main.py -a -r
    
This command bypasses the Neji annotation step by reading previous Neji annotations, which can then be processed in the post-processing stage of the annotation module. The final output of the Annotation module is a matrix with extracted information which is saved at the `matrix_location` directory.

### Evaluator
When a dataset provides gold standard annotations, it is possible to evaluate the performance of the annotation component by running the evaluation mode `-e`  with `-r` to use pre-existing Neji annotations. For that, run the following command:

    $ python main.py -e -r
 
This mode evaluates annotations at two different stages: firstly it evaluates the original annotations obtained from Neji, and secondly it evaluates post-processed annotations. It is possible to obtain a more detailed list of results by adding the `-d` or `--detail-eva` flag:
    
    $ python main.py -e -r -d
    
## Second stage: Harmonisation and migration of extracted data
The second stage of the pipeline is responsible for harmonising information stored in the matrix structure and migrating it into an OMOP CDM database.
This stage is divided in the following parts:

### Load OHDSI Vocabularies
Before harmonising extracted information it is necessary to prepare the OHDSI vocabularies. Firstly, ensure that these vocabularies are correctly set-up by following [these instructions](https://github.com/bioinformatics-ua/DrAC/tree/master/OHDSIVocabularies#ohdsi-vocabularies). Once these resources are set-up, it is necessary to load the vocabularies into the database by running the system with the `-o` or `--load-ohdsi-voc` flag: 

    $ python main.py -o
   
### Usagi Mapping Validation
Next, it is necessary to validate the mappings from extracted information to standard vocabularies using the Usagi tool. To create the input file for the Usagi tool, run the system in annotation mode with the `-u` or `--usagi-input` complementary flag:

    $ python3 main.py -a -r -u

The system will generate a CSV file and save it at the `usagi_input` directory defined in the settings file. Next, it is necessary to download the [Usagi tool](https://github.com/OHDSI/Usagi). When running Usagi for the first time, the user is prompted to provide the location of the desired [OHDSI vocabularies](https://github.com/bioinformatics-ua/DrAC/tree/master/OHDSIVocabularies#ohdsi-vocabularies) so that Usagi can create the index. After the index is created, import the `usagi_input` file selecting the options presented in the figure below:

<p align="center"><img src="https://github.com/bioinformatics-ua/DrAC/blob/master/images/UsagiConf.png" alt="UsagiConf"  border="0" /></p>

Once the input file is imported, Usagi generates mapping suggestions for each concept to the standard vocabularies. Each mapping has a similarity score which represents the confidence of the suggestion. The user can validate each mapping and correct it to another standard concept if necessary. Finally, export the validated mappings file to the `usagi_output` directory.

### Migrate data
The last step in the pipeline is to harmonise content stored in the `matrix` file using Usagi validated mappings and migrate it. To proceed with the harmonisation process and migrate the resulting data to the OMOP CDM Schema, run the system in annotation mode with the `-m` or `--migrate` complementary flag:
    
    $ python main.py -a -r -m
    
This command migrates data into the schema and saves the result of the migration process in a CSV file in the `results/` folder. However, it is also possible to migrate data into the OMOP CDM schema and automatically load it into the database. For that, simply add the `-l`or `--load-db` complementary flag to the previous command:

    $ python main.py -a -r -m -l

## Results
By preset, the `results/` folder is used to store output files generated when running the system, such as the Neji annotations file, the matrix file or the Usagi output file. For more information on the content stored in the `results/` folder, please refer to its [page](https://github.com/bioinformatics-ua/DrAC/blob/master/results/README.md).

## Help
For help, type the following command:

    $ python main.py -h
    
|Settings Flag|Description|
|---|---|
|-s SETTINGS_FILE, --settings SETTINGS_FILE|The system settings file (default: ../settings.ini)|

|Execution Flags|Description|
|---|---|
|-v, --voc-builder|In this mode, the system will create the vocabularies to use in Neji (default: False)|
|-a, --annotate|In this mode, the system will annotate the dataset (default: False)|
|-e, --evaluate|In this mode, the system will read the annotations and evaluate the dataset without converting it to the matrix (default: False)|
|-o, --load-ohdsi-voc|In this mode, the system will load the OHDSI vocabularies into the database (default: False)|

|Complementary Flags|Description|
|---|---|
|-r, --read-ann|This flag is complementary to the --annotate or --evaluate execution mode. With this flag activated, the system will use the previously stored Neji annotations (default: False)|
|-d, --detail-eva|This flag is complementary to the --evaluate execution mode. With this flag activated, the system will detail the evaluation by presenting all the false positives and negatives using the dataset (default: False)|
|-u, --usagi-input|This flag is complementary to the --annotate execution mode. With this flag activated, the system will create the input file to use in the Usagi tool (default: False)|
|-m, --migrate|This flag is complementary to the --annotate execution mode. With this flag activated, the system will load the annotated results into the OMOP CDM Schema (default: False)|
|-l, --load-db|This flag is complementary to the --annotate execution mode and it only works if the --migrate flag is active. With this flag activated, the system will load the annotated results into the database (default:False)|        

