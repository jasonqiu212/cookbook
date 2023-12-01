"""This file provides operations to extract information."""

import re

import ftfy
import spacy

from ingredient import Ingredient
from step import Step

nlp = spacy.load("en_core_web_md")


def preprocess(str):
    """
    Fixes mojibake and removes extra whitespace.
    """
    str = ftfy.fix_text(str)
    return re.sub('\s+', ' ', str)


def is_imperative(sentence):
    """
    Checks if sentence is imperative.

    Args:
        sentence: Sentence to check.

    Returns:
        True, if sentence is imperative. False otherwise.
    """
    doc = nlp(sentence)

    first_token = doc[0]
    if first_token.tag_ == 'VB':
        return True
    return False


def get_verbs(imperative_sentence):
    """
    Extracts the verbs from an imperative sentence.

    Args:
        imperative_sentence: Imperative sentence to extract from. 

    Returns:
        List of verbs.
    """
    doc = nlp(imperative_sentence)

    verbs = []
    for i, token in enumerate(doc):
        # Assuming sentence is imperative, 1st token should be an action
        if i == 0 or token.tag_ == 'VB':
            verbs.append(token.text.lower())
    return verbs


def get_nouns_compounds(sentence):
    """
    Extracts compounds that behave as a single noun from a sentence.

    Args:
        sentence: Sentence to extract from. 

    Returns:
        List of compounds.
    """
    doc = nlp(sentence)

    compounds = []
    for token in doc:
        if token.pos_ == 'NOUN':
            compound = []
            for child in token.children:
                if child.dep_ == 'compound':
                    compound.append(child.text.lower())
            compound.append(token.text.lower())
            compounds.append(' '.join(compound))
    return compounds


def get_direct_objects(sentence):
    """
    Extracts the direct objects from a sentence.

    Args:
        sentence: Sentence to extract from. 

    Returns:
        List of direct objects.
    """
    doc = nlp(sentence)

    direct_objects = []
    for token in doc:
        if token.dep_ == 'dobj':
            direct_objects.append(token.text.lower())
    return direct_objects


def get_indirect_objects(sentence):
    """
    Extracts the indirect objects from a sentence.

    Args:
        sentence: Sentence to extract from. 

    Returns:
        List of indirect objects.
    """
    doc = nlp(sentence)

    indirect_objects = []
    for token in doc:
        if token.dep_ == 'pobj':
            indirect_objects.append(token.text.lower())
    return indirect_objects


def extract_steps(raw_instructions):
    """
    Extracts steps from recipe.

    Args:
        raw_instructions: String representing the instructions in the recipe.

    Returns:
        List of steps.
    """
    raw_steps = []
    instructions = preprocess(raw_instructions)
    instruction_sentences = instructions.split('. ')
    l = 0
    r = 1
    while r < len(instruction_sentences):
        sentence = instruction_sentences[r] + '.'
        if is_imperative(sentence):
            raw_steps.append('. '.join(instruction_sentences[l:r]) + '.')
            l = r
        r = r + 1
    raw_steps.append('. '.join(instruction_sentences[l:r]))

    steps = []
    for raw_step in raw_steps:
        actions = get_verbs(raw_step)

        # TODO
        ingredients = []
        tools = []
        utensils = []
        parameters = []
        steps.append(Step(raw_step, actions, ingredients,
                     tools, utensils, parameters))
    return steps


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
    steps = extract_steps(raw_recipe['instructions'])
    ingredients = extract_ingredients(raw_recipe['ingredients'])

    return name, steps, ingredients
