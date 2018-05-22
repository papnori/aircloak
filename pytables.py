from ortools.linear_solver import pywraplp
import tables
import numpy as np
import random
import string

def main():

  fileName = 'smallconceptwithgauss.h5'
  fileNamer = 'smallconceptwithgaussresult.h5'
  h5f = tables.open_file(fileName)
  h5fr = tables.open_file(fileNamer)

  data = np.array(h5f.root.carray)
  print(data)

  nutrients = np.array(h5fr.root.carray)
  print(nutrients)

  # Instantiate a Glop solver, naming it SolveStigler.
  solver = pywraplp.Solver('SolveStigler',pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
  # Declare an array to hold our nutritional data.
  #food = [[]] * len(data)
  food = [[]] * 100

  # Objective:
  objective = solver.Objective()
  for i in range(0, 100):
    #print(str(data[i][0]))
    food[i] = solver.NumVar(0.0, 1.0, str(data[i][0]).join([random.choice(string.ascii_letters) for n in range(9)]))
    objective.SetCoefficient(food[i], 1)
  objective.SetMaximization()

  epsilon = 10       #torzitas merteke
  # Create the constraints, one per nutrient.
  constraints = [0] * len(nutrients)

  #print(data[500][100])
  for i in range(0, 100):
  #for i in range(0, len(nutrients)):
    constraints[i] = solver.Constraint(int(nutrients[i][1] - epsilon), int(nutrients[i][1] + epsilon))
    #print(i)
    for j in range(0, 100):
    #for j in range(0, len(data)):
      #print(food[j])

      constraints[i].SetCoefficient(food[j], int(data[j][i+1]))
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

  h5f.close()

if __name__ == '__main__':
  main()

