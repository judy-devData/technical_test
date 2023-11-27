# Intro

This project is a data pipeline that creates a graph which links  drugs with their mentions in clinical trials, medical publications and journals.

it includes 3 sources of data : 
* A list of drugs (csv file)
* A list of medical publications associated to a scientific journal and to a publication date (separated between a csv file and a json file)
* A list of clinical trials associated to a scientific journal and to a publication date (csv file) 

It then outputs the graph as a json file.    

# Processing

This data pipeline contains 4 functions to ensure the pre processing step:
* def reformat_json(file_path) : to reformat the pubmed json file and remove the trailing comma.
* def concat_pubmed(csv_file_path, json_file_path): to concat both files of pubmed.
* def parse_dates(df, column='date'): to Harmonize the dates.
* def remove_special_characters : to remove special characters from clinical trials file.

The graph is then created with find_drug_mentions(drug_name, df_pubmed_title, df_clinical_trials_title) 


# Usage

This project was developped with Python 3.9.1

You can clone this repo by downloading from github or simply clone it from your terminal

``````

To use this project, you need the pandas V2.1.3 library installed. the required packages and versions are contained in the Pipfile and Pipefile.lock

pipenv install

``````

Then to run the data pipeline, make sure to be in the repo base folder and then run the main.py : 

```python main.py```

# Ad Hoc Processing

```python ad_hoc.py```


# To go further 

To make this data pipeline able to handle large volumes of data we could : 
* Partition the data input files to parallelize processing
* Pandas is excellent for data manipulation and analysis on a single machine, it might encounter limitations when handling large datasets that don't fit into memory.
* You could use a Flink job based on PyFlink. Which leverages distributed computing frameworks for improved performance with parallel processing, making it more suitable for large scale data processing scenarios where processing time is critical.
* Pyflink/Pyspark would allow a  multithreading or multiprocessing approach which would be more suitable for large scale data.


# Part 2 : SQL

Please find the 2 SQL queries in the 'sql' folder of this repo.