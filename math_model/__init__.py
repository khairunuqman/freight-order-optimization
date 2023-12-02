from data_model import DataModel
from .variable_builder import VariableBuilder
from .constraint_builder import ConstraintBuilder
from .objective_builder import ObjectiveBuilder
from ortools.sat.python import cp_model
import time
class MathModel:
    def __init__(self,
                 data_model: DataModel,
                 model:cp_model) -> None:
        self.model:cp_model = model
        self.variable = VariableBuilder(data_model,self.model)
        # self.constraint = ConstraintBuilder(data_model)
        # self.objective = ObjectiveBuilder(data_model)

    def create_variable_instances(self) -> None:
        start_time = time.time()
        self.variable.add_freight_order_association()
        print(f"Variable Creation Time: {time.time()-start_time} seconds")