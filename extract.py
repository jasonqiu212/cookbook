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
    common_verbs = {'close', 'sit', 'stand', 'go', 'come', 'turn', 'bring', 'take', 'give', 'move', 'stop', 'start',
                    'leave', 'write', 'read', 'speak', 'listen', 'buy', 'pay', 'watch', 'play', 'run', 'walk', 'eat',
                    'drink', 'sleep'}
    pronouns = {'I', 'you', 'he', 'she', 'it', 'we', 'they'}
    interrogatives = {'what', 'who', 'how', 'where', 'when', 'why'}

    words = sentence.lower().split()

    if words:
        first_word = words[0]
        return first_word in common_verbs and first_word not in pronouns and first_word not in interrogatives

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
