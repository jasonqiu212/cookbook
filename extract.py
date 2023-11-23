"""This file provides operations to extract information."""

import spacy

from ingredient import Ingredient
from step import Step

# TODO: Method for extracting cooking actions
# TODO: Method for extracting ingredients
# TODO: Method for extracting tools, utensils, and parameters
nlp = spacy.load("en_core_web_sm")


def is_imperative(sentence):
    """
    Checks if sentence is imperative.

    Args:
        sentence: Sentence to check

    Returns:
        True, if sentence is imperative. False otherwise.
    """
    doc = nlp(sentence)

    for token in doc:
        if token.dep_ == "ROOT" and token.pos_ == "VERB" and token.tag_ == "VB":
            has_no_explicit_subject = not any(
                child.dep_ in ["nsubj", "nsubjpass"] for child in token.children)
            if has_no_explicit_subject:
                return True
    return False


def extract_ingredients(raw_ingredients):
    """
    Extracts ingredients from recipe.

    Args:
        raw_ingredients: Dictionary with ingredient name mapped to quantity

    Returns:
        List of ingredients.
    """
    ingredients = []
    for name, quantity in raw_ingredients.items():
        quantity_word_list = quantity.split()
        if len(quantity_word_list) == 0:
            ingredients.append(Ingredient(name, '', ''))
        elif len(quantity_word_list) == 1:
            ingredients.append(Ingredient(
                name, quantity_word_list[0], Ingredient.COUNTABLE_MEASUREMENT))
        else:
            ingredients.append(Ingredient(
                name, quantity_word_list[0], ' '.join(quantity_word_list[1:])))
    return ingredients


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
    ingredients = extract_ingredients(raw_recipe['ingredients'])

    # TODO: Include extraction methods here

    return name, steps, ingredients
