"""
Report tag
"""

import os
import docutils.core 
import tempfile
import uuid


from jinja2 import Template
from m2r import convert
from mldev.experiment_tag import experiment_tag
from mldev.experiment import BasicStage
from docutils.writers.html4css1 import Writer
from .loadfile import LoadFile
from .table import Table
from .graphic import Graphic
from .report_styles import ReportStyles


@experiment_tag()
class Report(BasicStage):
    def __init__(self, name, output_dir, template, report_model, theme = "light" , lang = "en"):
        self.__name = name
        self.__output_dir = output_dir
        self.__template = template
        self.__report_model = report_model
        self.__theme = theme
        self.__lang = lang

        self.__tmp_dir = None
        self.__rst_temp = None
        

    def __call__(self, *args, **kwargs):
        with tempfile.TemporaryDirectory() as tmpdirname:
            self.__tmp_dir = tmpdirname

            self.load_data(self.__report_model)

            rendered_file = self.fill_template()
            rst = self.convert_md_2_rst(rendered_file)
        
            self.create_result(rst)


    def load_data(self, model):
        for key in list(model.keys()):
            if isinstance(model[key], LoadFile):
                model[key] = model[key].data
            elif isinstance(model[key], Table) or isinstance(model[key], Graphic):
                model[key] = model[key].rst
            elif isinstance(model[key], dict) and len(list(model[key])) != 0:
                self.load_data(model[key])


    def fill_template(self):
        with open(self.__template, 'r') as template:
            md_text = Template(template.read(), trim_blocks=True)

        filled_template = md_text.render(repo=self.__report_model)
        return filled_template


    def convert_md_2_rst(self, rendered_file):
        rst = convert(rendered_file)
        return rst

    
    def create_result(self, rst):
        if not os.path.exists(self.__output_dir):
            os.makedirs(self.__output_dir, 0o755)
        res_path = os.path.join(self.__output_dir, self.__name + ".html")


        report_styles = ReportStyles(res_dir=self.__output_dir, 
                                     theme=self.__theme, 
                                     lang=self.__lang)
        report_styles.copy_assets()

        html = docutils.core.publish_string( rst, writer=Writer()) 
        result = report_styles.render_result(html.decode('UTF-8'))

        with open(res_path, 'w+') as res:
            res.write(result)
            res.close()