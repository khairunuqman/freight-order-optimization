from ortools.sat.python import cp_model
from data_model import DataModel
import pandas as pd

class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, data_model:DataModel, freight_order_association:dict):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.data_model = data_model
        self.freight_order_association = freight_order_association
        self._solution_count = 0
        self._solution_limit = 1
        self.solutions_dict = {}
    
    def on_solution_callback(self):
        self._solution_count += 1
        self.solution_to_dict()
        self.solution_to_csv()
        if self._solution_count >= self._solution_limit:
            print(f"Stop search after {self._solution_limit} solutions")
            self.StopSearch()

    def solution_count(self):
        return self.solution_count
    

    def solution_to_dict(self):
        for key,var in self.freight_order_association.items():
            # print(f'self.Value({var}): {self.Value(var)}')
            if self.Value(var):
                freight, order = key
                self.solutions_dict[key] = {
                    'freight':self.data_model.freight[freight],
                    'order':self.data_model.order[order],
                }


    def solution_to_csv(self):
        df_solution =\
            pd.DataFrame(columns=['freight_id',
                                  'order_id',
                                  'product_id',
                                  'customer',
                                  'carrier',
                                  'origin_port',
                                  'destination_port',
                                  'unit_quantity',
                                  'weight',
                                  'max_weight'
                        ])
        for _,row in self.solutions_dict.items():
            df_solution = df_solution.append(self.add_row(row['freight'],row['order']),ignore_index=True)

        df_solution.to_csv('Solution.csv', index=False)

    def add_row(self,freight,order):
            return [{
                'freight_id': freight.get_id(),
                'order_id': order.get_id(),
                'product_id': order.product_id.get_id(),
                'customer': order.customer,
                'carrier': freight.carrier,
                'origin_port': freight.origin_port.get_id(),
                'destination_port': freight.destination_port.get_id(),
                'unit_quantity':order.unit_quantity,
                'weight':order.weight,
                'max_weight':freight.max_wgh_qty
            }]