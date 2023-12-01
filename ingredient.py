import editdistance


class Ingredient:
    """
    Class representing an ingredient.
    """

    COUNTABLE_MEASUREMENT = 'COUNTS'

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
        return editdistance.eval(str, self.name) < 5

    def __repr__(self):
        if self.measurement == Ingredient.COUNTABLE_MEASUREMENT:
            return f'{self.quantity} {self.name}'
        return f'{self.quantity} {self.measurement} of {self.name}'
