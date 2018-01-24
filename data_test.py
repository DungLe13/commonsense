#!/usr/bin/env python3
"""
    data_test.py - Extract data from xml file + most simple method
    Author: Dung Le (dungle@bennington.edu)
    Date: 12/20/2017
"""

import xml.etree.ElementTree as ET
import re
import random
import nltk
from nltk.corpus import stopwords

tree = ET.parse('data/small-data.xml')
root = tree.getroot()

stop_words = set(stopwords.words('english'))
stop_words.remove('no')

with open('data/result-small-data.txt', 'w') as res_small:
    for instance in root:
        for question in instance[1]:
            for ans in question:
                if ans.attrib['correct'] == "True":
                    res = str(instance.attrib['id']) + ',' + str(question.attrib['id']) + ',' + str(ans.attrib['id'])
                    res_small.write(res + '\n')
res_small.close()

with open('data/predicted-small-data.txt', 'w') as pred_small:
    for instance in root:
        for question in instance[1]:
            ans_dict = {}
            for ans in question:
                ans_list = []
                answer = ans.attrib['text']
                normalized_ans = re.sub(r'[^\w\s]', '', answer)
                for w in nltk.word_tokenize(normalized_ans.lower()):
                    if w not in stop_words:
                        if w in nltk.word_tokenize(instance[0].text):
                            ans_list.append(w)
                ans_dict[ans.attrib['id']] = ans_list

            values = list(ans_dict.values())
            if len(values[0]) > len(values[1]):
                pred = str(instance.attrib['id']) + ',' + str(question.attrib['id']) + ',' + '0'
                pred_small.write(pred + '\n')
            elif len(values[0]) < len(values[1]):
                pred = str(instance.attrib['id']) + ',' + str(question.attrib['id']) + ',' + '1'
                pred_small.write(pred + '\n')
            else:
                pred = str(instance.attrib['id']) + ',' + str(question.attrib['id']) + ',' + str(random.randint(0, 1))
                pred_small.write(pred + '\n')
pred_small.close()
