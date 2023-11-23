"""This file provides operations to download recipes."""

import json
import requests


def download_recipe_by_name(query):
    """
    Downloads recipe from API through searching meal by name.

    Args:
        query: Search query for meal

    Returns:
        Dictionary containing recipe name, instructions, and ingredients of searched recipe
    """
    url = 'https://www.themealdb.com/api/json/v1/1/search.php?s={}'.format(
        query)
    response = requests.get(url)
    response_json = response.json()
    return process_recipe_from_api(response_json)


def download_recipe_by_url(url):
    """
    Downloads recipe from API through URL.

    Args:
        url: URL of recipe to download

    Returns:
        Dictionary containing recipe name, instructions, and ingredients of searched recipe
    """
    response = requests.get(url)
    response_json = response.json()
    return process_recipe_from_api(response_json)


# def load_mock_recipe(file_name):
#     """
#     Loads test recipe JSON file.

#     Args:
#         file_name: File name containing mock recipe

#     Returns:
#         Dictionary containing recipe name, instructions, and ingredients of mock recipe
#     """
#     with open(file_name) as json_file:
#         data = json.load(json_file)
#         return load_recipe(data)


def process_recipe_from_api(data):
    """
    Transforms recipe returned by API into relevant data.

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
        ingredient = data['meals'][0]['strIngredient{}'.format(i)].lower()
        measure = data['meals'][0]['strMeasure{}'.format(i)].lower()

        if ingredient == '' or measure == '':
            break

        recipe['ingredients'][ingredient] = measure
    return recipe
