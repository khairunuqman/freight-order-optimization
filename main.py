from data_model import DataModel
from data_preprocessor import PreProcessor
from math_model import MathModel
from optimizer import Optimizer
from ortools.sat.python import cp_model

# PreProcessing
pre_processor = PreProcessor()
data_model = DataModel(data=pre_processor)
model = cp_model.CpModel()

# Math Model
math_model = MathModel(data_model=data_model, model=model)
math_model.create_variable_instances()
math_model.create_constraints()
math_model.create_objective_coefficient()
math_model.display_num_var_ctr()

# Solving
optimizer = Optimizer(data_model,model,math_model)
optimizer.solve()
pass