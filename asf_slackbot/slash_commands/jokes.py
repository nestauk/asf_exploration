# ==== IMPORTS ====

import requests
from random import choice

# ================

def get_a_joke(term):
    """Get a dad joke.

    Args:
        term (str): Joke will contain this term.

    Returns:
        joke (str): Joke including given term.
    """

    response_json = requests.get(
        "https://icanhazdadjoke.com/search",
        headers={"Accept": "application/json"},
        params={"term": term},
    ).json()

    results = response_json["results"]
    total_jokes = response_json["total_jokes"]

    if total_jokes >= 1:
        return choice(results)["joke"]
    else:
        return None
