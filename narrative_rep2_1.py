#!/usr/bin/env python3
"""
    narrative_rep2_1.py - Narrative representation of event chain
    Author: Dung Le (dungle@bennington.edu)
    Date: 01/26/2017
"""

import xml.etree.ElementTree as ET
import spacy
import nltk
from stanford_parser_wrapper import StanfordCoreNLP

tree = ET.parse('data/train-data.xml')
root = tree.getroot()
parser = spacy.load('en')
'''
    Stanford CoreNLP 3.8.0 is used
    stanford-corenlp-full-2017-06-09 package can be downloaded at
    https://stanfordnlp.github.io/CoreNLP/history.html
    Open terminal, cd into the above downloaded package, and run the server (Java required):
    java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
'''
nlp = StanfordCoreNLP('http://localhost:9000')

modal_verbs = ['can', 'could', 'may', 'might', 'should', 'must', 'will', 'would']

# Supporting Function 1: Find phrasal verb
def get_phrasal_verb(list_deps, verb):
    for dep_dict in list_deps:
        if dep_dict['dep'] == 'compound:prt' and dep_dict['governorGloss'] == verb:
            phrasal_verb = dep_dict['governorGloss'] + '_' + dep_dict['dependentGloss']
            return phrasal_verb

'''
    For transitive verb: verb(arg_1, arg_2)
    For intransitive verb: verb(arg_1)
'''
for instance in root:
    sentences = nltk.sent_tokenize(instance[0].text)

    for sent in sentences:              
        # using Stanford CoreNLP to get dependency parsing
        output = nlp.annotate(sent, properties={
                    'annotators': 'tokenize,ssplit,pos,depparse,parse',
                    'outputFormat': 'json'})

        dependencies = output['sentences'][0]['enhancedPlusPlusDependencies']
        #print(dependencies)

        '''
            Narrative representation format for each sentence:
            an array of dictionaries, each contains three key 'verb', 'arg_1' and optional 'arg_2'
            e.g. [{'verb': 'went', 'arg_1': 'I', 'arg_2': None},
                  {'verb': 'flipped', 'arg_1': 'I', 'arg_2': 'light switch'}]
        '''
        narrative_array = []
        for dependency in dependencies:
            narrative_dict = {}
            # Find dependency of type nsubj to get arg_1
            # Set arg_2 to None temporarily
            if dependency['dep'] == 'nsubj' or dependency['dep'] == 'nsubj:xsubj':
                narrative_dict['verb'] = dependency['governorGloss']
                narrative_dict['arg_1'] = dependency['dependentGloss']
                narrative_dict['arg_2'] = None
                narrative_array.append(narrative_dict)
        #print(narrative_array)

        # For arg_2, go through the next 3 words after current verb
        # append any NN found into a string, and set it as arg_2
        # using spacy package to find POS
        sent_text = parser(sent)
        sent_pos = []
        for token in sent_text:
            sent_pos.append(str(token.pos_))
        
        words = nltk.word_tokenize(sent)
        for narr_dict in narrative_array:
            verb = narr_dict['verb']
            verb_pos = words.index(verb)
            argument_2 = ''

            # NOTE: verb_pos+4 is for the next 3 words; for the next 4 words, use verb_pos+5
            for i in range(verb_pos+1, min(len(words), verb_pos+4)):
                if sent_pos[i] == 'NOUN':
                    argument_2 = argument_2 + words[i] + ' '

            # Replace None with argument_2 in narrative_dict
            narr_dict['arg_2'] = argument_2.strip()

        # For each verb in each narrative dictionary, check for phrasal verb
        for narr_dict in narrative_array:
            verb = narr_dict['verb']
            phrasal_verb = get_phrasal_verb(dependencies, verb)

            if phrasal_verb:
                # Replace verb with phrasal_verb in narrative_dict
                narr_dict['verb'] = phrasal_verb
        print(narrative_array)
