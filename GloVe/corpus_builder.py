#!/usr/bin/env python3
"""
    corpus_builder.py - Building corpus from text in train, dev, and test sets 
    Author: Dung Le (dungle@bennington.edu)
    Date: 01/26/2017
"""

import xml.etree.ElementTree as ET

train_tree = ET.parse('../data/train-data.xml')
dev_tree = ET.parse('../data/dev-data.xml')
test_tree = ET.parse('../data/test-data.xml')

train_root = train_tree.getroot()
dev_root = dev_tree.getroot()
test_root = test_tree.getroot()

corpus = ''
for instance in train_root:
    corpus = corpus + instance[0].text + ' '

for instance in dev_root:
    corpus = corpus + instance[0].text + ' '

for instance in test_root:
    corpus = corpus + instance[0].text + ' '

with open('corpus.txt', 'wb') as corpus_file:
    corpus_file.write(corpus.encode('utf-8'))
corpus_file.close()
