import requests


def page_lookup(topic):
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    SEARCHPAGE = topic

    PARAMS = {
    "action": "query",
    "format": "json",
    "list": "search",
    "srsearch": SEARCHPAGE
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    return DATA['query']['search']
#if DATA['query']['search'][0]['title'] == SEARCHPAGE:
#    print("Your search page '" + SEARCHPAGE + "' exists on English Wikipedia")
