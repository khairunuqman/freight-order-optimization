from data_model import DataModel
from math_model import MathModel,VariableBuilder,ObjectiveBuilder
from ortools.sat.python import cp_model
from .solution_printer import SolutionPrinter
class Optimizer:
    def __init__(self,
                 data_model: DataModel,
                 model:cp_model,
                 math_model:MathModel) -> None:
        self.data_model = data_model
        self.model = model
        self.variable:VariableBuilder = math_model.variable
        self.objective:ObjectiveBuilder = math_model.objective
        self.solver = cp_model.CpSolver()
        self.set_solver_parameter()
        self.solution_printer = SolutionPrinter(self.data_model, self.variable.freight_order_association)

    def set_solver_parameter(self):
        self.solver.parameters.linearization_level = 0
        self.solver.parameters.enumerate_all_solutions = True
        self.model.Minimize(self.objective.get_value_coefficient())

    def solve(self):
        self.solver.Solve(self.model, self.solution_printer)
        print("\nStatistics")
        print(f"  - conflicts: {self.solver.NumConflicts()}")
        print(f"  - branches : {self.solver.NumBranches()}")
        print(f"  - wall time: {self.solver.WallTime()}s")
        print(f"  - objective value: {self.solver.ObjectiveValue()}")
        print(f"  - nb of solution: {self.solution_printer._solution_count}")