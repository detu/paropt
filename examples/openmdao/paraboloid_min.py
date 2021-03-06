from openmdao.api import Problem, ScipyOptimizeDriver, ExecComp, IndepVarComp
from paropt.paropt_driver import ParOptDriver
import argparse

# Create an argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--algorithm', default='ip',
                    choices=['ip', 'tr', 'mma'],
                    help='optimizer type')
args = parser.parse_args()

# Build the model
prob = Problem()

# Define the independent variables
indeps = prob.model.add_subsystem('indeps', IndepVarComp())
indeps.add_output('x', 3.0)
indeps.add_output('y', -4.0)

# Define the objective and the constraint functions
prob.model.add_subsystem('paraboloid', ExecComp('f = (x-3)**2 + x*y + (y+4)**2 - 3'))
prob.model.add_subsystem('con', ExecComp('c = x + y'))

# Connect the model
prob.model.connect('indeps.x', 'paraboloid.x')
prob.model.connect('indeps.y', 'paraboloid.y')
prob.model.connect('indeps.x', 'con.x')
prob.model.connect('indeps.y', 'con.y')

# Define the optimization problem
prob.model.add_design_var('indeps.x', lower=-50, upper=50)
prob.model.add_design_var('indeps.y', lower=-50, upper=50)
prob.model.add_objective('paraboloid.f')
prob.model.add_constraint('con.c', lower=0.0)

# Create the ParOpt driver
prob.driver = ParOptDriver()

# Set options for the driver
prob.driver.options['algorithm'] = args.algorithm

# Run the problem
prob.setup()
prob.run_driver()

# Print the minimum value
print("Minimum value = {fmin:.2f}".format(fmin=prob['paraboloid.f'][0]))

# Print the x/y location of the minimum
print("(x, y) = ({x:.2f}, {y:.2f})".format(x=prob['indeps.x'][0], y=prob['indeps.y'][0]))
