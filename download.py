"""This file provides operations to download recipes."""

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
        ingredient = data['meals'][0]['strIngredient{}'.format(i)]
        measure = data['meals'][0]['strMeasure{}'.format(i)]

        if not ingredient or ingredient == '' or not measure or measure == '':
            break

        recipe['ingredients'][ingredient.lower()] = measure.lower()
    return recipe
