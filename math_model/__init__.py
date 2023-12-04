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
        self.constraint = ConstraintBuilder(data_model,self.model,self.variable)
        # self.objective = ObjectiveBuilder(data_model)

    def create_variable_instances(self) -> None:
        start_time = time.time()
        self.variable.add_freight_order_association()
        print(f"Variable Creation Time: {time.time()-start_time} seconds")

    def create_constraints(self) -> None:
        start_time = time.time()
        self.constraint.one_order_max_one_freight()
        self.constraint.ub_orders_per_freight()
        self.constraint.maximize_freight_assignment_of_order()
        print(f"Constraint Creation Time: {time.time()-start_time} seconds")
    
    def display_num_var_ctr(self):
        print(f"Variables Created: {self.variable.get_number_of_variable()}")
        print(f"Constraints Created: {self.constraint.get_number_of_constraint()}")