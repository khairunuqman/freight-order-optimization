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

    def order_at_most_one_freight(self) -> None:
        for order_id in self.data_model.order:
            order_assignment_vars =\
                [self.variable.freight_order_association.get((freight_id, order_id), None)
                 for freight_id, _ in self.data_model.freight.items()
                 if self.variable.freight_order_association.get((freight_id, order_id), None) is not None]
            if order_assignment_vars:
                self.model.Add(sum(order_assignment_vars) <= 1)  # Order can be assigned to at most 1 freight
                self.nb_constraint += 1
    
    def freight_max_weight(self) -> None:
        for freight_id in self.data_model.freight:
            freight_assignment_vars =\
                [self.variable.freight_order_association.get((freight_id, order_id), None)
                 for order_id in self.data_model.order
                 if self.variable.freight_order_association.get((freight_id, order_id), None) is not None]
            weights =\
                [order.weight
                 for order_id, order in self.data_model.order.items()
                 if (freight_id, order_id) in self.variable.freight_order_association]
            if freight_assignment_vars:
                self.model.Add(
                    sum(freight_assignment_vars[i] * weights[i]
                        for i in range(len(weights)))<= self.data_model.freight[freight_id].max_wgh_qty)
                self.nb_constraint += 1

    def warehouse_max_capacity(self) -> None:
        for port_id in self.data_model.port:
            order_assignment_vars =\
                [self.variable.freight_order_association.get((freight_id, order_id), None)
                 for freight_id, _ in self.data_model.freight.items()
                 for order_id in self.data_model.order
                 if self.data_model.freight[freight_id].destination_port.id == port_id
                 if self.variable.freight_order_association.get((freight_id, order_id), None) is not None]
            if order_assignment_vars:
                self.model.Add(sum(order_assignment_vars) <= self.data_model.port[port_id].daily_capacity)
                self.nb_constraint += 1

    def remove_none_instances(self, item:list) -> list:
        return [
                var for var in item
                if var is not None
            ]
    def get_number_of_constraint(self):
        return self.nb_constraint
    