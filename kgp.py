# Generic Libraries
import re
import pandas as pd # For creating dataframes of extracted information
import bs4
import requests
from tqdm import tqdm

# NLP Specific Libraries
import spacy
from spacy import displacy
nlp = spacy.load('en_core_web_sm')
from spacy.matcher import Matcher 
from spacy.tokens import Span 

# Libraries for displaying Knowledge Graph
import networkx as nx
import matplotlib.pyplot as plt


pd.set_option('display.max_colwidth', 200)
%matplotlib inline

def get_entities(sent):
  head_entity = ""
  candidate_entity = ""

  prv_tok_dep = ""    # dependency tag of previous token in the sentence
  prv_tok_text = ""   # previous token in the sentence

  prefix = ""
  
  for tok in nlp(sent):
    # If token is a punctuation mark then move on to the next token
    if tok.dep_ != "punct":

      # CHECK: token is a 'compound' or 'modifier' or 'attribute'
      if tok.dep_ == "compound" or tok.dep_.endswith("mod") or tok.dep_ == "attr":
        prefix = tok.text
        
        # If the previous word was also a 'compound' or 'modifier' or 'attribute', then add the current word to it
        if prv_tok_dep == "compound" or prv_tok_dep.endswith("mod") or prv_tok_dep == "attr":
          prefix = prv_tok_text + " " + tok.text
      
      # Assign head entity or, subject
      if tok.dep_.find("subj") == True:
        head_entity = prefix + " " + tok.text
        prefix = ""
        prv_tok_dep = ""
        prv_tok_text = ""      

      # Assign candidate entity or, object
      if tok.dep_.find("obj") == True:
        candidate_entity = prefix + " " + tok.text
      else:
        candidate_entity = prefix # In some cases the candidate entity is an 'attribute'
        
      # Update variables
      prv_tok_dep = tok.dep_
      prv_tok_text = tok.text

  return [head_entity.strip(), candidate_entity.strip()]

def get_relation(sent):

  doc = nlp(sent)

  # Matcher class object 
  matcher = Matcher(nlp.vocab)

  #define the pattern 
  pattern = [{'DEP':'ROOT'}, 
            {'DEP':'prep','OP':"?"},
            {'DEP':'agent','OP':"?"},  
            {'POS':'ADJ','OP':"?"}] 

  matcher.add("matching_1", None, pattern) 

  matches = matcher(doc)
  k = len(matches) - 1

  span = doc[matches[k][1]:matches[k][2]] 

  return(span.text)

entity_pairs = []

for i in tqdm(unstructured_text["sentence"]):
  entity_pairs.append(get_entities(i))

relations = [get_relation(i) for i in tqdm(unstructured_text['sentence'])]

source = [i[0] for i in entity_pairs]

target = [i[1] for i in entity_pairs]

kg_df = pd.DataFrame({'source':source, 'target':target, 'edge':relations})
kg_df.head(6)

# Construct knowledge graph over extracted information (dataframe)
KG = nx.from_pandas_edgelist(kg_df, "source", "target", 
                          edge_attr=True, create_using=nx.MultiDiGraph())

# Plot Knowledge Graph
plt.figure(figsize=(12,12))
pos = nx.spring_layout(KG)
nx.draw(KG, with_labels=True, node_color='lightgreen', edge_cmap=plt.cm.Blues, pos = pos)
plt.show()

