"""This file provides operations to extract information."""

import step
import spacy

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
