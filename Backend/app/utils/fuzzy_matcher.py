from rapidfuzz import fuzz, process


class FuzzyMatcher:
    def find_best_match(self, query: str, items: list):
        descriptions = [item.get("description", "") for item in items]
        matches = process.extract(query, descriptions, scorer=fuzz.token_sort_ratio, limit=3)

        # Top match and its score
        best_match_name, score, index = matches[0]

        if score < 70:
            # Return None and top 3 suggestions
            suggestions = [match[0] for match in matches]
            return None, suggestions

        # Return the best match and empty suggestions list
        return items[index], []
