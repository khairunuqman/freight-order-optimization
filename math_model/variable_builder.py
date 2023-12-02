from data_model import DataModel
from ortools.sat.python import cp_model
class VariableBuilder:
    def __init__(self,
                 data_model:DataModel,
                 model:cp_model) -> None:
        self.data_model:DataModel = data_model
        self.model:cp_model = model
        self.freight_order_association:dict = {}

    def add_freight_order_association(self) -> None:
        self.freight_order_association.update({
            (freight_id, order_id): self.model.NewBoolVar(f"freight_{freight_id}_order_{order_id}")
            for freight_id, freight in self.data_model.freight.items()
            for order_id, order in self.data_model.order.items()
            if freight.origin_port.get_id() == order.origin_port.get_id()
            and freight.destination_port.get_id() == order.destination_port.get_id()
        })