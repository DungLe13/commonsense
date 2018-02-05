#!/usr/bin/env python3
"""
    narrative_rep3.py - Narrative representation of event chain
    Author: Dung Le (dungle@bennington.edu)
    Date: 01/31/2017
"""

import xml.etree.ElementTree as ET
import nltk
import spacy
import re
from stanford_parser_wrapper import StanfordCoreNLP

tree = ET.parse('data/train-data.xml')
root = tree.getroot()

parser = spacy.load('en')
nlp = StanfordCoreNLP('http://localhost:9000')
modal_verbs = ['can', 'could', 'may', 'might', 'should', 'must', 'will', 'would']

# Supporting functions
# Function 1: fill in the appropriate subject before the verb
def filling_subject(words, subject, verb):
    verb_pos = words.index(verb)

    if verb_pos >= 3:
        for i in range(verb_pos-1, verb_pos-4, -1):
            if words[i] == subject:
                return words
        words.insert(verb_pos, subject)
    return words

# Function 2: split a list into sublists, with separator = 'and'
def list_split(word_list):
    if 'and' in word_list:
        w_index = word_list.index('and')
        if word_list.count('and') == 1:
            return [word_list[0:w_index], word_list[w_index+1:len(word_list)]]
        else:
            return [word_list[0:w_index]] + list_split(word_list[w_index+1:len(word_list)])

# Function 3: check if len(str) >= 3 and str contains any VERB
def event_checker(event):
    if len(nltk.sent_tokenize(event)) < 3:
        return False
    else:
        # check if VERB existed
        event_text = parser(event)
        for token in event_text:
            if str(token.pos_) == 'VERB':
                return True
        return False

for instance in root:
    sentences = nltk.sent_tokenize(instance[0].text)
    phrases = []

    for sent in sentences:
        '''
        # Coreference Resolution using Stanford CoreNLP
        coref_output = nlp.annotate(sent, properties={
                    'annotators': 'coref',
                    'outputFormat': 'json'})
        print(coref_output['corefs'])
        '''
        # Using spacy to get POS; in this case, only care about VERB
        sent_text = parser(sent)
        sent_verbs = []

        for token in sent_text:
            if str(token.pos_) == 'VERB' and token.text not in modal_verbs:
                sent_verbs.append(token.text.lower())
        #print(sent_verbs)

        # Using Stanford CoreNLP to get the subject of each verb
        dep_output = nlp.annotate(sent, properties={
                        'annotators': 'tokenize,ssplit,pos,depparse,parse',
                        'outputFormat': 'json'})
        
        dependencies = dep_output['sentences'][0]['enhancedPlusPlusDependencies']

        words = nltk.word_tokenize(sent)
        for verb in sent_verbs:
            for dependency in dependencies:
                # Check if the subject of the verb in sent_verbs exists
                if (dependency['dep'] == 'nsubj' or dependency['dep'] == 'nsubj:xsubj') \
                   and dependency['governorGloss'] == verb:
                    # In the sent, check through the window of 3 words before verb,
                    # if found dependency['dependentGloss'], then pass
                    # if not, append dependency['dependentGloss'] before verb
                    words = filling_subject(words, dependency['dependentGloss'], verb)
        #print(words)

        '''
        To split a sentence containing multiple events into multiple sentences,
        with each containing exactly one event, I use the word 'and' as separator.
        However, need to check if a whole phrase (event) appear before and after 'and'
        '''
        words_splitted = list_split(words)
        if words_splitted:
            for words_arr in words_splitted:
                phrases.append(' '.join(words_arr))
        else:
            phrases.append(' '.join(words))
    #print(phrases)

    events = []
    for phrase in phrases:
        event = re.sub(r'([^\s\w]|_)+', '', phrase)
        events.append(event.strip())
    print(events)
