import json
import re
import pandas as pd

# Constants

df_pubmed = pd.read_csv('data/pubmed.csv')
df_clinical_trials = pd.read_csv('data/clinical_trials.csv')
df_drugs = pd.read_csv('data/drugs.csv')


def reformat_json(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Check if the line before the last line ends with a comma
    if lines[-2].rstrip().endswith(','):
        lines[-2] = lines[-2].rstrip()[:-1].rstrip() + '\n'

    with open(file_path, 'w') as file:
        file.writelines(lines)


def concat_pubmed(csv_file_path, json_file_path):
    # Read the CSV file into a DataFrame
    df_pubmed_csv = pd.read_csv(csv_file_path)

    # Read the JSON file into a DataFrame
    df_pubmed_json = pd.read_json(json_file_path)

    #  concat the DataFrames on a common DF
    df_pubmed = pd.concat([df_pubmed_csv, df_pubmed_json])

    return df_pubmed


# Function to parse dates
def parse_dates(df, column='date'):
    df[column] = pd.to_datetime(df[column], format='mixed')
    return df


# Function to remove special characters
def remove_special_characters(df, columns):
    for column in columns:
        pattern = re.compile(r'[^a-zA-Z0-9\s]')
        df[column] = df[column].apply(lambda x: pattern.sub('', str(x)))
    return df


# Function to find drug mentions in titles and creates the fields for the desired output

def find_drug_mentions(drug_name, df_pubmed_title, df_clinical_trials_title):
    matches = []

    for idx, row in df_pubmed_title.items():

        if drug_name.lower() in str(row).lower():  # Case-insensitive search
            date = df_pubmed.at[idx, 'date']
            journal = df_pubmed.at[idx, 'journal']

            formatted_date = date.strftime('%Y-%m-%d') if not pd.isnull(date) else None
            mention = {
                "title": row,
                "date": formatted_date,
                "journal": journal
            }
            matches.append(mention)

    for idx, row in df_clinical_trials_title.items():

        if drug_name.lower() in str(row).lower():  # Case-insensitive search
            date = df_clinical_trials.at[idx, 'date']
            journal = df_pubmed.at[idx, 'journal']
            formatted_date = date.strftime('%Y-%m-%d') if not pd.isnull(date) else None
            mention = {
                "title": row,
                "date": formatted_date,
                "journal": journal
            }
            matches.append(mention)

    return matches


def main():
    global df_pubmed, df_clinical_trials, df_drugs  # Declare global variables

    # reformat Json
    reformat_json('data/pubmed.json')

    # We preprocess the data
    print("Preprocessing the data...")

    # concat the files
    concat_pubmed('data/pubmed.csv', 'data/pubmed.json')

    # Parse dates
    df_pubmed = parse_dates(df_pubmed)
    df_clinical_trials = parse_dates(df_clinical_trials)

    # Remove special characters
    df_clinical_trials = remove_special_characters(df_clinical_trials, ['scientific_title', 'journal'])

    # We create the graph
    print("Creating the graph...")
    # Search for drug mentions in titles and create JSON output
    drug_mentions = {
        drug: find_drug_mentions(drug, df_pubmed['title'], df_clinical_trials['scientific_title'])
        for drug in df_drugs['drug']
    }

    # Save extracted information to a JSON file
    with open('data/graph.json', 'w') as json_file:
        json.dump(drug_mentions, json_file, indent=4, default=str)
    print("Pipeline execution finished.")


if __name__ == "__main__":
    main()
