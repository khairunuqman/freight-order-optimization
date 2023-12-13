from data_model import DataModel
from .variable_builder import VariableBuilder
from ortools.sat.python import cp_model
class ConstraintBuilder:
    def __init__(self,
                 data_model: DataModel,
                 model: cp_model,
                 variable: VariableBuilder) -> None:
        self.data_model = data_model
        self.model = model
        self.variable = variable
        self.one_order_one_freight = []
        self.orders_for_freight = []
        self.order_weights = []
        self.nb_constraint = 0

    def one_order_is_assigned_to_one_frieght(self) -> None:
        for order_id in self.data_model.order:
            order_assignment_vars =\
                [self.variable.freight_order_association.get((freight_id, order_id), None)
                 for freight_id, _ in self.data_model.freight.items()
                 if self.variable.freight_order_association.get((freight_id, order_id), None) is not None]
            self.model.Add(sum(order_assignment_vars) == 1)
            self.nb_constraint += 1

    def one_frieght_is_can_have_many_orders(self) -> None:
        for freight_id in self.data_model.freight:
            freight_assignment_vars =\
                [var for var in 
                    [self.variable.freight_order_association.get((freight_id, order_id), None)
                     for order_id in self.data_model.order]
                 if var is not None]
            self.model.Add(sum(freight_assignment_vars) >= 0)  # Freight can have 0 or more orders
            self.nb_constraint += 1

    def order_may_not_be_assignable_to_freight(self) -> None:
        for order_id in self.data_model.order:
            order_assignment_vars =\
                [self.variable.freight_order_association.get((freight_id, order_id), None)
                 for freight_id, _ in self.data_model.freight.items()
                 if self.variable.freight_order_association.get((freight_id, order_id), None) is not None]
            self.model.Add(sum(order_assignment_vars) <= 1)  # Order can be assigned to at most 1 freight
            self.nb_constraint += 1

    def limit_n_orders_per_freight(self) -> None:
        for freight_id in self.data_model.freight:
            freight_assignment_vars = [self.variable.freight_order_association.get((freight_id, order_id), None)
                                       for order_id in self.data_model.order]
            freight_assignment_vars = [var for var in freight_assignment_vars if var is not None]
            self.model.Add(sum(freight_assignment_vars) <= 30)
            self.nb_constraint += 1

    def remove_none_instances(self, item:list) -> list:
        return [
                var for var in item
                if var is not None
            ]
    def get_number_of_constraint(self):
        return self.nb_constraint
    