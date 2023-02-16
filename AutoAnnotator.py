import spacy
from spacy.tokens import Doc, Span, Token

nlp = spacy.load('en_core_web_sm')

def my_annotation_function(doc):
    # Define your annotation function here
    # For example, find all occurrences of the word "apple" and return them as entities
    entities = []
    for match in re.finditer('apple', doc.text):
        start, end = match.start(), match.end()
        entities.append((start, end, 'FRUIT'))
    return entities

# Add the annotation function as a component to the Spacy pipeline
nlp.add_pipe(my_annotation_function, name='my_annotation_function', last=True)

# Process your input text
doc = nlp('I ate an apple and a banana for breakfast.')

# Access the annotations
for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)
