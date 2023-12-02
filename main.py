from data_model import DataModel
from data_preprocessor import PreProcessor
from math_model import MathModel
from ortools.sat.python import cp_model

pre_processor = PreProcessor()
data_model = DataModel(data=pre_processor)
model = cp_model.CpModel()
math_model = MathModel(data_model=data_model, model=model)
math_model.create_variable_instances()
pass