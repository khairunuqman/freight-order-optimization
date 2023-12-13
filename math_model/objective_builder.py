from data_model import DataModel
from .variable_builder import VariableBuilder
from ortools.sat.python import cp_model
class ObjectiveBuilder:
    def __init__(self,
                 data_model: DataModel,
                 model: cp_model,
                 variable: VariableBuilder) -> None:
        pass