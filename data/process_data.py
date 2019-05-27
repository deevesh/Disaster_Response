import sys
import pandas as pd
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    '''
    input:
        messages_filepath: Path of messages dataset.
        categories_filepath: Path of categories dataset.
    output:
        df: The merged dataset
    '''
    #load data from csv
    messages = pd.read_csv(messages_filepath) #load messages data from csv
    categories = pd.read_csv(categories_filepath) #load categories data from csv
    df = pd.merge(messages, categories, left_on='id', right_on='id', how='outer')
    return df

def clean_data(df):
    '''
    input:
        df: Merged dataset 
    output:
        df: The dataset after cleaning.
    '''
    # create a dataframe of the 36 individual category columns
	categories = df.categories.str.split(';', expand = True)
	# take the first row of the categories dataframe
    row = categories.loc[0]
    # use this row to extract a list of new column names for categories.
	# one way is to apply a lambda function that takes everything 
	# up to the second to last character of each string with slicing
    category_colnames = row.apply(lambda x: x[:-2]).values.tolist()
    categories.columns = category_colnames
    categories.related.loc[categories.related == 'related-2'] = 'related-1'
    
    #  loop through columns in the catagories
    for column in categories:
        categories[column] = categories[column].astype(str).str[-1]
        categories[column] = pd.to_numeric(categories[column])
    
    df.drop('categories', axis = 1, inplace = True)
    df = pd.concat([df, categories], axis = 1)
    df.drop_duplicates(subset = 'id', inplace = True) #removing the duplicates 
    
    return df

def save_data(df, database_filepath):
	# store the data in an SQL lite database using table name as 'merge_messages'
    engine = create_engine('sqlite:///' + database_filepath)
    df.to_sql('merge_messages', engine, index=False)

def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)

        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)

        print('Cleaned data is saved to database!')

    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')

if __name__ == '__main__':
    main()
