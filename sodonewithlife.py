from __future__ import print_function
from ortools.linear_solver import pywraplp
import tables
import numpy as np
import random
import string

def main():
    fileName = 'smallconcept.h5'
    fileNamer = 'smallconceptresult.h5'
    fileNamee = 'smallconcept.h5'
    #fileName = 'smallconceptwithgauss.h5'
    #fileNamer = 'smallconceptwithgaussresult.h5'
    h5f = tables.open_file(fileName)
    h5fr = tables.open_file(fileNamer)
    h5fe = tables.open_file(fileNamee)

    data = np.array(h5f.root.carray)
    print(data)
    results = np.array(h5fr.root.carray)
    print(results)
    excepted = np.array(h5fe.root.carray)
    print(excepted)

    # Glop solver inicializalas.
    solver = pywraplp.Solver('LinearExample', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

    people = [[]] * 100

    # Objective function
    objective = solver.Objective()
    for i in range(0, len(people)):
        people[i] = solver.NumVar(0.0, 1.0, ''.join([random.choice(string.ascii_letters) for n in range(6)]))
        objective.SetCoefficient(people[i], 1)
    objective.SetMinimization()

    epsilon = 0
    constraints = [0] * len(results)

    for i in range(0, len(results)):
        constraints[i] = solver.Constraint(int(results[i][1] - epsilon), int(results[i][1] + epsilon))
        for j in range(0, len(people)):
            constraints[i].SetCoefficient(people[j], int(data[i][j + 1]))

    # Solve!
    status = solver.Solve()

    if status == solver.OPTIMAL:
        print('SOLUTION:')
        for i in range(0, len(people)):
            print(people[i].solution_value())

        print('Number of variables =', solver.NumVariables())
        print('Number of constraints =', solver.NumConstraints())

    else:  # No optimal solution was found.
        if status == solver.FEASIBLE:
            print('A potentially suboptimal solution was found.')
        else:
            print('The solver could not solve the problem.')

    h5f.close()
    h5fr.close()

if __name__ == '__main__':
  main()