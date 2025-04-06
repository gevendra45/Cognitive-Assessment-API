import re

def texttoresults(text, dictionary):
    results = {category: 0 for category in dictionary.keys()}
    words = re.findall(r'\b\w+\b', text.lower())
    for word in words:
        for pattern, categories in dictionary.items():
            if word in set(categories):
                results[pattern] += 1

    return results