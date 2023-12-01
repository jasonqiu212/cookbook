import re
import urllib.parse

from download import download_recipe_by_name, download_recipe_by_url
from extract import extract
from parsed_recipe import ParsedRecipe


class Bot:
    """
    Class representing a bot that can answer questions about a recipe. 
    """

    def __init__(self):
        self.history = []
        self.recipe = None
        self.step_index = None
        self.last_mentioned_action = None

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

        print(f'Thanks! Let\'s start working with \"{self.recipe.name}\".')
        self.show_current_step()
        print('What do you wish to do next?')
        print('Hint: Not sure what to ask? Enter \"help\" to show the supported queries and questions.')

    def load_recipe(self, raw_recipe):
        """
        Extracts and loads recipe into bot.

        Args:
            raw_recipe: Raw recipe fetched from API.
        """
        name, steps, ingredients = extract(raw_recipe)
        self.recipe = ParsedRecipe(name, steps, ingredients)
        self.step_index = 0

        # TODO
        self.last_mentioned_action = None

    def answer_queries(self):
        """
        Answers user's queries.
        """
        while True:
            question = input('> ').lower()
            if question == 'help':
                self.show_help()
            elif question == 'quit':
                print('Hope your food tastes great! Goodbye.')
                break
            elif question == 'show all steps':
                self.show_steps()
            elif question == 'show all ingredients':
                self.show_ingredients()
            elif question == 'repeat':
                self.show_current_step()
            elif question == 'next':
                self.show_next_step()
            elif question == 'go back':
                self.show_previous_step()
            elif re.search('step [\d]+', question):
                i = re.search(
                    'step [\d]+', question).group().split()[-1]
                self.show_step_i(i)
            elif re.search('what is a', question) or re.search('how do i', question):
                self.show_google_search(question)
            elif re.search('how do i do that', question):
                self.show_vague_how_to()
            # TODO: Add other cases using regular expression

    def show_help(self):
        """
        Displays valid queries that the bot can understand.
        """
        print('Here are the queries and questions I can answer:')
        print('- \'Help\': Display the supported queries and questions')
        print('- \'Quit\': Exit the chatbot')
        print('- \'Show all steps\': Show all steps of the recipe')
        print('- \'Show all ingredients\': Show the ingredients of the recipe')
        print('- \'Repeat\': Show the current step')
        print('- \'Next\': Show the next step')
        print('- \'Go back\': Show the previous step')
        print('- \'Step <STEP_NUMBER>\': Show a specific step')
        print('- \'What is a <INGREDIENT/TOOL/UTENSIL>\': Ask a question on an ingredient/tool/utensil')
        print('- \'How do I <TECHNIQUE>\': Ask a question on a technique')
        print('- \'How do I do that?\': Ask a question on the previously mentioned task')

    def show_steps(self):
        """
        Displays all steps for this recipe.
        """
        print('Here are all of the steps in this recipe:')
        print(self.recipe)

    def show_current_step(self):
        """
        Displays the current step for this recipe.
        """
        try:
            current_step = self.recipe.get_step(self.step_index)
        except ValueError:
            print('Recipe has not been loaded yet.')
        else:
            print(f"Step {self.step_index + 1}: {current_step}")

    def show_next_step(self):
        """
        Displays the next step.
        """
        if self.step_index >= self.recipe.get_number_of_steps() - 1:
            print('We are already at the last step of the recipe.')
        else:
            self.step_index += 1
            self.show_current_step()

    def show_previous_step(self):
        """
        Displays the previous step.
        """
        if self.step_index <= 0:
            print('We are already at the first step of the recipe.')
        else:
            self.step_index -= 1
            self.show_current_step()

    def show_step_i(self, i):
        """
        Displays the i-th step for this recipe.

        Args:
            i: Index of step to show.
        """
        try:
            self.recipe.get_step(int(i) - 1)
        except IndexError:
            print(
                f'This is an invalid step number. Please enter a step number between 1 and {self.recipe.get_number_of_steps()}')
        else:
            self.step_index = int(i) - 1
            self.show_current_step()

    def show_ingredients(self):
        """
        Displays all ingredients needed for this recipe.
        """
        print('Here are all of the ingredients used in this recipe:')
        for i, ingredient in enumerate(self.recipe.get_ingredients()):
            print(f'{i + 1}. {ingredient}')

    def show_google_search(self, query):
        """
        Displays a Google search URL for the given query.

        Args:
            query: The user's query.
        """
        base_url = 'https://www.google.com/search?q='
        query_encoded = urllib.parse.quote(query)
        search_url = base_url + query_encoded
        print(f'Here is a Google search for your question: {search_url}')

    def show_vague_how_to(self):
        """
        Displays an answer to a vague how to question using conversation history.
        """
        # TODO
