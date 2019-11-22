# -*- coding: utf-8 -*-
import csv
import nltk
from datetime import datetime
from collections import defaultdict
from nltk.stem.snowball import FrenchStemmer

ITEM_HEADERS = ["prix","marque","modele","date","annee","kilometrage","carburant","boite","temps",\
        "puissancef","place","couleur","adresse","loalld","typev","permis","annee_mois","puissanced","porte",\
        "lien","description","temps"]
CORPORA_HEADERS = ["date","lien","description"]
MONTH2SECOND = 2592001

def build_key(row): return row["date"] + chr (9774) + row["lien"]

def get_corpora(rows, download=True):
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    stemmer = FrenchStemmer()
    stop_words = set()
    if download: nltk.download('stopwords')
    stop_words.update(tuple(nltk.corpus.stopwords.words('french')))

    corpora = defaultdict(list)
    for row in rows:
        splitted = row["description"].lower().split(chr(9774))
        token = []
        for words in splitted:
            token += tokenizer.tokenize(words)
        corpora[build_key(row)]\
            = [stemmer.stem(word) for word in token if not word in list(stop_words)]
    return corpora

def write_corpora(corpora, filename, headers, mode='a'):
    with open(filename, mode, newline="", encoding='utf-8') as file:
        data = csv.DictWriter(file,fieldnames=headers)
        if mode == 'w': data.writeheader()
        for k, v in corpora.items():
            splitted = k.split(chr(9774))
            data.writerow({"date":splitted[0], "lien":splitted[1], "description":convert_to_string(v)})

def convert_to_string(token):
    size = len(token)
    if size == 0: return ""
    res = token[0]
    if size > 1:
        for word in token[1:]:
            res += "," + word
    return res

"""
stats, freq = dict(), dict()
s.translate(str.maketrans(string.punctuation,rrr))
    freq[k] = fq = nltk.FreqDist(v)
    stats[k] = {'total': len(v), 'unique': len(fq.keys())}
"""

# manage sets

def csv2list(filename):
    res = []
    with open(filename,encoding='utf-8') as file:
        data = csv.DictReader(file)
        for row in data:
            res.append(row)
    return res

def list2csv(rows, filename, headers, mode='a'):
    with open(filename,mode='w',encoding='utf-8') as file:
        data = csv.DictWriter(file,fieldnames=headers)
        if mode == 'w': data.writeheader()
        data.writerows(rows)

def list2dict(rows, dc):
    for row in rows:
        dc[build_key(row)] = 0

def inter_n_diff(dc, rows):
    inter, diff = [], []
    for row in rows:
        if build_key(row) in dc:
            inter.append(row)
        else:
            diff.append(row)
    return inter, diff

# manage temps

def get_datetime(dt):
    st = dt.split("/")
    return datetime(int(st[0]),int(st[1]),int(st[2]),int(st[3]),int(st[4]))

def update_temps(row):
    time = datetime.now() - get_datetime(row["date"])
    row["temps"] = time.total_seconds()

def sort_temps(rows, temps):
    overwaiting, stillwaiting = [], []
    for row in rows:
        update_temps(row)
        if row["temps"] < temps:
            stillwaiting.append(row)
        else:
            overwaiting.append(row)
    return overwaiting, stillwaiting
