from .generic_attribute import GenericAttribute
class Product(GenericAttribute):
    def __init__(self,
                 product_id: str,
                 plant_code: str) -> None:
        super().__init__(product_id)
        self.plant_code = plant_code