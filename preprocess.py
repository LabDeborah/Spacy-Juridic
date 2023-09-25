import json
from os import listdir
from os.path import isfile, join
import spacy
from spacy.tokens import DocBin

nlp = spacy.blank("pt")


def get_dataset(path: str) -> list:
    files = [join(path, f) for f in listdir("./dataset") if isfile(join(path, f))]
    spacy_data = []

    # Opening JSON file
    for file in files:
        with open(file) as json_file:
            data = json.load(json_file)

            # Convert everything to spacy dataset format
            # e.g. ("Tokyo Tower is 333m tall.", [(0, 11, "BUILDING"), (15, 18, "HEIGHT")]),
            # In the end we should have a list of items like this example above, each one
            # representing one JSON file

            # Found items
            # e.g. [(0, 11, "BUILDING"), (15, 18, "HEIGHT")]
            spacy_data_items = []

            for item in data["items"]:
                spacy_data_items.append((item["start"], item["end"], item["type"]))

            spacy_data.append((data["source"], spacy_data_items))

    return spacy_data


training_data_list = get_dataset("./dataset")
testing_data_list = get_dataset("./dataset-test")

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
