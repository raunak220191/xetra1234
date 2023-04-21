import pandas as pd
from fuzzywuzzy import fuzz

def fuzzy_search_df(query, df):
    operators = {"AND", "OR"}
    clauses = query.split()
    operator = None
    results = []
    for clause in clauses:
        if clause in operators:
            operator = clause
        else:
            scores = [fuzz.token_sort_ratio(clause, text) for text in df['text']]
            max_score = max(scores)
            results.append(max_score)
    if operator == "AND":
        score = min(results)
    else:
        score = max(results)
    ranked_results = df.assign(similarity=results).sort_values('similarity', ascending=False)
    return ranked_results, score
