import editdistance


class Ingredient:
    """
    Class representing an ingredient.
    """

    COUNTABLE_MEASUREMENT = 'COUNTS'

    def show_ingredients(ingredients):
        """
        Displays ingredients in given list.

        Args:
            ingredients: List of ingredients to show.
        """
        for i, ingredient in enumerate(ingredients):
            print(f'{i + 1}. {ingredient}')

    def __init__(self, name, quantity, measurement):
        self.name = name
        self.quantity = quantity
        self.measurement = measurement

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

    def __repr__(self):
        if self.measurement == Ingredient.COUNTABLE_MEASUREMENT:
            return f'{self.quantity} {self.name}'
        return f'{self.quantity} {self.measurement} of {self.name}'
