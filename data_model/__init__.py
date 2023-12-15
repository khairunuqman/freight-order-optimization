from data_preprocessor import PreProcessor
from .plant_port import PlantPort
from .order import Order
from .product import Product
from .freight import Freight
import time
import math
class DataModel:
    def __init__(self,data: PreProcessor) -> None:
        self.data:PreProcessor = data
        self.port:dict = {}
        self.product:dict = {}
        self.order:dict = {}
        self.freight:dict = {}
        self.initialize_data_model()
        self.UNUSED_FREIGHT_PENALTY = 100_00
        self.UNCOVERED_ORDER = 2

    def initialize_data_model(self) -> None:
        start_time = time.time()
        self.fill_warehouse_port()
        self.fill_product_per_plant()
        self.fill_order()
        self.fill_freight()
        print(f"Data Model Creation Time: {time.time()-start_time} seconds")
        print(f"Freight: {len(self.freight)}")
        print(f"Order: {len(self.order)}")

    def fill_warehouse_port(self):
        for _, row in self.data.df_port_info.iterrows():
            plant_port = PlantPort(
                port_id=row.port,
                plant_code=row.plant_code,
                daily_capacity=row.daily_capacity_,
                cost_unit=row.cost_unit
            )
            self.port[row.port] = plant_port

    def fill_product_per_plant(self):
        for _, row in self.data.df_products_per_plant.iterrows():
            product = Product(
                product_id=row.product_id,
                plant_code=row.plant_code
            )
            self.product[row.product_id] = product
    
    def fill_order(self):
        for _, row in self.data.df_order_list.iterrows():
            order = Order(
                order_id=row.order_id,
                origin_port=self.port[row.origin_port],
                carrier=row.carrier,
                customer=row.customer,
                product_id=self.product[row.product_id],
                plant_code=row.plant_code,
                destination_port=self.port[row.destination_port],
                unit_quantity=row.unit_quantity,
                weight=math.ceil(row.weight)
            )
            self.order[row.order_id] = order

    def fill_freight(self):
        for idx, row in self.data.df_freight_rates.iterrows():
            if row.max_wgh_qty > 2000:
                continue
            freight_id = f"{idx}_{row.carrier}_{row.orig_port_cd}_{row.dest_port_cd}"
            freight = Freight(
                freight_id=freight_id,
                carrier=row.carrier,
                orig_port_cd=self.port[row.orig_port_cd],
                dest_port_cd=self.port[row.dest_port_cd],
                minm_wgh_qty=row.minm_wgh_qty,
                max_wgh_qty=math.ceil(row.max_wgh_qty),
                minimum_cost=row.minimum_cost
            )
            self.freight[freight_id] = freight

