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

    def penalty_cost_order(self) -> None:
        for var_id in self.variable.freight_order_association:
            freight_id, order_id = var_id
            self.data_model.freight[freight_id]
            cost_per_unit = self.data_model.order[order_id].destination_port.cost_unit
            unit_quantity = self.data_model.order[order_id].unit_quantity
            ORDER_COST = cost_per_unit*unit_quantity
            self.value_coefficient += ORDER_COST * (1 - self.variable.freight_order_association[var_id])
        pass