"""
LoadFile tag
"""

import json
import pandas 

from mldev.experiment_tag import experiment_tag
from .supported_file_formats import Supported_Formats

@experiment_tag()
class LoadFile:
    def __init__ (self, url, filter_fields = None, filter_columns = None):
        self.__url = url
        self.__data = None
        self.__filter_fields = filter_fields     # to filter JSON
        self.__filter_columns = filter_columns   # to filter CSV

    @property
    def data(self):
        extention = self.__url.split(".")[-1]

        if extention == Supported_Formats.JSON:
            with open(self.__url) as f:
                self.__data = json.load(f)

            if self.__filter_fields != None:
                self.__data = {key: self.__data[key] for key in self.__data if key not in self.__filter_fields}


        if extention == Supported_Formats.CSV:
            self.__data = pandas.read_csv(self.__url)

            if self.__filter_columns != None:
                requered_columns = [key for key in list(self.__data.columns) if key not in self.__filter_columns]
                self.__data = self.__data[[requered_columns]]

        return self.__data
    
      