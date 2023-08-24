# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

"""
Generates model and CRUD operations classes for a given JSON input file.
"""
import argparse
import logging
from datetime import datetime
from controller.dynamo_connection import DynamoConnection
from controller.generate_model import GenerateModel
from controller.input_json_validator import JSONSchemaGenerator
from controller.generate_crud import GenerateCrud

# Configure logging
logging.basicConfig(
    filename=f'log_{datetime.today().strftime("%Y-%m-%d")}.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')


# Create the parser
parser = argparse.ArgumentParser(
    description='Input json file to generate model and controllers for DynamoDB tables')

# Add arguments
parser.add_argument('--file', type=str,
                    help='Json file location that contains DDB table names and schema information')

# Parse the arguments
args = parser.parse_args()

try:
    # Read the JSON file
    with open(args.file, 'r', encoding="utf-8") as json_file:
        try:
            # Send the Input JSON File Object for Validation
            json_schema_obj = JSONSchemaGenerator(json_file)
            schema = json_schema_obj.json_schema
            describe_table_list = json_schema_obj.describe_tables_list
        except Exception as e:
            logging.error(f"Error: Input is not a valid JSON. {e}")
            raise e

    dynamo_connection = DynamoConnection(describe_table_list, schema)
    table_attributes, unprocessed_tables = dynamo_connection.get_basic_attributes()
    logging.info(table_attributes)
    logging.warning(unprocessed_tables)

    # generating the Model
    logging.info('Generating Model ....')
    model_generation = GenerateModel('templates')
    model_generation.render_template(table_attributes)
    logging.info('Model generated.')

    # generating the CRUD
    logging.info('Generating CRUD ....')
    crud_generation = GenerateCrud('templates')
    ''' 
    updating the describe_table_list based on the unprocessed 
    tables to avoid creating CRUD for such tables
    '''
    if unprocessed_tables:
        for table_name in unprocessed_tables.keys():
            describe_table_list.remove(table_name)

    crud_generation.render_template(describe_table_list)

    # Displaying Warning
    if unprocessed_tables:
        print(f'The following tables are not processed:')
        print(unprocessed_tables)


except FileNotFoundError:
    logging.error("Error: File not found.")
except IOError as e:
    logging.error(f"Error: Failed to read file. {e}")
