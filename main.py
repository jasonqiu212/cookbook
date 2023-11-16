"""This file serves as the entry point of the program."""

from bot import Bot
from download import download_recipe_by_name, load_mock_recipe
from extract import extract


def main():
    # # Change following constants if needed
    # RECIPE_NAME_QUERY = 'meatloaf'
    # MOCK_RECIPE_FILE_NAME = 'mock-recipe-1.json'

    # # recipe = download_recipe_by_name(RECIPE_NAME_QUERY)
    # recipe = load_mock_recipe(MOCK_RECIPE_FILE_NAME)
    # results = extract(recipe)
    # print(results)
    bot = Bot()
    bot.start()


if __name__ == '__main__':
    main()
