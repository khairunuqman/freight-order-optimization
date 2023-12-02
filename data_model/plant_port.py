from .generic_attribute import GenericAttribute
class PlantPort(GenericAttribute):
    def __init__(self,
                 port_id: str,
                 plant_code: str,
                 daily_capacity: float,
                 cost_unit: float) -> None:
        super().__init__(port_id)
        self.plant_code = plant_code
        self.daily_capacity = daily_capacity
        self.cost_unit = cost_unit
