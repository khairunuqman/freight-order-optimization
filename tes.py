from ortools.sat.python import cp_model

class FreightAssignmentModel:
    def __init__(self, num_orders, num_freights):
        self.model = cp_model.CpModel()
        self.vars = {}
        self.num_orders = num_orders
        self.num_freights = num_freights

        # Create binary decision variables
        for order in range(num_orders):
            for freight in range(num_freights):
                self.vars[(order, freight)] = self.model.NewBoolVar(f'Order_{order}_Freight_{freight}')

        # Each order is assigned to at most one freight
        for order in range(num_orders):
            self.model.Add(sum(self.vars[(order, freight)] for freight in range(num_freights)) <= 1)

        # Each freight can have multiple orders
        for freight in range(num_freights):
            self.model.Add(sum(self.vars[(order, freight)] for order in range(num_orders)) >= 0)

        for freight in range(num_freights):
            self.model.Add(sum(self.vars[(order, freight)] for order in range(num_orders)) <= 3)

        # Define the objective function (maximize the number of orders assigned)
        # self.model.Maximize(
        #     sum(self.vars[(order, freight)] for order in range(num_orders)
        #         for freight in range(num_freights)))
        self.model.Maximize(
            sum(
                sum(self.vars[(order, freight)] for order in range(num_orders)) 
                for freight in range(num_freights)
            )
        )

    def solve(self):
        solver = cp_model.CpSolver()
        status = solver.Solve(self.model)

        if status == cp_model.OPTIMAL:
            solution = []
            for order in range(self.num_orders):
                for freight in range(self.num_freights):
                    if solver.Value(self.vars[(order, freight)]) == 1:
                        solution.append((f'Order {order}', f'Freight {freight}'))
            return solution
        else:
            print(f'Solver status: {solver.StatusName(status)}')
            print(f'Objective value: {solver.ObjectiveValue()}')
            for order in range(self.num_orders):
                for freight in range(self.num_freights):
                    print(f'Var[{order},{freight}] = {solver.Value(self.vars[(order, freight)])}')
            return None


# Example usage:
if __name__ == "__main__":
    num_orders = 5
    num_freights = 3

    model = FreightAssignmentModel(num_orders, num_freights)
    result = model.solve()

    if result:
        for order, freight in result:
            print(f"{order} assigned to {freight}")
    else:
        print("No solution found.")