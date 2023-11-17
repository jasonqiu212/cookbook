"""This file provides operations to extract information."""

import step

# TODO: Method for extracting cooking actions
# TODO: Method for extracting ingredients
# TODO: Method for extracting tools, utensils, and parameters


def is_imperative(sentence):
    """
    Checks if sentence is imperative.
    """
    # TODO


def extract(raw_recipe):
    """
    Extracts name, ingredients, and steps with annotations from recipe.

    Args:
        raw_recipe: Dictionary representing recipe to extract from

    Returns:
        Tuple of recipe name, ingredients and steps with annotations
    """
    name = raw_recipe['name']
    steps = []
    ingredients = []

    # TODO: Include extraction methods here

    return name, steps, ingredients
