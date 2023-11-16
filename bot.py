from parsed_recipe import ParsedRecipe


class Bot:
    """
    Class representing a bot that can answer questions about a recipe. 
    """

    def __init__(self):
        self.history = []
        self.recipe = None
        self.step_pointer = None

    def start(self):
        """
        Starts interactions with user.
        """
        print(
            'Welcome to your interactive cookbook! Please input a URL to a recipe from XXX.')
        url = input('> ')
        self.load_recipe(url)

        print('Thanks! Let\'s start working with \"{}\". What do you want to do?'.format(
            self.recipe.name))
        print('Hint: Not sure what to ask? Enter \"help\" to show the supported queries and questions.')

        self.answer_queries()

    def load_recipe(self, url):
        """
        Loads and extracts recipe from link into bot.

        Args:
            url: Weblink to load recipe from
        """
        # call extraction methods
        name = ''
        steps = []
        ingredients = []
        self.recipe = ParsedRecipe(name, steps, ingredients)
        self.step_pointer = 0

    def answer_queries(self):
        """
        Answers user's queries.
        """
        while True:
            question = input('> ').lower()
            if question == 'quit':
                print('Hope your food tastes great! Goodbye.')
                break
            elif question == 'help':
                self.show_help()
            # TODO: Add other cases
            # elif question == ...

    def show_help():
        """
        Displays valid queries that the bot can understand.
        """
        print('Here are the queries and questions I can answer:')
        print('1. help: Display the supported queries and questions')
        print('2. quit: Exit the chatbot')
        # TODO: Add more possible commands

    def show_ingredients():
        """
        Displays all ingredients needed for this recipe.
        """
