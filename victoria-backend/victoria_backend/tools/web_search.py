from langchain.agents import tool
from duckduckgo_search import DDGS

results = DDGS().text("python programming", max_results=10)
print(results)