from data_model import DataModel
from math_model import MathModel,VariableBuilder
from ortools.sat.python import cp_model
class Optimizer:
    def __init__(self,
                 data_model: DataModel,
                 model:cp_model,
                 math_model:MathModel) -> None:
        self.data_model = data_model
        self.model = model
        self.variable:VariableBuilder = math_model.variable
        self.solver = cp_model.CpSolver()
        self.set_solver_parameter()
        # self.solution_printer = SolutionPrinter(self.data_model, self.var_aircraft_to_rotation)

    def set_solver_parameter(self):
        self.solver.parameters.linearization_level = 0
        self.solver.parameters.enumerate_all_solutions = False

    def solve(self):
        # self.solver.Solve(self.model, self.solution_printer)
        self.solver.Solve(self.model)
        print("\nStatistics")
        print(f"  - conflicts: {self.solver.NumConflicts()}")
        print(f"  - branches : {self.solver.NumBranches()}")
        print(f"  - wall time: {self.solver.WallTime()}s")
        pass
        # print(f"  - Nb of Solution: {self.solution_printer._solution_count}")