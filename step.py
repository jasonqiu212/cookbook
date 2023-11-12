class Step:
    """
    Class representing a step in the cookbook with annotations. 
    """

    def __init__(self, text, action, ingredients, tools, utensils, parameters):
        self.text = text
        self.action = action
        self.ingredients = ingredients
        self.tools = tools
        self.utensils = utensils
        self.parameters = parameters
