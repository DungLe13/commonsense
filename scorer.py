#!/usr/bin/env python3
"""
    scorer.py - Scorer for Commonsense Knowledge task
    Author: Dung Le (dungle@bennington.edu)
    Date: 12/20/2017
"""

result_file = 'result-small-data.txt'
predicted_file = 'predicted-small-data.txt'

with open('data/{0}'.format(result_file), 'r') as fr:
    results = [line.strip() for line in fr]
fr.close()

with open('data/{0}'.format(predicted_file), 'r') as fd:
    predictions = [line.strip() for line in fd]
fd.close()

A = 0
for i in range(len(results)):
    if results[i] == predictions[i]:
        A += 1

print(A/len(results))
