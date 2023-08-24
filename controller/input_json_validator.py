# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import json


class JSONSchemaGenerator:
    def __init__(self, file_object):
        self.json_obj = self.check_for_valid_json(file_object)
        self.json_schema = self.prepare_json()
        self.describe_tables_list = self.get_describe_schema_tables()

    def prepare_json(self):
        tables_schema = {}
        for data in self.json_obj:
            table_name = data['name']
            attributes = data['attributes'] if "attributes" in data else []

            # hash_key, sort_key = get_table_key_attributes(table_name)
            # print(hash_key)
            # print(sort_key)
            table_region = {'region': data['region']}
            attribute_dict = {}
            for attribute in attributes:
                attribute_name = attribute['name']
                attribute_type = attribute['type']
                attribute_dict[attribute_name] = attribute_type
            tables_schema[table_name] = {"attributes": attribute_dict}
            tables_schema[table_name].update(table_region)
        return tables_schema

    def get_describe_schema_tables(self):
        desc_table_lst = []
        for key, val in self.json_schema.items():
            desc_table_lst.append(key)
        return desc_table_lst

    @staticmethod
    def check_for_valid_json(file_obj):
        try:
            json_obj = json.load(file_obj)
            return json_obj
        except ValueError as err:
            raise err

