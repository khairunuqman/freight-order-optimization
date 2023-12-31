import pandas as pd
import re
from .data_reader import DataReader
class PreProcessor(DataReader):
    def __init__(self) -> None:
        super().__init__()
        self.df_port_info = pd.DataFrame()
        self.input_schema()
        self.input_integrity()
        self.output_transformation()

    def input_schema(self):
        self.df_plant_ports.columns =\
            self.dataframe_col_rename_std(self.df_plant_ports) # used
        self.df_freight_rates.columns =\
            self.dataframe_col_rename_std(self.df_freight_rates) # used
        self.df_order_list.columns =\
            self.dataframe_col_rename_std(self.df_order_list) # used
        self.df_products_per_plant.columns =\
            self.dataframe_col_rename_std(self.df_products_per_plant) # used
        self.df_vmi_customers.columns =\
            self.dataframe_col_rename_std(self.df_vmi_customers)
        self.df_wh_capacities.columns =\
            self.dataframe_col_rename_std(self.df_wh_capacities) # used
        self.df_wh_costs.columns =\
            self.dataframe_col_rename_std(self.df_wh_costs) # used

    def input_integrity(self):
        self.integrity_freight()

    def output_transformation(self):
        self.transform_port_info()
        self.transform_freight()

    def transform_port_info(self):
        self.df_port_info = self.df_plant_ports
        self.df_port_info = pd.merge( self.df_port_info,
                                     self.df_wh_capacities,
                                     left_on='plant_code',
                                     right_on='plant_id',
                                     how='left')
        self.df_port_info.drop(columns=['plant_id'], inplace=True)
        self.df_port_info = pd.merge( self.df_port_info,
                                     self.df_wh_costs,
                                     left_on='plant_code',
                                     right_on='wh',
                                     how='left')
        self.df_port_info.drop(columns=['wh'], inplace=True)

    def transform_freight(self):
        self.df_freight_rates.max_wgh_qty =\
            self.df_freight_rates.max_wgh_qty.str.replace(',', '').astype(float)
        self.df_freight_rates.minimum_cost =\
            self.df_freight_rates.minimum_cost.apply(lambda x: x.replace('$', '').strip())
    
    def integrity_freight(self):
        ORIGIN_PORT = list(set(self.df_order_list.origin_port.to_list()))
        DESTINATION_PORT = list(set(self.df_order_list.destination_port.to_list()))
        cond_freight_origin = self.df_freight_rates.orig_port_cd.isin(ORIGIN_PORT)
        cond_freight_destination = self.df_freight_rates.dest_port_cd.isin(DESTINATION_PORT)
        self.df_freight_rates = self.df_freight_rates[cond_freight_origin & cond_freight_destination]

    def dataframe_col_rename_std(self,df) -> pd.DataFrame:
        return [re.sub('[^a-zA-Z0-9_]', '_', col.lower().replace(' ', '_')) for col in df.columns]