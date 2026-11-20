from ddgs import DDGS

results = DDGS().text(
    "founder of coca cola",
    max_results=3
)

print(list(results))
