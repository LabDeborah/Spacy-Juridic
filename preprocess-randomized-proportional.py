import json
from os import listdir
from os.path import isfile, join
import spacy
from spacy.tokens import DocBin
from random import shuffle
import json

from TagCount import TagCount

nlp = spacy.blank("pt")


def map_items_by_tag(full_dataset: list):
    count = TagCount()
    count.count_tags(full_dataset)

    for item in full_dataset:
        with open(item) as json_file:
            data = json.load(json_file)
            for tag in data['items']:
                match tag['type']:
                    case 'NOT_HEARD':
                        count.result_collections['NOT_HEARD'].append(item)
                    case 'RENDERED_MOOT':
                        count.result_collections['RENDERED_MOOT'].append(item)
                    case 'SUSPENDED':
                        count.result_collections['SUSPENDED'].append(item)
                    case 'NOT_ENTERTAINED':
                        count.result_collections['NOT_ENTERTAINED'].append(item)
                    case 'GRANTED_TO_REVOKE':
                        count.result_collections['GRANTED_TO_REVOKE'].append(item)
                    case 'NOT_GRANTED':
                        count.result_collections['NOT_GRANTED'].append(item)
                    case 'GRANTED':
                        count.result_collections['GRANTED'].append(item)
                    case 'GRANTED_AND_INDICATE':
                        count.result_collections['GRANTED_AND_INDICATE'].append(item)
    return count

def get_dataset(path: str, training_size_percentage: int, testing_size_percentage: int) -> tuple:
    try:
        if (training_size_percentage + testing_size_percentage != 100):
            raise Exception('Dataset usage should be equal 100% (training + testing)')
        files = [
            join(path, f)
            for f in listdir(path)
            if isfile(join(path, f)) and f != ".DS_Store"
        ]

        training_data = []
        testing_data = []

        count = map_items_by_tag(files)

        for key in count.result_collections:
            items = count.result_collections[key]
            training_set_size = round(len(items) * (training_size_percentage / 100))

            training_data = [*training_data, *items[:training_set_size]]
            testing_data = [*testing_data, *items[training_set_size:]]

        print(set(training_data) & set(testing_data))

        return (training_data, testing_data)
    except Exception as e:
        print(f"Message: {e}")


TRAINING_SET_SIZE_PCT = 80
TESTING_SET_SIZE_PCT = 20

(training_data_list, testing_data_list) = get_dataset("./dataset", TRAINING_SET_SIZE_PCT, TESTING_SET_SIZE_PCT)

# The DocBin will store the example documents
db = DocBin()
for text, annotations in training_data_list:
    doc = nlp(text)
    ents = []
    for start, end, label in annotations:
        span = doc.char_span(start, end, label=label)
        if label == "RATIO_DECIDENDI" or label == "SUBJECT":
            pass
        elif span == None:
            pass
        else:
            ents.append(span)
    doc.ents = ents
    db.add(doc)

# Do the same thing for the test dataset
db_test = DocBin()
for text, annotations in testing_data_list:
    doc = nlp(text)
    ents = []
    for start, end, label in annotations:
        span = doc.char_span(start, end, label=label)
        if label == "RATIO_DECIDENDI" or label == "SUBJECT":
            pass
        elif span == None:
            pass
        else:
            ents.append(span)
    doc.ents = ents
    db_test.add(doc)

# Save the training dataset to the spacy format
db.to_disk("./train.spacy")
db_test.to_disk("./dev.spacy")
