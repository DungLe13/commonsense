## Commonsense Knowledge

Is it possible for an artificial intelligence system to understand commonsense knowledge through reading comprehension? And if yes, how can this knowledge be represented and interpreted in the task of question answering? These are the questions that this project, first described in *SemEval-2018 Task 11: Machine Comprehension using Commonsense Knowledge*, aims to answer.

All the files and folders are described below:

### Folders

- **literatures**: a collection of research papers about narrative event representation and commonsense knowledge database.
- **data**: three datasets (train-data, dev-data, test-data) are in .xml format, and can be downloaded from the competition on CodaLab (https://competitions.codalab.org/competitions/17184).
- **DeScript**: is a commonsense database (more information on this database can be found in a paper in **literature**.)
- **GloVe**: corpus construction, built from the scenerios in all three datasets; vocab construction and vector representation of words trained using GloVe word embedding (Pennington et al., 2014)

### Files

- **data_test.py**: get used to the dataset; a quick implementation of baseline method by comparing word appearances in answers and scenario, and using randomness for undecided answers.
- **scorer.py**: calculate the accuracy of the method against actual results (provided in train set and dev set only).
- **test_OMCS.py**: Open Mind Common Sense is another commonsense database by the MIT Lab; this file explores the coverage of this database against train data. More information on the database can be found in **literature** folder.
- **stanford_parser\_wrapper.py**: A Python wrapper for the usage of Stanford CoreNLP 3.8.0.
- **narrative_rep.py**: narrative representation of events chain (as described by Chambers and Jurafsky, 2008). Format: `protagonist(verb, dependency)`.
- **narrarive_rep2.py**: another approach on narrative representation. Format: (for transitive verb) `verb(predicate_1, predicate_2)`; (for intransitive verb) `verb(predicate_1)`