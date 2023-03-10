from ortools.linear_solver import pywraplp
# Set up the linear programming solver
solver = pywraplp.Solver.CreateSolver('SCIP')
# Set up the decision variables
bs = solver.IntVar(1, 5000, 'bs')
bd = solver.IntVar(bs.solution_value(), 5000, 'bd')

# Set up the constraints
solver.Add(bs * solver.Div(5000, bs * 10) <= 10)
solver.Add(bd * solver.Div(5000, bd * 10) <= 10)
solver.Add(bd >= bs)

# Set up the objective function
ts = 50
td = 89
obj = (5000/float(bs.solution_value()))*ts+((5000/float(bd.solution_value()))-(5000/float(bs.solution_value())))*td
solver.Minimize(obj)


# Solve the optimization problem
status = solver.Solve()

# Print the optimal batch sizes and total time
if status == pywraplp.Solver.OPTIMAL:
    print('Optimal batch size for Sourcing:', int(b1.solution_value()))
    print('Optimal batch size for OCR:', int(b2.solution_value()))
    print('Total time:', solver.Objective().Value())
else:
    print('The problem does not have an optimal solution.')
