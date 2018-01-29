#!/usr/bin/env python3
"""
    narrative_rep.py - Narrative representation of event chain (based on Chambers and Jurafsky)
    Author: Dung Le (dungle@bennington.edu)
    Date: 01/21/2017
"""

import xml.etree.ElementTree as ET
import spacy
import json
from stanford_parser_wrapper import StanfordCoreNLP

tree = ET.parse('data/small-data.xml')
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

for instance in root:
    text = parser(instance[0].text)

    '''
        Protagonist dictionary: a dictionary with all the subjects (act as protagonists)
        in the text, along with their counts
        e.g. {'i': 12, 'it': 2}
        TODO: Coreference Resolution (what are 'it', 'they', 'he' referred to?)
    '''
    protagonist_dict = {}
    count = 1
    for token in text:
        if str(token.dep_) == 'nsubj' and str(token.pos_) == 'PRON':
            if str(token.text.lower()) not in protagonist_dict:
                protagonist_dict[str(token.text.lower())] = count
            else:
                count += 1
                protagonist_dict[str(token.text.lower())] = count

    # Only consider protagonists that appear more than 10 times in text
    protagonists = []
    for pronoun, count_val in protagonist_dict.items():
        if count_val >= 10:
            protagonists.append(pronoun)

    # If none of the protagonists appears more than 10 times,
    # only append the one with the highest count
    if not protagonists:
        for pronoun, count_val in protagonist_dict.items():
            if count_val == max(protagonist_dict.values()):
                protagonists.append(pronoun)

    '''
        Narrative dictionary: a dictionary with the key being protagonist and the value
        being an array that contains narrative event - tupple of (event, dependency)
        Stanford Parser with universal dependencies is used to obtain dependency from
        narrative event.
        e.g. {'i': [(went, subj), (flipped, subj), (see, subj), ...]}
    '''
    output = nlp.annotate(instance[0].text, properties={
                'annotators': 'tokenize,ssplit,pos,depparse,parse',
                'outputFormat': 'json'})

    '''
    NOTE: It might be helpful to have a search function that search through an array
          of dictionaries and find the correspond dependency['dep'].
    TODO: phrasal verb: e.g. we went out for dinner last night
          instead of event being 'went', it should be 'went_out'.
          (Hint: check if dependency['dep'] == 'compound:prt' exists, and instead of using
          narrative event as (went, subj), use (went_out, subj))
    TODO: modifying verb: e.g. I had to clean the house before going out
          instead of narrative events including all [(had, subj), (clean, subj), (going, subj)]
          it should be just [(clean, subj), (going, subj)] since 'had to' is modifying verb.
          (Hint: check if dependency['dep'] == 'xcomp' exists, and just use verb from
          dependency['dependentGloss'])
    TODO: negative statement (not) - adding 'neg' or 'pos' to narrative event accordantly
          (Hint: check for dependency['dep'] == 'neg' and dependency['governorGloss'])
    '''
    narrative_dict = {}
    for person in protagonists:
        events = []

        for i in range(len(output['sentences'])):
            all_deps = output['sentences'][i]['enhancedPlusPlusDependencies']

            for dependency in all_deps:
                if (dependency['dep'] == 'nsubj' or dependency['dep'] == 'nsubj:xsubj') and dependency['dependentGloss'].lower() == person:
                    narrative_event = (dependency['governorGloss'].lower(), 'subj')
                    events.append(narrative_event)
                elif dependency['dep'] == 'nsubjpass' and dependency['dependentGloss'].lower() == person:
                    narrative_event = (dependency['governorGloss'].lower(), 'obj')
                    events.append(narrative_event)
        #print(events)
        narrative_dict[person] = events
    print(narrative_dict)
