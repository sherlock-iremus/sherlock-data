import rdflib
import pandas as pd
from pprint import pprint


df = pd.read_csv('thesaurus-mots-clefs.csv', delimiter=',')
df = df.dropna()
data = df.values.tolist()

pprint(data)