class Ingredient:
    """
    Class representing an ingredient.
    """

    COUNTABLE_MEASUREMENT = 'COUNTS'

    def __init__(self, name, quantity, measurement):
        self.name = name
        self.quantity = quantity
        self.measurement = measurement

    def __repr__(self):
        if self.measurement == Ingredient.COUNTABLE_MEASUREMENT:
            return f'{self.quantity} {self.name}'
        return f'{self.quantity} {self.measurement} of {self.name}'
