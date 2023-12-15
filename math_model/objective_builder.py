from data_model import DataModel
from .variable_builder import VariableBuilder
from ortools.sat.python import cp_model
class ObjectiveBuilder:
    def __init__(self, data_model: DataModel, model: cp_model, variable: VariableBuilder) -> None:
        self.data_model = data_model
        self.model = model
        self.variable = variable
        self.value_coefficient = 0

    def get_value_coefficient(self) -> float:
        return self.value_coefficient

    def construct_objective_coefficient(self) -> None:
        self.penalty_unassigned_freight()
        self.penalty_uncovered_order()

    def penalty_unassigned_freight(self) -> None:
        for freight_id in self.data_model.freight:
            freight_assignment_vars =\
                [self.variable.freight_order_association.get((freight_id, order_id), None)
                 for order_id in self.data_model.order
                 if self.variable.freight_order_association.get((freight_id, order_id), None) is not None]
            self.value_coefficient += self.data_model.UNUSED_FREIGHT_PENALTY * (1 - sum(freight_assignment_vars))

    def penalty_uncovered_order(self) -> None:
        for order_id in self.data_model.order:
            order_assignment_vars =\
                [self.variable.freight_order_association.get((freight_id, order_id), None)
                 for freight_id, _ in self.data_model.freight.items()
                 if self.variable.freight_order_association.get((freight_id, order_id), None) is not None]
            self.value_coefficient += self.data_model.UNCOVERED_ORDER * (1 - sum(order_assignment_vars))