import pandas as pd
class DataReader:
    def __init__(self) -> None:
        RELATIVE_PATH = "..\\data\\supply_chain\\"
        self.df_freight_rates =\
            pd.read_csv(f"{RELATIVE_PATH}FreightRates.csv").head(200)
        self.df_order_list =\
            pd.read_csv(f"{RELATIVE_PATH}OrderList.csv").head(1000)
        self.df_plant_ports =\
            pd.read_csv(f"{RELATIVE_PATH}PlantPorts.csv")
        self.df_products_per_plant =\
            pd.read_csv(f"{RELATIVE_PATH}ProductsPerPlant.csv")
        self.df_vmi_customers =\
            pd.read_csv(f"{RELATIVE_PATH}VmiCustomers.csv")
        self.df_wh_capacities =\
            pd.read_csv(f"{RELATIVE_PATH}WhCapacities.csv")
        self.df_wh_costs =\
            pd.read_csv(f"{RELATIVE_PATH}WhCosts.csv")
