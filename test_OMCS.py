#!/usr/bin/env python3
"""
    test_OMCS.py - Compare answer with text + finding relations from OMCS
    Author: Dung Le (dungle@bennington.edu)
    Date: 01/08/2017
"""

import xml.etree.ElementTree as ET
import re
import random
import nltk
import requests
from nltk.corpus import stopwords
from rake_nltk import Rake

tree = ET.parse('data/small-data.xml')
root = tree.getroot()

stop_words = set(stopwords.words('english'))
stop_words.remove('no')
r = Rake()

for instance in root:
    for question in instance[1]:
        print(question.attrib['text'])
        # Get keywords from question
        r.extract_keywords_from_text(question.attrib['text'])
        question_keywords = r.get_ranked_phrases()
        # print(question_keywords)
        
        ans_dict = {}
        ans_keywords_dict = {}
        for ans in question:
            ans_list = []
            answer = ans.attrib['text']
            # Get keywords from answer
            r.extract_keywords_from_text(answer)
            answer_keywords = r.get_ranked_phrases()
            ans_keywords_dict[ans.attrib['id']] = answer_keywords
            # print(answer_keywords)

            # Attempt 1: Normalized answer and check if the answer exists somewhere in the text
            # If yes, append the words in this answer into a list;  if not, the list will be empty
            # Each answer now has a list of words 
            normalized_ans = re.sub(r'[^\w\s]', '', answer)
            for w in nltk.word_tokenize(normalized_ans.lower()):
                if w not in stop_words:
                    if w in nltk.word_tokenize(instance[0].text):
                        ans_list.append(w)
            ans_dict[ans.attrib['id']] = ans_list

        values = list(ans_dict.values())
        # Compare the length of two lists of answers
        # Since all the stopwords have been removed, the list with higher length will be the answer
        if len(values[0]) > len(values[1]):
            pred = str(instance.attrib['id']) + ',' + str(question.attrib['id']) + ',' + '0'
            print(pred)
        elif len(values[0]) < len(values[1]):
            pred = str(instance.attrib['id']) + ',' + str(question.attrib['id']) + ',' + '1'
            print(pred)
        else:
            # Cannot determine which answer is correct
            # In this case, find the relations between a word in the question and a word in the answer
            print(question_keywords)
            ans1 = list(ans_keywords_dict.values())[0]
            ans2 = list(ans_keywords_dict.values())[1]
            print(ans1, ans2)
            
            for keyword in question_keywords:
                keyword.replace(" ", "_")
                if ans1:
                    for pos_ans in ans1:
                        pos_ans.replace(" ", "_")
                        url = "http://api.conceptnet.io/query?node=/c/en/{0}&other=/c/en/{1}".format(keyword, pos_ans)
                        obj = requests.get(url).json()
                        print('=== ANS 1 ===')
                        print(len(obj['edges']))

                if ans2:
                    for pos_ans in ans2:
                        pos_ans.replace(" ", "_")
                        url = "http://api.conceptnet.io/query?node=/c/en/{0}&other=/c/en/{1}".format(keyword, pos_ans)
                        obj = requests.get(url).json()
                        print('=== ANS 2 ===')
                        print(len(obj['edges']))
            
            # pred = str(instance.attrib['id']) + ',' + str(question.attrib['id']) + ',' + 'none'
            # print(pred)
