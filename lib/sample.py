from gdpr import GDPR

from gdpr.services.pdf_to_text_service import pdf_to_text_service
from gdpr.services.filename_from_path_service import filename_from_path_service
from gdpr.services.dispatch_background_logging_service import dispatch_background_logging_service

from gdpr.services.url_trees_from_sources_service import url_trees_from_sources_service
from gdpr.services.absolute_urls_from_tree_service import absolute_urls_from_tree_service
from gdpr.services.links_from_soup_service import links_from_soup_service

from gdpr.services.anti_patterns_for_article_service import anti_patterns_for_article_service

import datetime
import json
import requests
from bs4 import BeautifulSoup

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from gensim.models import Word2Vec

# --- new addition ---
# https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da
# https://spacy.io/models/en
import nltk
from pprint import pprint
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
#nltk.download() # 'averaged_perceptron_tagger'

from nltk.metrics.distance import edit_distance

import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm

from gdpr.services.summarized_text_service import summarized_text_service
from gdpr.policies import summary_policy

import os

#from striprtf.striprtf import rtf_to_text

nlp = en_core_web_sm.load()

def main():
    #logpath = '/tmp/gdpr.log'
    #dispatch_background_logging_service(logpath)

    now = datetime.datetime.now()
    data_path = '../data/{date}/'.format(date='09-25-2019') # prod: now.strftime("%m-%d-%Y")

    gdpr = GDPR()
    dpa = gdpr.get_dpa(GDPR.EU_MEMBER.HUNGARY)
    dpa.bulk_collect(data_path)

    """for root, _, files in os.walk(data_path):
        filename = files[0] if len(files) > 0 else None
        if filename is None:
            continue

        if filename.endswith('.rtf') is False:
            continue

        print('root:', root)

        with open(root + '/' + filename, 'rb') as f:
            rtf = f.read().decode('cp1252') # use the france.policies decoding policy
            text = rtf_to_text(rtf)
            with open(root + '/' + filename.split('.')[0] + '.txt', 'w') as outfile:
                outfile.write(text)"""

    """with open('../data/09-25-2019/GB/metropolitan-police-service-enforcement-notice---data-protection-act-1998action-weve-takenpdf-1.4mb/en.txt') as f:
        summary = f.read()
        cursor = 0
        for p in [p for p in summary.split('\n') if p]:
            for sent in nltk.sent_tokenize(p):
                print(str(cursor), ':', str(len(sent)))
                #with open('../data/09-25-2019/GB/metropolitan-police-service-enforcement-notice---data-protection-act-1998action-weve-takenpdf-1.4mb/sent0.txt', 'w') as outfile:
                #    outfile.write(sent)
                #break
                if len(sent) >= 80:
                    print(sent)
                cursor += 1
                #if cursor == 50:
                #    break"""

    """for (dirpath, dirnames, filenames) in os.walk('../data/09-25-2019'):
        if 'en.txt' in filenames:
            with open(dirpath + '/en.txt') as f:
                doc = f.read()

            with open(dirpath + '/en_summary.txt', 'w') as f:
                n_sentences = summary_policy.n_sentences()
                summary = summarized_text_service(doc, n_sentences)
                f.write(summary)"""

    """
    path = './modules/gdpr/assets/r-facebook-mpn-20181024.pdf'
    text = pdf_to_text_service(path)
    filename = filename_from_path_service(path)
    with open('./modules/gdpr/assets/' + filename + '.txt', 'w') as f:
        f.write(text)
    """

    #anti_patterns = anti_patterns_for_article_service("5.1b", delimiter='.')
    #print(anti_patterns)
    # make sense of log.
    # then delete log after session is over.

"""    with open('./modules/gdpr/assets/supported_authorities.json', 'r') as f:
        authorities = json.load(f)

    sources = authorities['GB']['sources']

    print("Building source urls as tree(s):")
    root_nodes = url_trees_from_sources_service(sources)
    print(root_nodes)

    print("Extracting absolute urls from the tree(s):")
    for node in root_nodes:
        print(absolute_urls_from_tree_service(node))

print('Extracting links from ico:')

url = 'https://ico.org.uk/action-weve-taken/enforcement?rows=1000000'
response = requests.request('GET', url)
html_doc = response.text

soup = BeautifulSoup(html_doc, 'html.parser')
links = links_from_soup_service(soup, target_element='.resultlist')
print(links)
print('Number of links extracted: {}'.format(len(links)))
print("-------------------------------------------------\n\n")"""

"""def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent"""

#from collections import Counter

#with open('./modules/gdpr/assets/r-facebook-mpn-20181024.txt', 'r') as f:
    #doc_str = f.read()
    #print(json.dumps(Counter(nltk.word_tokenize(doc_str)).most_common(), indent=4))
    # print(get_data_processor_service(doc_str))
    #sents = preprocess(doc_str)
    # grammar = 'NP: {<DT>?<JJ>*<NN>}' # the official grammar chunking
    # https://www.programcreek.com/python/example/91255/nltk.RegexpParser
    #grammar = "ENT: {<PESSOA>*}"

    #cp = nltk.RegexpParser(grammar)
    #cs = cp.parse(sents)
    # print(cs)
    # 'European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices'
    #nlp_doc = nlp(doc_str)
    #texts = [X.text for X in nlp_doc.ents]
    #print(json.dumps(Counter(texts).most_common(), indent=4))
    # pprint([(X.text, X.label_) for X in nlp_doc.ents])

    # source: https://spacy.io/api/annotation#named-entities
    #people = []
    #for X in nlp_doc.ents:
    #    if X.label_ == 'PERSON':
    #        people.append(X.text.lower())
    #people = list(set(people))

    #print(json.dumps(people, indent=4))

    #nlp = spacy.load("en_core_web_sm")

    # spacy.io example on their homepage
    # Process whole documents
    #text = doc_str

    #doc = nlp(text)

    # Analyze syntax
    #print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
    #print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

    # Find named entities, phrases and concepts
    #for entity in doc.ents:
    #    print(entity.text, entity.label_)

    # https://spacy.io/usage/training#training-simple-style

if __name__ == '__main__':
    main()
