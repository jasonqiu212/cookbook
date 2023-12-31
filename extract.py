"""This file provides operations to extract information."""

from collections import defaultdict
from unicodedata import numeric
import re

import ftfy
import spacy

from ingredient import Ingredient
from step import Step

nlp = spacy.load("en_core_web_md")


def preprocess(t):
    """
    Fixes mojibake, removes extra whitespace, and replaces vulgar fractions.
    """
    VULGAR_FRACTIONS = ['¼', '½', '¾', '⅐', '⅑', '⅒', '⅓', '⅔',
                        '⅕', '⅖', '⅗', '⅘', '⅙', '⅚', '⅛', '⅜', '⅝', '⅞', '⅟', '↉']
    t = ftfy.fix_text(t)
    for frac in VULGAR_FRACTIONS:
        while re.search(frac, t):
            m = re.search(frac, t).group()
            converted = str(round(numeric(m), 2))
            t = t.replace(m, converted)

    return re.sub('\s+', ' ', t)


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


def get_main_action(imperative_sentence, actions):
    """
    Extracts the main action from an imperative sentence.

    Args:
        imperative_sentence: Imperative sentence to extract from. 
        actions: List of verbs in the imperative sentence.

    Returns:
        String representing the main action.
    """
    if not actions:
        return ''

    main_action = [actions[0]]
    doc = nlp(imperative_sentence.lower())
    for token in doc:
        if token.text == main_action[0]:
            for child in token.children:
                if child.dep_ in ['dobj']:
                    main_action.append(child.text)
            break
    return ' '.join(main_action)


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


def extract_tools(sentence, ingredients, name):
    """
    Extracts kitchen tools from sentence.

    Args:
        sentence: Sentence to extract from.
        ingredients: List of ingredients for recipe.
        name: Name of recipe.

    Returns:
        List of strings representing tools used in this sentence.
    """
    NON_TOOLS = ['mins', 'gas', 'heat', 'secs', 'it']
    indirect_objects = get_indirect_objects(sentence)
    tools = []
    for obj in indirect_objects:
        if obj in NON_TOOLS or obj in name.lower():
            continue
        if any(ingredient.is_similar(obj) for ingredient in ingredients):
            continue
        tools.append(obj)

    doc = nlp(sentence.lower())
    i = 0
    tool_compounds = []
    for tool in tools:
        while doc[i].text != tool:
            i += 1

        token = doc[i]

        compound = []
        for child in token.children:
            if child.dep_ == 'compound' or child.dep_ == 'nmod' or child.dep_ == 'amod':
                compound.append(child.text.lower())
        compound.append(token.text.lower())
        tool_compounds.append(' '.join(compound))

        i += 1

    return tool_compounds


def extract_time_parameters(sentence):
    """
    Extracts time parameters from sentence.

    Args:
        sentence: Sentence to extract from.

    Returns:
        Dictionary with mapping from action verb to time parameters.
    """
    doc = nlp(sentence)

    time_entities = []
    for ent in doc.ents:
        if ent.label_ == 'TIME':
            time_entities.append(ent.text.lower())

    doc = nlp(sentence.lower())
    i = 0
    actions = []
    for ent in time_entities:
        word_to_find = ent.split()[-1]

        while doc[i].text != word_to_find:
            i += 1

        token = doc[i]

        while token.has_head() and token.head != token:
            if token.tag_ == 'VB':
                break
            token = token.head

        actions.append(token.text.lower())
        i += 1

    time_parameters = defaultdict(list)
    for ent, action in zip(time_entities, actions):
        time_parameters[action].append(ent)

    return time_parameters


