# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

"""
    Connects to AWS DynamoDB and returns attributes for each table
"""
from typing import Union
import logging
import boto3


class DynamoConnection:
    """
        Connects to AWS DynamoDB and returns attributes for each table
    """
    def __init__(self, table_name: Union[list[str], str], table_schema):
        self.table = table_name
        self.table_schema = table_schema
        self.dynamo_client = boto3.client('dynamodb')

    def customize_attribute_response(self, attributes):
        """
        Customize the attributes

        Args:
            attributes (_type_): _description_
        """        
        if attributes.get('AttributeDefinitions') and attributes.get('KeySchema'):
            for attribute_definition in attributes.get('AttributeDefinitions'):
                for key_schema in attributes.get('KeySchema'):
                    if key_schema.get('AttributeName') == attribute_definition.get('AttributeName'):
                        key_schema['AttributeType'] = attribute_definition.get(
                            'AttributeType')

        if attributes.get('AttributeDefinitions'):
            for attribute_definition in attributes.get('AttributeDefinitions'):
                if attributes.get('GlobalSecondaryIndexes'):
                    for gsi_data in attributes.get('GlobalSecondaryIndexes'):
                        for key_schema in gsi_data.get('KeySchema'):
                            if key_schema.get('AttributeName') == attribute_definition.get('AttributeName'):
                                key_schema['AttributeType'] = attribute_definition.get(
                                    'AttributeType')
                if attributes.get('LocalSecondaryIndexes'):
                    for lsi_data in attributes.get('LocalSecondaryIndexes'):
                        for key_schema in lsi_data.get('KeySchema'):
                            if key_schema.get('AttributeName') == attribute_definition.get('AttributeName'):
                                key_schema['AttributeType'] = attribute_definition.get(
                                    'AttributeType')

    def get_basic_attributes(self):
        """
            Retrieve the basic attributes

        Returns:
            _type_: result_attributes, unprocessed_tables
        """
        self.table = [self.table] if isinstance(
            self.table, str) else self.table
        result_attributes = dict()
        unprocessed_tables = dict()
        for table in self.table:
            try:
                table_desc = self.dynamo_client.describe_table(TableName=table)
                logging.info(table_desc)
                # fetching the attributes, GSI and LSI
                result_attributes[table] = {
                    'AttributeDefinitions': table_desc['Table'].get('AttributeDefinitions'),
                    'KeySchema': table_desc['Table'].get('KeySchema'),
                    'LocalSecondaryIndexes': table_desc['Table'].get('LocalSecondaryIndexes'),
                    'GlobalSecondaryIndexes': table_desc['Table'].get('GlobalSecondaryIndexes'),
                    'UserAttributes': self.table_schema[table].get('attributes', []),
                    'Region': self.table_schema[table].get('region', 'ap-south-1'),
                }

                self.customize_attribute_response(result_attributes[table])

            except Exception as exception:
                logging.warning(exception)
                unprocessed_tables[table] = str(exception)

        return result_attributes, unprocessed_tables
