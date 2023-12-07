import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# PARTE 1:
angulo = ctrl.Antecedent(np.arange(-180, 181, 1), 'angulo')
vel_angular = ctrl.Antecedent(np.arange(-10, 11, 1), 'vel_angular')

# PARTE 2 :
posicao = ctrl.Antecedent(np.arange(-10, 11, 1), 'posicao')
vel_linear = ctrl.Antecedent(np.arange(-10, 11, 1), 'vel_linear')

acao = ctrl.Consequent(np.arange(-10, 11, 1), 'acao')

# angulo
angulo['N'] = fuzz.trimf(angulo.universe, [-180, -180, 0])
angulo['Z'] = fuzz.trimf(angulo.universe, [-15, 0, 15])
angulo['P'] = fuzz.trimf(angulo.universe, [0, 180, 180])

# velocidade angular 
vel_angular['N'] = fuzz.trimf(vel_angular.universe, [-10, -10, 0])
vel_angular['Z'] = fuzz.trimf(vel_angular.universe, [-2, 0, 2])
vel_angular['P'] = fuzz.trimf(vel_angular.universe, [0, 10, 10])

# posição
posicao['N'] = fuzz.trimf(posicao.universe, [-10, -10, 0])
posicao['Z'] = fuzz.trimf(posicao.universe, [-2, 0, 2])
posicao['P'] = fuzz.trimf(posicao.universe, [0, 10, 10])

# velocidade 
vel_linear['N'] = fuzz.trimf(vel_linear.universe, [-10, -10, 0])
vel_linear['Z'] = fuzz.trimf(vel_linear.universe, [-2, 0, 2])
vel_linear['P'] = fuzz.trimf(vel_linear.universe, [0, 10, 10])

acao['N'] = fuzz.trimf(acao.universe, [-10, -10, 0])
acao['Z'] = fuzz.trimf(acao.universe, [-2, 0, 2])
acao['P'] = fuzz.trimf(acao.universe, [0, 10, 10])

# regras !
regra_1 = ctrl.Rule(antecedent=(angulo['N'] & vel_angular['N'] & posicao['N'] & vel_linear['N']), consequent=acao['P'])
                   
regra_2 = ctrl.Rule(antecedent=(angulo['N'] & vel_angular['Z'] & posicao['N'] & vel_linear['Z']), consequent=acao['N'])
                   
regra_3 = ctrl.Rule(antecedent=(angulo['N'] & vel_angular['P'] & posicao['N'] & vel_linear['P']), consequent=acao['Z'])
                   
regra_4 = ctrl.Rule(antecedent=(posicao['N'] & vel_linear['N']), consequent=acao['P'])
                   
regra_5 = ctrl.Rule(antecedent=(posicao['Z'] & vel_linear['Z']), consequent=acao['Z'])
                   
regra_6 = ctrl.Rule(antecedent=(posicao['Z'] & vel_linear['P']), consequent=acao['N'])
                   
regra_7 = ctrl.Rule(antecedent=(posicao['P'] & vel_linear['N']), consequent=acao['N'])

regra_8 = ctrl.Rule(antecedent=(posicao['P'] & vel_linear['Z']), consequent=acao['P'])

regra_9 = ctrl.Rule(antecedent=(posicao['P'] & vel_linear['P']), consequent=acao['P'])

sis_controle = ctrl.ControlSystem([regra_1, regra_2, regra_3, regra_4, regra_5, regra_6, regra_7, regra_8, regra_9])

simulador = ctrl.ControlSystemSimulation(sis_controle)

simulador.input['angulo'] = -45
simulador.input['vel_angular'] = 5
simulador.input['posicao'] = -5
simulador.input['vel_linear'] = -3

simulador.compute()

print(simulador.output['acao'])
acao.view(sim=simulador)

import matplotlib.pyplot as plt

plt.show()