def extract_temperature_parameters(sentence):
    """
    Extracts temperature parameters from sentence and standardizes temperature format in sentence.

    Args:
        sentence: Sentence to extract from.

    Returns:
        Dictionary with mapping from action verb to temperature parameters and processed sentence.
    """
    HEAT_LEVEL_KEYWORDS = ('low heat', 'medium heat',
                           'medium-high heat', 'meadium high heat', 'high heat')
    temperature_parameters = []
    lower_sentence = sentence.lower()

    for keyword in HEAT_LEVEL_KEYWORDS:
        if keyword in lower_sentence:
            temperature_parameters.append(keyword)

    while re.search('\d+c/\d+c fan/gas \d+', lower_sentence):
        m = re.search('\d+c/\d+c fan/gas \d+', lower_sentence).group()
        m_list = m.split('/')
        t, f, g = m_list[0].replace(
            'c', '°C'), m_list[1].replace('c', '°C'), m_list[2]
        param = ' or '.join((t, f, g))
        temperature_parameters.append(param)
        lower_sentence = lower_sentence.replace(m, '')
        start_index = sentence.lower().index(m)
        end_index = start_index + len(m)
        sentence = sentence[:start_index] + param + sentence[end_index:]
    while re.search('\d+c\/fan \d+c\/gas \d+', lower_sentence):
        m = re.search('\d+c\/fan \d+c\/gas \d+', lower_sentence).group()
        m_list = m.split('/')
        t, f, g = m_list[0].replace(
            'c', '°C'), m_list[1][4:].replace('c', '°C') + ' fan', m_list[2]
        param = ' or '.join((t, f, g))
        temperature_parameters.append(param)
        lower_sentence = lower_sentence.replace(m, '')
        start_index = sentence.lower().index(m)
        end_index = start_index + len(m)
        sentence = sentence[:start_index] + param + sentence[end_index:]
    while re.search('\d+°c\/fan\d+°c\/gas \d+', lower_sentence):
        m = re.search('\d+°c\/fan\d+°c\/gas \d+', lower_sentence).group()
        m_list = m.replace('c', 'C').split('/')
        t, f, g = m_list[0], m_list[1][3:] + ' fan', m_list[2]
        param = ' or '.join((t, f, g))
        temperature_parameters.append(param)
        lower_sentence = lower_sentence.replace(m, '')
        start_index = sentence.lower().index(m)
        end_index = start_index + len(m)
        sentence = sentence[:start_index] + param + sentence[end_index:]
    while re.search('\d+c\/\d+f\/gas \d+', lower_sentence):
        m = re.search('\d+c\/\d+f\/gas \d+', lower_sentence).group()
        m_list = m.split('/')
        t, g = m_list[0].replace('c', '°C'), m_list[2]
        param = ' or '.join((t, g))
        temperature_parameters.append(param)
        lower_sentence = lower_sentence.replace(m, '')
        start_index = sentence.lower().index(m)
        end_index = start_index + len(m)
        sentence = sentence[:start_index] + param + sentence[end_index:]
    while re.search('\d+°c\/\d+°f\/gas mark \d+', lower_sentence):
        m = re.search('\d+°c\/\d+°f\/gas mark \d+', lower_sentence).group()
        m_list = m.split('/')
        t, g = m_list[0].replace('c', 'C'), m_list[2].replace('mark ', '')
        param = ' or '.join((t, g))
        temperature_parameters.append(param)
        lower_sentence = lower_sentence.replace(m, '')
        start_index, end_index = sentence.lower().index(
            m), start_index + len(m)
        sentence = sentence[:start_index] + param + sentence[end_index:]
    while re.search('\d+°c', lower_sentence):
        m = re.search('\d+°c', lower_sentence).group()
        temperature_parameters.append(m.replace('c', 'C'))
        lower_sentence = lower_sentence.replace(m, '')
    while re.search('\d+°f', lower_sentence):
        m = re.search('\d+°f', lower_sentence).group()
        temperature_parameters.append(m.replace('f', 'F'))
        lower_sentence = lower_sentence.replace(m, '')

    return temperature_parameters, sentence


