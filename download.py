"""This file provides operations to download and load recipes."""

import json


def download():
    """
    Loads recipe from API.

    Returns:
        Dictionary representing ingredients and steps of recipe.
    """
    # TODO: Change as per required for chosen API


def load_test_recipe():
    """
    Loads test recipe JSON file.

    Returns:
        Dictionary representing ingredients and steps of recipe.
    """
    # TODO: Change as per required for chosen API
    with open("recipe.json") as json_file:
        return json.load(json_file)
