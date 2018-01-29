#!/usr/bin/env python3
"""
    narrative_rep2.py - Narrative representation of event chain
    Author: Dung Le (dungle@bennington.edu)
    Date: 01/26/2017
"""

import xml.etree.ElementTree as ET
from stanford_parser_wrapper import StanfordCoreNLP

tree = ET.parse('data/small-data.xml')
root = tree.getroot()
'''
    Stanford CoreNLP 3.8.0 is used
    stanford-corenlp-full-2017-06-09 package can be downloaded at
    https://stanfordnlp.github.io/CoreNLP/history.html
    Open terminal, cd into the above downloaded package, and run the server (Java required):
    java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
'''
nlp = StanfordCoreNLP('http://localhost:9000')

'''
    For transitive verb: verb(predicate_1, predicate_2)
    For intransitive verb: verb(predicate_1)
'''
for instance in root:
    output = nlp.annotate(instance[0].text, properties={
                'annotators': 'tokenize,ssplit,pos,depparse,parse',
                'outputFormat': 'json'})