def extract_steps(raw_instructions, ingredients, name):
    """
    Extracts steps from recipe.

    Args:
        raw_instructions: String representing the instructions in the recipe.
        ingredients: List of ingredients for recipe.
        name: Name of recipe.

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
        main_action = get_main_action(raw_step, actions)
        step_ingredients = extract_ingredients_from_step(raw_step, ingredients)
        tools = extract_tools(raw_step, ingredients, name)
        temperature_parameters, processed_step = extract_temperature_parameters(
            raw_step)
        parameters = {
            'time': extract_time_parameters(raw_step),
            'temperature': temperature_parameters
        }
        steps.append(Step(processed_step, actions, main_action, step_ingredients,
                     tools, parameters))
    return steps


def extract_ingredients(raw_ingredients):
    """
    Extracts ingredients from recipe.

    Args:
        raw_ingredients: Dictionary with ingredient name mapped to quantity.

    Returns:
        List of ingredients.
    """
    for name, quantity in raw_ingredients.items():
        raw_ingredients[name] = preprocess(quantity)

    ingredients = []
    for name, quantity in raw_ingredients.items():
        quantity_word_list = quantity.split()
        ingredient = None

        if len(quantity_word_list) == 0:
            ingredient = Ingredient(
                name, Ingredient.NO_QUANTITY, Ingredient.COUNTABLE_MEASUREMENT, [])
        elif len(quantity_word_list) == 1:
            token = quantity_word_list[0]

            # Single token in format of '<QUANTITY>' where <QUANTITY> is an integer
            # i.e. Ingredient is countable
            if token.isnumeric():
                ingredient = Ingredient(
                    name, int(token), Ingredient.COUNTABLE_MEASUREMENT, [])

            # Single token in format of '<QUANTITY>' where <QUANTITY> is a float
            elif token.replace('.', '').isnumeric():
                ingredient = Ingredient(
                    name, float(token), Ingredient.COUNTABLE_MEASUREMENT, [])

            # Single token representing '<DESCRIPTOR>'
            elif token.isalpha():
                ingredient = Ingredient(
                    name, Ingredient.NO_QUANTITY, Ingredient.COUNTABLE_MEASUREMENT, [token])

            # Single token in format of '<QUANTITY><MEASUREMENT>'
            else:
                numeric_match = re.search('\d*\.?\d+', token)
                split_index = numeric_match.end() if numeric_match else len(token) + 1
                q = float(token[:split_index])
                m = token[split_index:]
                ingredient = Ingredient(name, q, m, [])

        else:
            parenthesis_matches = re.findall('\(.+\)', quantity)
            for match in parenthesis_matches:
                quantity = quantity.replace(match, '')

            quantity_word_list = quantity.split()

            # Multiple tokens in format of '<FRACTION_QUANTITY> <MEASUREMENT> <DESCRIPTORS>'
            # i.e. 1 1/2 oz
            if quantity_word_list[0].isnumeric() and re.search('\d\/\d', quantity_word_list[1]):
                fraction_token = quantity_word_list[1]
                numerator_match = re.search('\d', fraction_token)
                split_index = numerator_match.end()
                numerator, denominator = float(fraction_token[:split_index]), float(
                    fraction_token[split_index + 1:])
                q = float(quantity_word_list[0]) + \
                    round(numerator / denominator, 2)

                m = quantity_word_list[2] if len(
                    quantity_word_list) >= 3 else Ingredient.COUNTABLE_MEASUREMENT
                d = ' '.join(quantity_word_list[3:]).split(' and ') if len(
                    quantity_word_list) >= 4 else []
                d = list(map(lambda s: s.strip(), d))
                ingredient = Ingredient(name, q, m, d)

            elif quantity_word_list[0].replace('.', '').isnumeric():
                q = (int(quantity_word_list[0])
                     if quantity_word_list[0].isnumeric()
                     else float(quantity_word_list[0]))

                doc = nlp(quantity)

                # Multiple tokens in format of '<QUANTITY> <DESCRIPTORS>'
                if doc[1].pos_ in ['ADJ', 'ADV', 'VERB']:
                    d = ' '.join(quantity_word_list[1:]).split(' and ') if len(
                        quantity_word_list) >= 2 else []
                    d = list(map(lambda s: s.strip(), d))
                    ingredient = Ingredient(
                        name, q, Ingredient.COUNTABLE_MEASUREMENT, d)

                # Multiple tokens in format of '<QUANTITY> <MEASUREMENT> <DESCRIPTORS>'
                else:
                    m = quantity_word_list[1]
                    d = ' '.join(quantity_word_list[2:]).split(' and ') if len(
                        quantity_word_list) >= 3 else []
                    d = list(map(lambda s: s.strip(), d))
                    ingredient = Ingredient(name, q, m, d)

            # Multiple tokens that are all descriptors
            else:
                d = quantity.split(' and ')
                d = list(map(lambda s: s.strip(), d))
                ingredient = Ingredient(
                    name, Ingredient.NO_QUANTITY, Ingredient.COUNTABLE_MEASUREMENT, d)

        ingredients.append(ingredient)
    return ingredients


def compile_tools(steps):
    """
    Compiles the tools used from each step.

    Args:
        steps: Steps to compile from.

    Returns:
        Dictionary with mapping from tool to step index that the tool is used in.
    """
    tools = {}
    for i, step in enumerate(steps):
        for tool in step.get_tools():
            if tool in tools.keys():
                continue
            tools[tool] = i
    return tools


def extract(raw_recipe):
    """
    Extracts name, steps with annotations, ingredients, and tools from the recipe.

    Args:
        raw_recipe: Dictionary representing recipe to extract from.

    Returns:
        Tuple of recipe name, steps with annotations, ingredients, and tools.
    """
    name = raw_recipe['name']
    ingredients = extract_ingredients(raw_recipe['ingredients'])
    steps = extract_steps(raw_recipe['instructions'], ingredients, name)
    tools = compile_tools(steps)

    return name, steps, ingredients, tools
