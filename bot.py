from download import download_recipe_by_name, download_recipe_by_url
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
        self.get_recipe_source()
        self.answer_queries()

    def get_recipe_source(self):
        """
        Gets recipe source from user.
        """
        print(
            'Welcome to your interactive cookbook! How would you like to fetch your recipe from TheMealDB?')
        print('[1] URL to a specific recipe.')
        print('[2] Search recipe by name.')
        while True:
            query_choice = input('> ')
            if query_choice == '1':
                print('Got it! Please input the URL to a recipe on TheMealDB.')
                url = input('> ')
                raw_recipe = download_recipe_by_url(url)
                self.load_recipe(raw_recipe)
                break
            if query_choice == '2':
                print('Got it! Please input the name to a recipe you wish to cook.')
                name = input('> ')
                raw_recipe = download_recipe_by_name(name)
                self.load_recipe(raw_recipe)
                break
            else:
                print(
                    'Sorry, I did not understand that. Please enter either 1 or 2 to indicate your choice.')

        print('Thanks! Let\'s start working with \"{}\". What do you want to do?'.format(
            self.recipe.name))
        print('Hint: Not sure what to ask? Enter \"help\" to show the supported queries and questions.')

    def load_recipe(self, raw_recipe):
        """
        Extracts and loads recipe into bot.

        Args:
            raw_recipe: Raw recipe fetched from API
        """
        # TODO: Call extraction methods
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
            # TODO: Add other cases using regular expression?
            # elif question == ...

    def show_help(self):
        """
        Displays valid queries that the bot can understand.
        """
        print('Here are the queries and questions I can answer:')
        print('help: Display the supported queries and questions')
        print('quit: Exit the chatbot')
        # TODO: Add more possible commands

    def show_steps(self):
        """
        Displays all steps for this recipe.
        """
        # TODO

    def show_current_step(self):
        """
        Displays all steps for this recipe.
        """
        # TODO

    def show_next_step(self):
        """
        Displays the next step.
        """
        # TODO

    def show_previous_step(self):
        """
        Displays the previous step.
        """
        # TODO

    def show_step_i(self, i):
        """
        Displays the i-th step for this recipe.

        Args:
            i: Index of step to show
        """
        # TODO

    def show_ingredients(self):
        """
        Displays all ingredients needed for this recipe.
        """
        # TODO

    def show_google_search(self, query):
        """
        Displays a link to a Google search 
        """
        # TODO
