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
        name, steps, ingredients = extract(raw_recipe)
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


    def answer_what_is(question, recipe_json):
        # 解析问题中的关键词
        key_word = question.lower().split("what is ")[1].replace("?", "").strip()

        # 搜索成分
        for ingredient in recipe_json["ingredients"]:
            if key_word in ingredient["name"].lower():
                return f"{ingredient['name']} is an ingredient used in the recipe, with a quantity of {ingredient['quantity']}."

        # 搜索工具
        for tool in recipe_json["tools"]:
            if key_word in tool.lower():
                return f"{tool} is a tool used in the recipe."

        # 如果没有找到
        return "I'm sorry, I couldn't find information about that in the recipe."


#what is示例使用
#recipe_json = json.loads(your_recipe_json_string)  # 假设 your_recipe_json_string 是你从API获取的JSON字符串
#question = "What is pancetta?"
#answer = answer_what_is(question, recipe_json)
#print(answer)


    def answer_how_to(question, recipe_json):
        # 解析问题中的关键动作
        action = question.lower().split("how do i ")[1].replace("?", "").strip()

        # 搜索步骤
        for step in recipe_json["steps"]:
            if action in step.lower():
                return step

        # 如果没有找到
        return "I'm sorry, I couldn't find specific instructions on that in the recipe."

# how to 示例使用
#recipe_json = json.loads(your_recipe_json_string)  # 假设 your_recipe_json_string 是你从API获取的JSON字符串
#question = "How do I whisk the eggs?"
#answer = answer_how_to(question, recipe_json)
#print(answer)
    
