from .generic_attribute import GenericAttribute
from.plant_port import PlantPort
class Order(GenericAttribute):
    def __init__(self,
                 order_id: str,
                 origin_port: PlantPort,
                 carrier: str,
                 customer: str,
                 product_id: str,
                 plant_code,
                 destination_port: PlantPort,
                 unit_quantity: float,
                 weight: float) -> None:
        super().__init__(order_id)
        self.origin_port = origin_port
        self.carrier = carrier
        self.customer = customer
        self.product_id = product_id
        self.plant_code = plant_code
        self.destination_port = destination_port
        self.unit_quantity =unit_quantity
        self.weight = weight