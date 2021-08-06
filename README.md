# Search Term Analyser
## Overview
Details needed once implemented

## Main Application Guide
"INSERT RUNNING DETAILS HERE"

## Tools and languages
- Python 3.8 - for code development and unit testing
- pytest - framework for unit testing
- nose2 - library used as unit test runner

## Testing & Requirements Guide
The following make commands can be used in the command line:
- `make requirements` : uses pip to install the various packages within the requirements.txt file (this command is 
ran at the start of the other make commands below)
- `make unittest` : uses nose2 and pytest to run all the unit tests within the repository
- `make cov` : uses nose2 and pytest to run all the unit tests within the repository and also gives the coverage 
of the code
- `make covhtml` : uses nose2 and pytest to run all the unit tests within the repository and also gives the coverage 
of the code in a html format which is opened in firefox
- `make start` : uses pythonpath and runs the main.py file, starting the application to continuously check the 
folder for CSV files, with a delay of 20 seconds after every file has been checked before checking again.
