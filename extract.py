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


def get_noun_compounds(sentence):
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
                if child.dep_ == 'compound' or child.dep_ == 'nmod':
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


def extract_ingredients_from_step(sentence, ingredients):
    """
    Extracts ingredients from sentence that appear in list of ingredients.

    Args:
        sentence: Sentence to extract from.
        ingredients: List of ingredients for recipe.

    Returns:
        List of ingredients in sentence.
    """
    noun_compounds = get_noun_compounds(sentence)
    step_ingredients = set()
    for noun_compound in noun_compounds:
        for ingredient in ingredients:
            if ingredient.is_similar(noun_compound):
                step_ingredients.add(ingredient)
                break
    return list(step_ingredients)


def extract_steps(raw_instructions, ingredients):
    """
    Extracts steps from recipe.

    Args:
        raw_instructions: String representing the instructions in the recipe.
        ingredients: List of ingredients for recipe.

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
        step_ingredients = extract_ingredients_from_step(raw_step, ingredients)

        # TODO
        tools = []
        utensils = []
        parameters = []
        steps.append(Step(raw_step, actions, step_ingredients,
                     tools, utensils, parameters))
    return steps


def extract_ingredients(raw_ingredients):
    """
    Extracts ingredients from recipe.

    Args:
        raw_ingredients: Dictionary with ingredient name mapped to quantity.

    Returns:
        List of ingredients.
    """
    ingredients = []
    for name, quantity in raw_ingredients.items():
        quantity_word_list = quantity.split()
        ingredient = None

        if len(quantity_word_list) == 0:
            ingredient = Ingredient(
                name, Ingredient.NO_QUANTITY, Ingredient.COUNTABLE_MEASUREMENT, [])
        elif len(quantity_word_list) == 1:
            token = quantity_word_list[0]

            # Single token in format of '<QUANTITY>'
            # i.e. Ingredient is countable
            if token.isnumeric():
                ingredient = Ingredient(
                    name, token, Ingredient.COUNTABLE_MEASUREMENT, [])

            # Single token representing '<DESCRIPTOR>'
            elif token.isalpha():
                ingredient = Ingredient(
                    name, Ingredient.NO_QUANTITY, Ingredient.COUNTABLE_MEASUREMENT, [token])

            # Single token in format of '<QUANTITY><MEASUREMENT>'
            else:
                numeric_match = re.search('\d+', token)
                split_index = numeric_match.end() if numeric_match else len(token) + 1
                q = token[:split_index]
                m = token[split_index:]
                ingredient = Ingredient(name, q, m, [])

        else:
            parenthesis_matches = re.findall('\(.+\)', quantity)
            for match in parenthesis_matches:
                quantity = quantity.replace(match, '')

            quantity_word_list = quantity.split()

            # Multiple tokens in format of '<FRACTION_QUANTITY> <MEASUREMENT> DESCRIPTORS>'
            if quantity_word_list[0].isnumeric() and re.search('\d\/\d', quantity_word_list[1]):
                fraction_token = quantity_word_list[1]
                numerator_match = re.search('\d', fraction_token)
                split_index = numerator_match.end()
                numerator, denominator = int(fraction_token[:split_index]), int(
                    fraction_token[split_index + 1:])
                q = int(quantity_word_list[0]) + \
                    round(numerator / denominator, 2)

                m = quantity_word_list[2] if len(
                    quantity_word_list) >= 3 else Ingredient.COUNTABLE_MEASUREMENT
                d = ' '.join(quantity_word_list[3:]).split(' and ') if len(
                    quantity_word_list) >= 4 else []
                d = list(map(lambda s: s.strip(), d))
                ingredient = Ingredient(name, q, m, d)

            # Multiple tokens in format of '<QUANTITY> <MEASUREMENT> <DESCRIPTORS>'
            elif quantity_word_list[0].isnumeric():
                q = int(quantity_word_list[0])
                m = quantity_word_list[1]
                d = ' '.join(quantity_word_list[2:]).split(' and ') if len(
                    quantity_word_list) >= 3 else []
                d = list(map(lambda s: s.strip(), d))
                ingredient = Ingredient(
                    name, q, m, d)

            # Multiple tokens that are all descriptors
            else:
                d = quantity.split(' and ')
                d = list(map(lambda s: s.strip(), d))
                ingredient = Ingredient(
                    name, Ingredient.NO_QUANTITY, Ingredient.COUNTABLE_MEASUREMENT, d)

        ingredients.append(ingredient)
    return ingredients


def extract(raw_recipe):
    """
    Extracts name, ingredients, and steps with annotations from recipe.

    Args:
        raw_recipe: Dictionary representing recipe to extract from.

    Returns:
        Tuple of recipe name, ingredients and steps with annotations.
    """
    name = raw_recipe['name']
    ingredients = extract_ingredients(raw_recipe['ingredients'])
    steps = extract_steps(raw_recipe['instructions'], ingredients)

    return name, steps, ingredients
