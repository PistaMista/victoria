from langchain.agents import tool
from duckduckgo_search import DDGS

@tool
def web_search(query: str):
    """Searches the web for the given search term,
    returning an array of dictionaries of the form:
    {
        'title': RESULT_TITLE,
        'href': LINK_TO_THE_WEBPAGE,
        'body': DESCRIPTION
    }
    
    When asked about a location, try searching in the language spoken
    at the place you are asked about.
    """
    results = DDGS().text(query, max_results=10)
    return results