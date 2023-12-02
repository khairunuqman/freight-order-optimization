from .generic_attribute import GenericAttribute
from.plant_port import PlantPort
class Freight(GenericAttribute):
    def __init__(self,
                 freight_id: str,
                 carrier: str,
                 orig_port_cd: PlantPort,
                 dest_port_cd: PlantPort,
                 minm_wgh_qty: float,
                 max_wgh_qty: float,
                 minimum_cost: float) -> None:
        super().__init__(freight_id)
        self.carrier = carrier
        self.origin_port = orig_port_cd
        self.destination_port = dest_port_cd
        self.min_wgh_qty = minm_wgh_qty
        self.max_wgh_qty = max_wgh_qty
        self.base_cost = minimum_cost