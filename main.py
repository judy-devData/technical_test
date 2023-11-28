import json
import re
import pandas as pd


def reformat_json(file_path):
    """ reads the lines of the json file and removes the trailing comma to produce
        a valid json.
        Parameters:
        file_path:
        """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Check if the line before the last line ends with a comma
    if lines[-2].rstrip().endswith(','):
        lines[-2] = lines[-2].rstrip()[:-1].rstrip() + '\n'

    with open(file_path, 'w') as file:
        file.writelines(lines)


def concat_pubmed(csv_file_path, json_file_path):
    """ concatenate two data frames
        a valid json.
        Parameters:
        csv_file_path: the path of the csv file
        json_file_path: the path of the json file
        returns:
        df_pubmed: the concatenated df pubmed with the index reset

        """

    # Read the CSV file into a DataFrame
    df_pubmed_csv = pd.read_csv(csv_file_path)

    # Read the JSON file into a DataFrame
    df_pubmed_json = pd.read_json(json_file_path)

    #  concat the DataFrames on a common DF
    df_pubmed = pd.concat([df_pubmed_csv, df_pubmed_json], ignore_index=True)

    return df_pubmed


# Function to parse dates
def parse_dates(df, column='date'):
    """ formats the column date of a data frame
        Parameters:
        df
        date
        returns:
        df: data framed with the formatted unified date
        """

    df[column] = pd.to_datetime(df[column], format='mixed')
    return df


# Function to remove special characters
def remove_special_characters(df, columns):
    """ removes the special characters from a given column that don't fall into the category of a letter/number
        Parameters:
        df
        columns to remove the special characters from
        returns:
        df: data frame with the removed special characters
        """
    for column in columns:
        pattern = re.compile(r'[^a-zA-Z0-9\s]')
        df[column] = df[column].apply(lambda x: pattern.sub('', str(x)))
    return df


# Function to find drug mentions in titles and creates the fields for the desired output

def find_drug_mentions(drug_name, df_pubmed, df_trials, df_pubmed_title, df_trials_title):
    """ removes the special characters from a given column that don't fall into the category of a letter/number
        Parameters:
        drug name
        df : the two data frames to look for drug mentions within
        columns: the columns to consider within each data frame
        returns:
        matches: a list of dictionaries (mentions of the drugs) with keys (title, date, journal) and their respective values
        """
    matches = []

    for idx, row in df_pubmed_title.items():

        if drug_name.lower() in str(row).lower():  # Case-insensitive search
            date = df_pubmed.at[idx, 'date']
            journal = df_pubmed.at[idx, 'journal']

            formatted_date = date.strftime('%Y-%m-%d')
            mention = {
                "title": row,
                "date": formatted_date,
                "journal": journal
            }

            matches.append(mention)

    for idx, row in df_trials_title.items():

        if drug_name.lower() in str(row).lower():  # Case-insensitive search
            date = df_trials.at[idx, 'date']
            journal = df_pubmed.at[idx, 'journal']
            formatted_date = date.strftime('%Y-%m-%d')

            mention = {
                "title": row,
                "date": formatted_date,
                "journal": journal
            }
            matches.append(mention)

    return matches


def main():
    df_trials = pd.read_csv('data/clinical_trials.csv')
    df_drugs = pd.read_csv('data/drugs.csv')

    # We preprocess the data
    print("Preprocessing the data...")

    # reformat Json
    reformat_json('data/pubmed.json')

    # concat the files
    df_pubmed = concat_pubmed('data/pubmed.csv', 'data/pubmed.json')

    # Parse dates
    df_trials = parse_dates(df_trials)
    df_pubmed = parse_dates(df_pubmed)

    # Remove special characters
    df_trials = remove_special_characters(df_trials, ['scientific_title', 'journal'])

    # We create the graph
    print("Creating the graph...")
    # Search for drug mentions in titles and create JSON output
    drug_mentions = {
        drug: find_drug_mentions(drug, df_pubmed, df_trials, df_pubmed['title'], df_trials['scientific_title'])
        for drug in df_drugs['drug']
    }

    # # Save extracted information to a JSON file
    with open('data/graph.json', 'w') as json_file:
        json.dump(drug_mentions, json_file, indent=4, default=str)
    print("Pipeline execution finished.")


if __name__ == "__main__":
    main()
