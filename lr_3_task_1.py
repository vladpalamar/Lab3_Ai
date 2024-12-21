import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

water_temperature = ctrl.Antecedent(np.arange(0, 101, 1), 'water_temperature')
water_pressure = ctrl.Antecedent(np.arange(0, 101, 1), 'water_pressure')

hot_water_valve = ctrl.Consequent(np.arange(-90, 91, 1), 'hot_water_valve')
cold_water_valve = ctrl.Consequent(np.arange(-90, 91, 1), 'cold_water_valve')

water_temperature['cold'] = fuzz.trapmf(water_temperature.universe, [0, 0, 20, 40])
water_temperature['cool'] = fuzz.trimf(water_temperature.universe, [20, 40, 60])
water_temperature['warm'] = fuzz.trimf(water_temperature.universe, [50, 70, 90])
water_temperature['hot'] = fuzz.trapmf(water_temperature.universe, [70, 90, 100, 100])

water_pressure['weak'] = fuzz.trapmf(water_pressure.universe, [0, 0, 20, 50])
water_pressure['medium'] = fuzz.trimf(water_pressure.universe, [20, 50, 80])
water_pressure['strong'] = fuzz.trapmf(water_pressure.universe, [50, 80, 100, 100])

hot_water_valve['large_left'] = fuzz.trapmf(hot_water_valve.universe, [-90, -90, -60, -30])
hot_water_valve['medium_left'] = fuzz.trimf(hot_water_valve.universe, [-60, -30, 0])
hot_water_valve['small_left'] = fuzz.trimf(hot_water_valve.universe, [-30, 0, 30])
hot_water_valve['small_right'] = fuzz.trimf(hot_water_valve.universe, [0, 30, 60])
hot_water_valve['medium_right'] = fuzz.trimf(hot_water_valve.universe, [30, 60, 90])
hot_water_valve['large_right'] = fuzz.trapmf(hot_water_valve.universe, [60, 90, 90, 90])

cold_water_valve['large_left'] = fuzz.trapmf(cold_water_valve.universe, [-90, -90, -60, -30])
cold_water_valve['medium_left'] = fuzz.trimf(cold_water_valve.universe, [-60, -30, 0])
cold_water_valve['small_left'] = fuzz.trimf(cold_water_valve.universe, [-30, 0, 30])
cold_water_valve['small_right'] = fuzz.trimf(cold_water_valve.universe, [0, 30, 60])
cold_water_valve['medium_right'] = fuzz.trimf(cold_water_valve.universe, [30, 60, 90])
cold_water_valve['large_right'] = fuzz.trapmf(cold_water_valve.universe, [60, 90, 90, 90])

rule1 = ctrl.Rule(water_temperature['hot'] & water_pressure['strong'],
                  (hot_water_valve['medium_left'], cold_water_valve['medium_right']))
rule2 = ctrl.Rule(water_temperature['hot'] & water_pressure['medium'],
                  cold_water_valve['medium_right'])
rule3 = ctrl.Rule(water_temperature['warm'] & water_pressure['strong'],
                  hot_water_valve['small_left'])
rule4 = ctrl.Rule(water_temperature['warm'] & water_pressure['weak'],
                  (hot_water_valve['small_right'], cold_water_valve['small_right']))
rule5 = ctrl.Rule(water_temperature['warm'] & water_pressure['medium'],
                  (hot_water_valve['small_left'], cold_water_valve['small_left']))
rule6 = ctrl.Rule(water_temperature['cool'] & water_pressure['strong'],
                  (hot_water_valve['medium_right'], cold_water_valve['medium_left']))
rule7 = ctrl.Rule(water_temperature['cool'] & water_pressure['medium'],
                  (hot_water_valve['medium_right'], cold_water_valve['small_left']))
rule8 = ctrl.Rule(water_temperature['cold'] & water_pressure['weak'],
                  hot_water_valve['large_right'])
rule9 = ctrl.Rule(water_temperature['cold'] & water_pressure['strong'],
                  (hot_water_valve['medium_left'], cold_water_valve['medium_right']))
rule10 = ctrl.Rule(water_temperature['warm'] & water_pressure['strong'],
                   (hot_water_valve['small_left'], cold_water_valve['small_left']))
rule11 = ctrl.Rule(water_temperature['warm'] & water_pressure['weak'],
                   (hot_water_valve['small_right'], cold_water_valve['small_right']))

water_control = ctrl.ControlSystem([
    rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11
])
water_simulation = ctrl.ControlSystemSimulation(water_control)

water_simulation.input['water_temperature'] = 80
water_simulation.input['water_pressure'] = 70

water_simulation.compute()

print(f"Hot Water Valve Angle: {water_simulation.output['hot_water_valve']:.2f} degrees")
print(f"Cold Water Valve Angle: {water_simulation.output['cold_water_valve']:.2f} degrees")
