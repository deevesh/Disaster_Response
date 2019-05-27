# Disaster Response Pipeline

In this project we have to analyze disaster data from Figure Eight in order to build a model for an API which can classify disaster messages. 

The project workspace contains a data set with real messages that were sent during disasters. I had to create a ML pipeline to categorize these events so that the messages could be sent to the appropriate disaster relief agency. 

In the current repository, we have 3 folders:
1. app:  Flask Web App which will be taking the user message and classify them into 36 categories
2. data: contains the 2 datasets and the ETL Pipeline (process_data.py) which loads the messages, cleans the data stores and stores it in a SQLite database.  
3. models: contains the ML Pipeline (train_classifier.py) that loads the data from SQLite database, and build a text processing model using GridSearchCV in order to create a model, exporting it as a pickle file. 


### Instructions:
Run the following commands in the project's root directory to set up your database and model.

To run ETL pipeline that cleans data and stores in the database:
python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db

To run ML pipeline that trains classifier and saves the model:
python models/train_classifier.py data/DisasterResponse.db models/msg_classifier.pkl

Run the following command in the app's directory to run your web app:
python run.py

Go to http://0.0.0.0:3001/ to launch the web application. 
