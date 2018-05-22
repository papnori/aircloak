from ortools.linear_solver import pywraplp

def main():

    data = [
        ['qegy', 0, 1, 0, 1, 0],
        ['qketto', 1, 1, 1, 1, 0],
        ['qharom', 1, 1, 1, 1, 1],
        ['qnegy', 0, 0, 0, 0, 0],
        ['qot', 0, 0, 1, 0, 1]
    ];
    nutrients = [
        ['egy', 2],
        ['ketto', 2],
        ['harom', 2],
        ['negy', 0],
        ['ot', 0]
    ]
    # Instantiate a Glop solver, naming it SolveStigler.
    solver = pywraplp.Solver('SolveStigler',pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
    # Declare an array to hold our nutritional data.
    food = [[]] * len(data)

    # Objective:
    objective = solver.Objective()
    for i in range(0, len(data)):
        food[i] = solver.NumVar(0.0, 1.0, data[i][0])
        objective.SetCoefficient(food[i], 1)
    objective.SetMinimization()

    epsilon = 0       #torzitas merteke
    # Create the constraints, one per nutrient.
    constraints = [0] * len(nutrients)
    for i in range(0, len(nutrients)):
        constraints[i] = solver.Constraint(nutrients[i][1] - epsilon, nutrients[i][1] + epsilon)
        for j in range(0, len(data)):
            constraints[i].SetCoefficient(food[j], data[j][i+1])
    # Solve!
    status = solver.Solve()

    if status == solver.OPTIMAL:
        num_nutrients = len(data[i]) - 1
        nutrients = [0] * (len(data[i]) - 1)
        for i in range(0, len(data)):
            print(food[i].solution_value())

            for nutrient in range(0, num_nutrients):
                nutrients[nutrient] = food[i].solution_value()
        print('Number of variables =', solver.NumVariables())
        print('Number of constraints =', solver.NumConstraints())

    else:  # No optimal solution was found.
        if status == solver.FEASIBLE:
            print ('A potentially suboptimal solution was found.')
        else:
            print ('The solver could not solve the problem.')

if __name__ == '__main__':
    main()