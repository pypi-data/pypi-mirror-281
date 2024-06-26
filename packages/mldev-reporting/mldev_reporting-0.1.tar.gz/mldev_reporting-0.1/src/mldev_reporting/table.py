"""
Tabls tag
"""

import pandas

from mldev.experiment_tag import experiment_tag
from .supported_file_formats import Supported_Formats


@experiment_tag()
class Table:
    def __init__(self, title, headers = None, rows = None, data = None, widths = None, header_rows = None):
        self.__useInline = True if data == None else False

        if self.__useInline :
            if not isinstance(headers, list):
                raise Exception("MLDEV Reporting Exeption: headers set to not array value while using inline data")

            if not isinstance(rows, list):
                raise Exception("MLDEV Reporting Exeption: rows set to not array value while using inline data")

            if not isinstance(rows[0], list):
                raise Exception("MLDEV Reporting Exeption: row set to not array value while using inline data")
        else:
            if isinstance(headers, list):
                raise Exception("MLDEV Reporting Exeption: headers set to array value while using data from file")

            if isinstance(rows, list):
                raise Exception("MLDEV Reporting Exeption: rows set to array value while using data from file")

        self.__data = data
        self.__title = title
        self.__headers = headers
        self.__rows = rows
        self.__widths = widths
        self.__header_rows = header_rows if header_rows != None else 1

    
    @property
    def rst(self):
        table_headers = None
        table_rows = None

        if not self.__useInline: 
            table_data = self.__data.data

        self.__isCSV = isinstance(table_data, pandas.DataFrame)

        if self.__isCSV:
            table_headers = list(table_data.columns)
            table_rows = table_data.values.tolist()
        elif not self.__useInline: 
            table_headers = table_data[self.__headers]
            table_rows = table_data[self.__rows]
        else:
            table_headers = self.__headers
            table_rows = self.__rows
        
        
        return f"""
.. list-table:: {self.__title}{f'''
   :widths: {self.__widths}''' if self.__widths != None else ''}
   :header-rows: {self.__header_rows}

{self.draw_item(table_headers)[:-1]}
{"".join(list(map(self.draw_item, table_rows)))[:-1]}

"""

    def draw_item(self, row):
        row_str = f"{' '*3}* - {row[0]}\n"

        for index in range(1, len(row)):
            row_str += f"{' '*5}- {row[index]}\n"

        return row_str

        