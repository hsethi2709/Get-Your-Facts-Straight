#!/usr/bin/python3

"""
    parse.py

    MediaWiki API Demos
    Demo of `Parse` module: Parse content of a page

    MIT License
"""

import requests

def get_text_from_page(page):
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
    "action": "query",
    "titles": page,
    "prop": "extracts",
    "explaintest": 1,
    "exsentences":10,
    "format": "json"
    }   

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    return(DATA["query"])
