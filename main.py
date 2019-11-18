# -*- coding: utf-8 -*-
import csv
import nltk
from collections import defaultdict
from nltk.stem.snowball import FrenchStemmer

d = {}
with open("data.csv",encoding='utf-8') as file:
    data = csv.DictReader(file)
    data = list(data)
    for row in data:
        d[str(row["description"])] = str(row["modele"])

tokenizer = nltk.RegexpTokenizer(r'\w+')
stemmer = FrenchStemmer()
sw = set()
nltk.download('stopwords')
sw.update(tuple(nltk.corpus.stopwords.words('french')))

corpora = defaultdict(list)
for k,v in d.items():
    tmp = tokenizer.tokenize(k.lower())
    corpora[v] += [stemmer.stem(w) for w in tmp if not w in list(sw)]

stats, freq = dict(), dict()
for k, v in corpora.items():
    freq[k] = fq = nltk.FreqDist(v)
    stats[k] = {'total': len(v), 'unique': len(fq.keys())}
