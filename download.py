"""This file provides operations to download and load recipes."""

import json


def download_recipe_by_name(query):
    """
    Downloads recipe from API through searching meal by name.

    Args:
        query: Search query for meal

    Returns:
        Dictionary containing recipe name, instructions, and ingredients of searched recipe
    """
    # TODO: Change as per required for chosen API
    data = {}
    return load_recipe(data)


def load_mock_recipe(file_name):
    """
    Loads test recipe JSON file.

    Args:
        file_name: File name containing mock recipe

    Returns:
        Dictionary containing recipe name, instructions, and ingredients of mock recipe
    """
    with open(file_name) as json_file:
        data = json.load(json_file)
        return load_recipe(data)


def load_recipe(data):
    """
    Loads recipe returned by API into relevant data.

    Args:
        data: Recipe returned by API

    Returns:
        Dictionary containing recipe name, instructions, and ingredients
    """
    recipe = {}
    recipe['name'] = data['meals'][0]['strMeal']
    recipe['instructions'] = data['meals'][0]['strInstructions']
    recipe['ingredients'] = {}
    for i in range(1, 21):
        ingredient = data['meals'][0]['strIngredient{}'.format(i)]
        measure = data['meals'][0]['strMeasure{}'.format(i)]

        if ingredient == '' or measure == '':
            break

        recipe['ingredients'][ingredient] = measure
    return recipe
