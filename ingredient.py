import editdistance


class Ingredient:
    """
    Class representing an ingredient.
    """

    COUNTABLE_MEASUREMENT = 'COUNTS'
    NO_QUANTITY = -1

    def show_ingredients(ingredients):
        """
        Displays ingredients in given list.

        Args:
            ingredients: List of ingredients to show.
        """
        for i, ingredient in enumerate(ingredients):
            print(f'{i + 1}. {ingredient}')

    def __init__(self, name, quantity, measurement, descriptors):
        self.name = name
        self.quantity = quantity
        self.measurement = measurement
        self.descriptors = descriptors

    def is_similar(self, str):
        """
        Checks if this ingredient's name is similar to given string using edit distance.

        Args:
            str: String to check similarity with.

        Returns:
            True, if similar. False otherwise.
        """
        contains_str = str in self.name
        return editdistance.eval(str, self.name) < 2 or contains_str

    def is_countable(self):
        return self.measurement == Ingredient.COUNTABLE_MEASUREMENT

    def has_no_quantity(self):
        return self.measurement == Ingredient.NO_QUANTITY

    def __repr__(self):
        descriptors_str = ', ' + ' and '.join(
            self.descriptors) if self.descriptors else ''
        if self.quantity == Ingredient.NO_QUANTITY:
            return f'{self.name}{descriptors_str}'
        if self.measurement == Ingredient.COUNTABLE_MEASUREMENT:
            return f'{self.quantity} {self.name}{descriptors_str}'
        return f'{self.quantity} {self.measurement} of {self.name}{descriptors_str}'
