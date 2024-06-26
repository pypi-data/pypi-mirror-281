import os
import plotly
import uuid
import tempfile
import plotly.express as px
import plotly.graph_objects as go

from mldev.experiment_tag import experiment_tag
from enum import StrEnum


class Graphic_Types(StrEnum):
    LINE = "line"
    BAR = "bar"
    HISTOGRAM_2D = "histogram_2d"
    SCATTER="scatter"


def draw_line(fig, dataset):
    fig.add_trace(go.Scatter(**dataset))


def draw_bar(fig, dataset):
    fig.add_trace(go.Bar(**dataset))


def draw_2d_histogram(fig, dataset):
    fig.add_trace(go.Histogram2d(**dataset))
 

def draw_scatter(fig, dataset):
    fig.add_trace(go.Scatter(**dataset))


draw_functions = {
    Graphic_Types.LINE: draw_line,
    Graphic_Types.BAR: draw_bar,
    Graphic_Types.HISTOGRAM_2D: draw_2d_histogram,
    Graphic_Types.SCATTER: draw_scatter
}


@experiment_tag()
class Graphic:
    """
    Graphic tag
    """
    def __init__(self, datasets, config={}):
        if datasets == None or len(datasets) == 0:
            raise Exception("Exeption: graphic must have at least one dataset.")

        self.__datasets = datasets
        self.__config = config
    
  
    @property
    def rst(self):
        tmp_graphic_file = os.path.join(tempfile.mkdtemp(), str(uuid.uuid4()) + ".html")
        fig = go.Figure()
        fig.update_layout(margin_b=0, margin_l=0, margin_r=0, margin_t=0)
        for dataset in self.__datasets:
            graphic_type = dataset["graphic_type"]
            data =  dataset["dataset"].data if  dataset["dataset"] != None else None

            dataset["y"] = sum(data[[dataset["y"]]].values.tolist(), [])
            dataset["x"] = sum(data[[dataset["x"]]].values.tolist(), [])

            del dataset["graphic_type"]
            del dataset["dataset"]

            draw_functions[graphic_type](fig, dataset)
        fig.update_layout(self.__config)
        plotly.offline.plot(fig, filename=tmp_graphic_file)

        return f"""
.. raw:: html
   :file: {tmp_graphic_file}
"""