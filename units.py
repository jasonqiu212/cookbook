"""This file provides operations and constants for handling imperial and metric units."""

IMPERIAL_TO_METRIC = {
    'tsp': (4.92892, 'ml'),
    'teaspoon': (4.92892, 'ml'),
    'teaspoons': (4.92892, 'ml'),

    'tbs': (14.7868, 'ml'),
    'tblsp': (14.7868, 'ml'),
    'tbsp': (14.7868, 'ml'),
    'tablespoon': (14.7868, 'ml'),
    'tablespoons': (14.7868, 'ml'),

    'cup': (236.588, 'ml'),
    'cups': (236.588, 'ml'),

    'oz': (28.3495, 'g'),
    'ounce': (28.3495, 'g'),
    'ounces': (28.3495, 'g'),

    'lb': (453.592, 'g'),
    'pound': (453.592, 'g'),
    'pounds': (453.592, 'g'),
}

METRIC_TO_IMPERIAL = {
    'ml': (0.067628, 'tbsp'),
    'milliliter': (0.067628, 'tbsp'),
    'milliliters': (0.067628, 'tbsp'),

    'l': (4.22675, 'cups'),
    'liter': (4.22675, 'cups'),
    'liters': (4.22675, 'cups'),

    'g': (0.035274, 'oz'),
    'gram': (0.035274, 'oz'),
    'grams': (0.035274, 'oz'),

    'kg': (2.20462, 'lb'),
    'kilogram': (2.20462, 'lb'),
    'kilograms': (2.20462, 'lb'),
}


def is_imperial(measurement):
    return measurement in IMPERIAL_TO_METRIC.keys()


def is_metric(measurement):
    return measurement in METRIC_TO_IMPERIAL.keys()


def convert_imperial_to_metric(quantity, measurement):
    """
    Converts imperial quantity to metric.

    Args:
        quantity: Numerical quantity.
        measurement: Imperial unit.

    Returns:
        Tuple representing converted quantity and metric unit.
        Original quantity and measurement, if given measurement is not imperial.
    """
    if not is_imperial(measurement):
        return quantity, measurement
    ratio, metric_measurement = IMPERIAL_TO_METRIC[measurement]
    return round(quantity * ratio, 2), metric_measurement


def convert_metric_to_imperial(quantity, measurement):
    """
    Converts metric quantity to imperial.

    Args:
        quantity: Numerical quantity.
        measurement: Metric unit.

    Returns:
        Tuple representing converted quantity and imperial unit.
        Original quantity and measurement, if given measurement is not metric.
    """
    if not is_metric(measurement):
        return quantity, measurement
    ratio, imperial_measurement = METRIC_TO_IMPERIAL[measurement]
    imperial_quantity = round(quantity * ratio, 2)

    if imperial_measurement == 'cups' and imperial_quantity == 1:
        imperial_measurement = 'cup'

    return imperial_quantity, imperial_measurement


def convert_fahrenheit_to_celsius(temperature):
    return round((temperature - 32) * (5 / 9), 2)


def convert_celsius_to_fahrenheit(temperature):
    return round((temperature * (9 / 5)) + 32, 2)
