class ParsedRecipe:
    """
    Class representing a parsed recipe.
    """

    def __init__(self, name, steps, ingredients):
        self.name = name
        self.steps = steps
        self.ingredients = ingredients

    def get_number_of_steps(self):
        return len(self.steps)

    def get_ingredients(self):
        return self.ingredients

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
