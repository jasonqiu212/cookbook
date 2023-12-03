import re

from units import convert_celsius_to_fahrenheit, convert_fahrenheit_to_celsius, convert_imperial_to_metric, convert_metric_to_imperial, IMPERIAL_TO_METRIC, METRIC_TO_IMPERIAL


class Step:
    """
    Class representing a step in the cookbook with annotations. 
    """

    def __init__(self, text, actions, main_action, ingredients, tools, parameters):
        self.text = text
        self.actions = actions
        self.main_action = main_action
        self.ingredients = ingredients
        self.tools = tools
        self.parameters = parameters

    def get_actions(self):
        return self.actions

    def get_main_action(self):
        return self.main_action

    def get_ingredients(self):
        return self.ingredients

    def get_tools(self):
        return self.tools

    def get_time_parameters(self):
        return self.parameters['time']

    def get_temperature_parameters(self):
        return self.parameters['temperature']

    def convert_units(self, target_unit):
        """
        Converts the units in this recipe to the target unit.

        Args:
            target_unit: Target unit. Valid units are 'METRIC' and 'IMPERIAL'.
        """
        if target_unit != 'METRIC' and target_unit != 'IMPERIAL':
            return

        temperature_parameters = self.get_temperature_parameters()

        to_match = '\d*\.?\d+°C' if target_unit == 'IMPERIAL' else '\d*\.?\d+°F'
        f_temp = convert_celsius_to_fahrenheit if target_unit == 'IMPERIAL' else convert_fahrenheit_to_celsius

        converted_parameters = []

        for p in temperature_parameters:
            while re.search(to_match, p):
                temperature = float(re.search(to_match, p).group()[:-2])
                converted, unit = f_temp(temperature)
                p = re.sub(to_match, str(converted) + unit, p, 1)
            converted_parameters.append(p)

        self.parameters['temperature'] = converted_parameters

        for original, converted in zip(temperature_parameters, converted_parameters):
            self.text = self.text.replace(original, converted)

        units = METRIC_TO_IMPERIAL if target_unit == 'IMPERIAL' else IMPERIAL_TO_METRIC
        f = convert_metric_to_imperial if target_unit == 'IMPERIAL' else convert_imperial_to_metric

        for unit in reversed(units.keys()):
            if re.search(f'\d*\.?\d+ {unit}', self.text):
                m = re.search(f'\d*\.?\d+ {unit}', self.text).group()
                print(m)
                q_str = m.replace(f' {unit}', '')
                q = int(q_str) if q_str.isnumeric() else float(q_str)
                converted_quantity, converted_measurement = f(q, unit)
                self.text = self.text.replace(m, ' '.join(
                    [str(converted_quantity), converted_measurement]))

    def __repr__(self):
        return self.text
