def find_word_between(partition, word1, word2, user_word):
    pattern = fr'\b({word1}\b(?:(?!{word1}|{word2}).)*?\b{user_word}\b(?:(?!{word1}|{word2}).)*?\b{word2})\b'
    matches = partition.str.findall(pattern, re.IGNORECASE)
    return matches
