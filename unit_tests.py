import unittest
import pandas as pd
import re
import os
from main import (reformat_json, concat_pubmed, parse_dates, remove_special_characters, find_drug_mentions,
                  generate_graph)


class TestFunctions(unittest.TestCase):
    def setUp(self):
        # Setup any initial variables or data needed for tests
        self.csv_file = 'data/csv_file.csv'
        self.json_file = 'data/json_file.json'
        # Create sample DataFrames for testing
        pubmed_data = {
            'title': ['Title 1', 'Title 2', 'Title 3'],
            'date': ['2023-01-01', '2023-01-02', '2023-01-03'],
            'journal': ['Journal A', 'Journal B', 'Journal C']
        }
        trials_data = {
            'scientific_title': ['Sci Title 1', 'Sci Title 2', 'Sci Title 3'],
            'date': ['2023-01-01', '2023-01-02', '2023-01-03'],
            'journal': ['Journal X', 'Journal Y', 'Journal Z']
        }

        drug_data = {'drug': ['DrugA', 'DrugB', 'DrugC']}
        self.df_pubmed = pd.DataFrame(pubmed_data)
        self.df_trials = pd.DataFrame(trials_data)
        self.df_drugs = pd.DataFrame(drug_data)

    def test_reformat_json(self):
        # Create a temporary test JSON file
        bad_json = 'data/bad_json.json'
        with open(bad_json, 'w') as file:
            with open(bad_json, 'w') as file:
                file.write('[ \n')
                file.write('{"key1": "value1"},\n')
                file.write('{"key2": "value2"},\n')
                file.write(']\n')

        # Call the function to test
        reformat_json(bad_json)
        # Read the modified JSON file and check if the last comma is removed
        with open(bad_json, 'r') as file:
            lines = file.readlines()
            self.assertFalse(lines[-1].strip().endswith(','))  # Check for no trailing comma
        # Clean up/delete the test JSON file after the test
        os.remove(bad_json)

    def test_concat_pubmed(self):
        # Create some sample DataFrames for testing
        df_csv = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        df_json = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})

        # Save the DataFrames to test files (csv and json)
        df_csv.to_csv(self.csv_file, index=False)
        df_json.to_json(self.json_file)

        # Call the function to test
        df_result = concat_pubmed(self.csv_file, self.json_file)

        # Check if the output DataFrame has the expected shape
        self.assertEqual(df_result.shape, (4, 2))
        # remove the files
        os.remove('data/csv_file.csv')
        os.remove('data/json_file.json')

    def test_parse_dates(self):
        # Create a sample DataFrame for testing
        self.df = pd.DataFrame({'date': ['2023-01-01', '1 January 2020'], 'column2': ['a', 'b']})
        # Test the parse_dates function
        df_result = parse_dates(self.df, column='date')
        # Check if the 'date' column is converted to datetime
        self.assertEqual(df_result['date'].dtype, 'datetime64[ns]')  # Check if the column is of datetime type

    def test_remove_special_characters(self):
        self.df = pd.DataFrame({'column1': ['abc@123', 'def$456', 'ghi#789'],
                                'column2': ['!@#123', '*&$456', '%^&789']})
        # define the parameters needed for test
        columns_to_clean = ['column1', 'column2']
        cleaned_df = remove_special_characters(self.df, columns_to_clean)

        # Check if special characters are removed
        for col in columns_to_clean:
            for val in cleaned_df[col]:
                self.assertFalse(bool(re.search(r'[^a-zA-Z0-9\s]', str(val))))

        # Check if DataFrame shape remains the same
        self.assertEqual(self.df.shape, cleaned_df.shape)

    def test_find_drug_mentions(self):

        # Test the function's behavior
        drug_name = 'drug'
        df_pubmed_title = self.df_pubmed['title']
        df_trials_title = self.df_trials['scientific_title']

        # Call the function to find drug mentions
        matches = find_drug_mentions(drug_name, self.df_pubmed, self.df_trials, df_pubmed_title, df_trials_title)

        # Verify the expected structure of matches
        self.assertIsInstance(matches, list)
        self.assertTrue(all(isinstance(mention, dict) for mention in matches))
        for mention in matches:
            self.assertIn('title', mention)
            self.assertIn('date', mention)
            self.assertIn('journal', mention)
            self.assertIsInstance(mention['title'], str)
            self.assertIsInstance(mention['date'], str)
            self.assertIsInstance(mention['journal'], str)

    def test_generate_graph(self):
        # Call the function to test
        drug_mentions = generate_graph(self.df_drugs, self.df_pubmed, self.df_trials)

        # Perform assertions based on expected output structure or content
        self.assertIsInstance(drug_mentions, dict)  # Check if the output is a dictionary

        # Assuming we know the expected structure of the output
        # Replace these expected values with your actual expected results
        expected_keys = ['DrugA', 'DrugB', 'DrugC']
        expected_value_structure = {'title': str, 'date': str, 'journal': str}

        for drug, mentions in drug_mentions.items():
            self.assertIn(drug, expected_keys)  # Check if drug names are keys in the output

            for mention in mentions:
                self.assertIsInstance(mention, dict)  # Check if each mention is a dictionary
                for key, value_type in expected_value_structure.items():
                    self.assertIn(key, mention)  # Check if the required keys are present
                    self.assertIsInstance(mention[key], value_type)  # Check the value types


if __name__ == '__main__':
    unittest.main()
