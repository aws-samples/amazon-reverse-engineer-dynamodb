# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from jinja2 import Environment, FileSystemLoader

class CreateScript:
    """
        Create a script
    """
    def __init__(self, filename, code):
        self.script_name = 'crud/'+filename + '.py'
        self.script_code = code

    def create_file(self):
        """
            Create a file

        Returns:
            _type_: _description_
        """        
        with open(self.script_name, 'w') as file:
            file.write(self.script_code)

        return None


class GenerateCrud:

    def __init__(self, template_location):
        file_loader = FileSystemLoader(template_location)
        env = Environment(loader=file_loader, autoescape=True)
        self.template = env.get_template('crud.jinja')

    def render_template(self, DDB_tables):

        output = self.template.render(tables=DDB_tables)

        # print(output)
        script = CreateScript('demo_crud', output)
        script.create_file()
