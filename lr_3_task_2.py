import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

room_temperature = ctrl.Antecedent(np.arange(0, 41, 1), 'room_temperature')
temp_change_rate = ctrl.Antecedent(np.arange(-5, 6, 1), 'temp_change_rate')

ac_regulator = ctrl.Consequent(np.arange(-90, 91, 1), 'ac_regulator')

room_temperature['very_cold'] = fuzz.trapmf(room_temperature.universe, [0, 0, 5, 10])
room_temperature['cold'] = fuzz.trimf(room_temperature.universe, [5, 10, 20])
room_temperature['normal'] = fuzz.trimf(room_temperature.universe, [15, 20, 25])
room_temperature['warm'] = fuzz.trimf(room_temperature.universe, [20, 25, 30])
room_temperature['very_warm'] = fuzz.trapmf(room_temperature.universe, [30, 35, 40, 40])

temp_change_rate['negative'] = fuzz.trapmf(temp_change_rate.universe, [-5, -5, -2, 0])
temp_change_rate['zero'] = fuzz.trimf(temp_change_rate.universe, [-1, 0, 1])
temp_change_rate['positive'] = fuzz.trapmf(temp_change_rate.universe, [0, 2, 5, 5])

ac_regulator['large_left'] = fuzz.trapmf(ac_regulator.universe, [-90, -90, -60, -30])
ac_regulator['small_left'] = fuzz.trimf(ac_regulator.universe, [-60, -30, 0])
ac_regulator['off'] = fuzz.trimf(ac_regulator.universe, [-10, 0, 10])
ac_regulator['small_right'] = fuzz.trimf(ac_regulator.universe, [0, 30, 60])
ac_regulator['large_right'] = fuzz.trapmf(ac_regulator.universe, [30, 60, 90, 90])

rule1 = ctrl.Rule(room_temperature['very_warm'] & temp_change_rate['positive'], ac_regulator['large_left'])
rule2 = ctrl.Rule(room_temperature['very_warm'] & temp_change_rate['negative'], ac_regulator['small_left'])
rule3 = ctrl.Rule(room_temperature['warm'] & temp_change_rate['positive'], ac_regulator['large_left'])
rule4 = ctrl.Rule(room_temperature['warm'] & temp_change_rate['negative'], ac_regulator['off'])
rule5 = ctrl.Rule(room_temperature['very_cold'] & temp_change_rate['negative'], ac_regulator['large_right'])
rule6 = ctrl.Rule(room_temperature['very_cold'] & temp_change_rate['positive'], ac_regulator['small_right'])
rule7 = ctrl.Rule(room_temperature['cold'] & temp_change_rate['negative'], ac_regulator['large_right'])
rule8 = ctrl.Rule(room_temperature['cold'] & temp_change_rate['positive'], ac_regulator['off'])
rule9 = ctrl.Rule(room_temperature['very_warm'] & temp_change_rate['zero'], ac_regulator['large_left'])
rule10 = ctrl.Rule(room_temperature['warm'] & temp_change_rate['zero'], ac_regulator['small_left'])
rule11 = ctrl.Rule(room_temperature['very_cold'] & temp_change_rate['zero'], ac_regulator['large_right'])
rule12 = ctrl.Rule(room_temperature['cold'] & temp_change_rate['zero'], ac_regulator['small_right'])
rule13 = ctrl.Rule(room_temperature['normal'] & temp_change_rate['positive'], ac_regulator['small_left'])
rule14 = ctrl.Rule(room_temperature['normal'] & temp_change_rate['negative'], ac_regulator['small_right'])
rule15 = ctrl.Rule(room_temperature['normal'] & temp_change_rate['zero'], ac_regulator['off'])

ac_control = ctrl.ControlSystem([
    rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10,
    rule11, rule12, rule13, rule14, rule15
])
ac_simulation = ctrl.ControlSystemSimulation(ac_control)

ac_simulation.input['room_temperature'] = 28
ac_simulation.input['temp_change_rate'] = 2

ac_simulation.compute()

print(f"AC Regulator Angle: {ac_simulation.output['ac_regulator']:.2f} degrees")
