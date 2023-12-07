import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

angle = ctrl.Antecedent(np.arange(-90, 91, 1), 'angle')
angular_velocity = ctrl.Antecedent(np.arange(-10, 11, 1), 'angular_velocity')

output = ctrl.Consequent(np.arange(-1, 2, 1), 'output') 

angle['left'] = fuzz.trimf(angle.universe, [-90, -90, 0])
angle['vertical'] = fuzz.trimf(angle.universe, [-45, 0, 45])
angle['right'] = fuzz.trimf(angle.universe, [0, 90, 90])

angular_velocity['left'] = fuzz.trimf(angular_velocity.universe, [-10, -10, 0])
angular_velocity['zero'] = fuzz.trimf(angular_velocity.universe, [-5, 0, 5])
angular_velocity['right'] = fuzz.trimf(angular_velocity.universe, [0, 10, 10])

output['negative'] = fuzz.trimf(output.universe, [-1, -1, 0])
output['zero'] = fuzz.trimf(output.universe, [-1, 0, 1])
output['positive'] = fuzz.trimf(output.universe, [0, 1, 1])

rule1 = ctrl.Rule(angle['left'] & angular_velocity['left'], output['negative'])
rule2 = ctrl.Rule(angle['vertical'] & angular_velocity['zero'], output['zero'])
rule3 = ctrl.Rule(angle['right'] & angular_velocity['right'], output['positive'])


system = ctrl.ControlSystem([rule1, rule2, rule3])
fis = ctrl.ControlSystemSimulation(system)


fis.input['angle'] = -30
fis.input['angular_velocity'] = -5


fis.compute()

print(f"Sistema Fis : {fis.output['output']}")
