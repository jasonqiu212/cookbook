from units import convert_imperial_to_metric, convert_metric_to_imperial


class ParsedRecipe:
    """
    Class representing a parsed recipe.
    """

    def __init__(self, name, steps, ingredients, tools):
        self.name = name
        self.steps = steps
        self.ingredients = ingredients
        self.tools = tools

    def get_number_of_steps(self):
        return len(self.steps)

    def get_ingredients(self):
        return self.ingredients

    def get_tools(self):
        return self.tools

    def get_step(self, i):
        """
        Gets the i-th step of the recipe.

        Args:
            i: Index of step to retrieve.

        Returns:
            i-th step of the recipe. IndexError, if index is out of bounds.

        Raises:
            ValueError: If i is None.
            IndexError: If i is out of bounds.

        """
        if i == None:
            raise ValueError
        if i < 0 or i >= len(self.steps):
            raise IndexError
        return self.steps[i]

    def convert_units(self, target_unit):
        """
        Converts the units in this recipe to the target unit.

        Args:
            target_unit: Target unit. Valid units are 'METRIC' and 'IMPERIAL'.
        """
        if target_unit != 'METRIC' and target_unit != 'IMPERIAL':
            return
        for i in self.ingredients:
            if i.has_no_quantity() or i.is_countable():
                continue
            if target_unit == 'METRIC':
                i.quantity, i.measurement = convert_imperial_to_metric(
                    i.quantity, i.measurement)
            elif target_unit == 'IMPERIAL':
                i.quantity, i.measurement = convert_metric_to_imperial(
                    i.quantity, i.measurement)
        for i in self.steps:
            i.convert_units(target_unit)

    def translate_portion_size(self, ratio):
        """
        Translates the ingredient quantities in this recipe by a ratio.

        Args:
            ratio: Ratio to translate by.
        """
        if not isinstance(ratio, float) and not isinstance(ratio, int):
            return
        if ratio == 1:
            return
        for i in self.ingredients:
            if i.has_no_quantity():
                continue
            i.quantity = i.quantity * ratio
        for i in self.steps:
            i.translate_portion_size(ratio)

    def __repr__(self):
        s = ''
        for i, step in enumerate(self.steps):
            s += f'Step {i + 1}: {step}\n'
        return s.strip()
