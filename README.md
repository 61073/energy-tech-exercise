# House Heating Analysis Application
## Overview
Uses a list of heating data for a number of customer houses and uses this along with a Weather API and heat pump data,
 to calculate the recommended heat pump requirements and costs for each house. It currently outputs the data as a
 formatted string. 2 examples are shown below, one as a success and another with missing weather/location data.
The output string will show each house's data one after the other continuously.

###Success Example:
    --------------------------------------
    e21a3149-b88c-40e9-86fd-c94a6b93cb78
    --------------------------------------
    Estimated Heat Loss = 8906
    Design Region = W Pennines (Ringway)
    Power Heat Loss = 4
    Recommended Heat Pump = 5kW Package
    Cost Breakdown:
     Design & Supply of your Air Source Heat Pump System Components (5kW), 3947.00
     Installation of your Air Source Heat Pump and Hot Water Cylinder, 2900.00
     Supply & Installation of your Homely Smart Thermostat, 150.00
     Supply & Installation of a new Consumer Unit, 300.00
     MCS System Commissioning & HIES Insurance-backed Warranty, 1648.00
    Total Cost, including VAT = 9392.25

###Missing weather Example:
    --------------------------------------
    e21a3149-b88c-40e9-86fd-c94a6b93cb78
    --------------------------------------
    Heating Loss: 16500
    Warning: Could not find design region

## Main Application Guide
This application is intended to be used as an AWS lambda using the lambda_handler method in heating_analyser_lambda.py
 as the input. The lambda requires an input of house heating data in a list as described in the docstrings
 documentation.

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
- `make start` : uses pythonpath and runs the heating_analyser_lambda.py file, starting lambda_handler method with 5
 example files to be processed, and prints the response
