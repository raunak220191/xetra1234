import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

# Load the legal document
with open('legal_document.txt', 'r') as file:
    text = file.read()

# Tokenize the text into sentences
sentences = nltk.sent_tokenize(text)

# Extract noun phrases using named entity recognition
clauses = []
for sentence in sentences:
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    entities = nltk.chunk.ne_chunk(tagged)
    clauses.extend([ " ".join([token for token, pos in entity.leaves()]) 
                    for entity in entities if isinstance(entity, nltk.tree.Tree) and entity.label() == "NP"])

# Print the extracted clauses
print(clauses)
