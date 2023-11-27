class Step:
    """
    Class representing a step in the cookbook with annotations. 
    """

    def __init__(self, text, actions, ingredients, tools, utensils, parameters):
        self.text = text
        self.actions = actions
        self.ingredients = ingredients
        self.tools = tools
        self.utensils = utensils
        self.parameters = parameters

    def __repr__(self):
        return self.text
