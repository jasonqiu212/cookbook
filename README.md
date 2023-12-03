# CS 337: Cookbook

Team members:

- Jason Qiu
- Jiayi Xu
- Mingyu Jin

## Overview

## Getting Started

1. Clone this repository.

```
$ git clone git@github.com:jasonqiu212/cookbook.git
$ cd cookbook
```

2. Install the required Python packages from `requirements.txt`.

> We recommend using a [virtual environment](https://docs.python.org/3/library/venv.html) to run this project.

```
$ python3 -m pip install -r requirements.txt
```

3. Download the `spacy` package `en_core_web_md`.

```
$ python3 -m spacy download en_core_web_md
```

4. Start the chatbot.

```
$ python3 main.py
```

5. The chatbot provides 2 methods to fetch a recipe. To test the chatbot, choose option 1 and use the following test recipes:
   - https://www.themealdb.com/api/json/v1/1/lookup.php?i=52845
   - https://www.themealdb.com/api/json/v1/1/lookup.php?i=52806

```
$ Welcome to your interactive cookbook! How would you like to fetch your recipe from TheMealDB?
$ [1] URL to a specific recipe.
$ [2] Search recipe by name.
$ > 1
$ Got it! Please input the URL to a recipe on TheMealDB.
$ > https://www.themealdb.com/api/json/v1/1/lookup.php?i=52845
```

Congratulations! You have successfully initialized your cookbook.

## Acknowledgements

- [TheMealDB](https://www.themealdb.com/)
- Python libraries used: [spaCy](https://spacy.io/), [ftfy](https://ftfy.readthedocs.io/en/latest/#), [editdistance](https://pypi.org/project/editdistance/)
