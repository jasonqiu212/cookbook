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
        print()
        self.show_current_step()
        print()
        print('What do you wish to do next?')
        print('Hint: Not sure what to ask? Enter \"help\" to show the supported queries and questions.')

    def load_recipe(self, raw_recipe):
        """
        Extracts and loads recipe into bot.

        Args:
            raw_recipe: Raw recipe fetched from API.
        """
        name, steps, ingredients, tools = extract(raw_recipe)
        self.recipe = ParsedRecipe(name, steps, ingredients, tools)
        self.step_index = 0

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
            elif question == 'show all steps':
                self.show_steps()
            elif question == 'show all ingredients':
                self.show_ingredients()
            elif question == 'show all tools':
                self.show_tools()
            elif re.search('when do i need the [\w|\s]+', question):
                tool = re.search(
                    'when do i need the [\w|\s]+', question).group()[19:]
                self.show_step_for_tool(tool)
            elif re.search('how do i do that', question):
                self.show_vague_how_to()
            elif re.search('how do i', question) or re.search('how to', question):
                self.show_youtube_search(question)
            elif re.search('what is a', question):
                self.show_google_search(question)
            elif question == 'what ingredients do i need':
                self.show_current_step_ingredients()
            elif question == 'what tools do i need':
                self.show_current_step_tools()
            elif question == 'how long':
                self.show_current_step_time_parameters()
            elif question == 'what temperature':
                self.show_current_step_temperature_parameters()
            elif question == 'convert units':
                target_unit = self.get_unit_conversion_choice()
                self.recipe.convert_units(target_unit)
                self.show_ingredients()
            else:
                print('Sorry, I did not understand that.')

    def show_help(self):
        """
        Displays valid queries that the bot can understand.
        """
        print('Here are the queries and questions I can answer:')
        print('Tip: For convenience, I can detect the commands in lowercase and without punctuation too!')
        print()

        print('Basics:')
        print('- \'Help\': Display the supported queries and questions')
        print('- \'Quit\': Exit the chatbot')
        print()

        print('Navigation:')
        print('- \'Repeat\': Show the current step')
        print('- \'Next\': Show the next step')
        print('- \'Go back\': Show the previous step')
        print('- \'Step <STEP_NUMBER>\': Show a specific step')
        print()

        print('Questions about the recipe:')
        print('- \'Show all steps\': Show all steps of the recipe')
        print('- \'Show all ingredients\': Show the ingredients needed for the recipe')
        print('- \'Show all tools\': Show the tools needed for the recipe')
        print(
            '- \'When do I need the <TOOL>?\': Show the step number a tool is first used in')
        print()

        print('Questions about the current step:')
        print('- \'How do I do that?\': Ask a question on a previously mentioned task')
        print('- \'What is a <INGREDIENT/TOOL/UTENSIL>\': Ask a question on an ingredient/tool/utensil')
        print('- \'How do I <TECHNIQUE>\': Ask a question on a technique')
        print('- \'What ingredients do I need?\': Ask about the ingredients needed for this step')
        print('- \'What tools do I need?\': Ask about the ingredients needed for this step')
        print('- \'How long?\': Ask about the timings for this step')
        print('- \'What temperature?\': Ask about the temperature settings for this step')
        print()

        print('Transform recipe:')
        print(
            '- \'Convert units\': Convert the units from imperial to metric, or vice versa')

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
        self.show_list_in_numbered_list(self.recipe.get_ingredients())

    def show_tools(self):
        """
        Displays all tools needed for this recipe.
        """
        print('Here are all of the tools used in this recipe:')
        self.show_list_in_numbered_list(list(self.recipe.get_tools().keys()))

    def show_step_for_tool(self, query):
        """
        Displays the step number where the tool is used in.

        Args:
            query: The user's tool query.
        """
        for tool in self.recipe.get_tools().keys():
            if query in tool:
                print(
                    f'{tool.capitalize()} is/are used in step {self.recipe.get_tools()[tool] + 1}.')
                return
        print('Sorry, I cannot find the tool you are looking for in the recipe.')

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

    def show_youtube_search(self, query):
        """
        Displays a YouTube search URL for the given query.

        Args:
            query: The user's query.
        """
        base_url = "https://www.youtube.com/results?search_query="
        query_encoded = urllib.parse.quote(query)
        search_url = base_url + query_encoded
        return print(f'Here is a YouTube search for your question: {search_url}')

    def show_vague_how_to(self):
        """
        Displays an answer to a vague how to question using conversation history.
        """
        action = self.recipe.get_step(self.step_index).get_main_action()
        if action:
            print(
                f'Judging from the last step I showed you, are you asking about how to {action}?')
            query = f"How to {action}"
            return self.show_youtube_search(query)
        else:
            return 'The last step did not contain an action I recognize. Could you please specify the action?'

    def show_current_step_ingredients(self):
        """
        Displays a list of ingredients for the current step.
        """
        step_ingredients = self.recipe.get_step(
            self.step_index).get_ingredients()
        if step_ingredients:
            print('Here are all of the ingredients used in this step:')
            self.show_list_in_numbered_list(step_ingredients)
        else:
            print('No ingredients are needed for this step.')

    def show_current_step_tools(self):
        """
        Displays a list of tools for the current step.
        """
        step_tools = self.recipe.get_step(
            self.step_index).get_tools()
        if step_tools:
            print('Here are all of the tools used in this step:')
            self.show_list_in_numbered_list(step_tools)
        else:
            print('No tools are needed for this step.')

    def show_current_step_time_parameters(self):
        """
        Displays the time parameters for the current step.
        """
        time_parameters = self.recipe.get_step(
            self.step_index).get_time_parameters()
        if time_parameters:
            print('Here are the timings to watch out for:')
            for action, parameters in time_parameters.items():
                parameters_str = ' or '.join(parameters)
                print(f'- {action.capitalize()} for {parameters_str}')
        else:
            print('There are no timings for this step.')

    def show_current_step_temperature_parameters(self):
        """
        Displays the temperature parameters for the current step.
        """
        temperature_parameters = self.recipe.get_step(
            self.step_index).get_temperature_parameters()
        if len(temperature_parameters) == 0:
            print('There are no temperature parameters for this step.')
        elif len(temperature_parameters) == 1:
            print(temperature_parameters[0])
        else:
            print('Here are the temperature settings for this step:')
            for parameter in temperature_parameters:
                print(f'- {parameter}')

    def get_unit_conversion_choice(self):
        """
        Gets target unit from user.
        """
        print(
            'Got it! What unit which you like to convert to?')
        print('[1] Metric')
        print('[2] Imperial')
        while True:
            query_choice = input('> ')
            if query_choice == '1':
                print('Okay! Converting to metric units now!')
                return 'METRIC'
            if query_choice == '2':
                print('Okay! Converting to imperial units now!')
                return 'IMPERIAL'
            else:
                print(
                    'Sorry, I did not understand that. Please enter either 1 or 2 to indicate your choice.')

    def show_list_in_numbered_list(self, lst):
        """
        Displays list in numbered list format.

        Args:
            lst: List of strings to show.
        """
        for i, item in enumerate(lst):
            print(f'{i + 1}. {item}')
