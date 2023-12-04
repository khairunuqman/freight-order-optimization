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

    def one_order_max_one_freight(self) -> None:
        for _, order in self.data_model.order.items():
            one_order_one_freight = [
                self.variable.freight_order_association.get((freight.get_id(), order.get_id()), None)
                for _, freight in self.data_model.freight.items()
            ]
            one_order_one_freight = self.remove_none_instances(one_order_one_freight)
            if one_order_one_freight:
                self.one_order_one_freight.extend(one_order_one_freight)
                self.model.AddAtMostOne(one_order_one_freight)

    def ub_orders_per_freight(self) -> None:
        for _, freight in self.data_model.freight.items():
            orders_for_freight = [
                self.variable.freight_order_association.get((freight.get_id(), order.get_id()), None)
                for _, order in self.data_model.order.items()
            ]
            orders_for_freight = self.remove_none_instances(orders_for_freight)
            if orders_for_freight:
                self.orders_for_freight.extend(orders_for_freight)
                # self.model.Maximize(sum(orders_for_freight))
                self.model.Add(sum(orders_for_freight) <= 20)
                
    def maximize_freight_assignment_of_order(self) -> None:
        order_ids = {order.get_id() for _, order in self.data_model.order.items()}
        for _, freight in self.data_model.freight.items():
            orders_for_freight = [
                self.variable.freight_order_association.get((freight.get_id(), order.get_id()), None)
                for _, order in self.data_model.order.items()
            ]
            orders_for_freight = self.remove_none_instances(orders_for_freight)
            if orders_for_freight:
                
                print('it goes here')
                self.model.Maximize(
                    sum(
                        sum(orders_for_freight)
                        for order_id in order_ids
                        # if self.variable.freight_order_association.get((freight.get_id(), order.get_id()), None) is not None
                        if (freight.get_id(), order_id) in self.variable.freight_order_association
                        )
                )
    
    def remove_none_instances(self, item:list) -> list:
        return [
                var for var in item
                if var is not None
            ]
    def get_number_of_constraint(self):
        return len(self.one_order_one_freight)\
            + len(self.orders_for_freight)\
            + len(self.order_weights)
    



    # def max_weight_constraint(self) -> None:
    #     for _, freight in self.data_model.freight.items():
    #         # Use a set for faster membership tests
    #         orders_for_freight_set = {
    #             order.get_id()
    #             for _, order in self.data_model.order.items()
    #             if (association := self.variable.freight_order_association.get((freight.get_id(), order.get_id()), None)) is not None
    #         }           
    #         orders_for_freight_set.discard(None)

    #         if len(orders_for_freight_set) > 0:
    #             # # Precompute a dictionary to map order IDs to weights
    #             # order_weights_dict = {order.get_id(): order.weight for order in self.data_model.order.values()}

    #             # # Calculate the total weight for the freight
    #             # total_weight = sum(order_weights_dict.get(order_id, 0) for order_id in orders_for_freight_set)

    #             # # Add constraint: total order weight <= max weight of freight
    #             # self.model.Add(total_weight <= freight.max_wgh_qty)

    #             # Create binary variables for each order
    #             order_selected_vars = {
    #                 order.get_id(): self.model.NewBoolVar(f"order_{order.get_id()}_{freight.get_id()}")
    #                 for _, order in self.data_model.order.items()
    #                 if order.get_id() in orders_for_freight_set
    #             }

    #             # Convert weights to integers (adjust the multiplier as needed)
    #             weights_int = {
    #                 order_id: int(order.weight * 100)
    #                 for order_id, order in self.data_model.order.items()
    #             }

    #             # Add constraint: total order weight <= max weight of freight
    #             self.model.Add(
    #                 sum(
    #                     order_selected_vars[order_id] * weights_int[order_id]
    #                     for order_id in orders_for_freight_set
    #                 ) <= int(freight.max_wgh_qty * 100)
    #             )
    