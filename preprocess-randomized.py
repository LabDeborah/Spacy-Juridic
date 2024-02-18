import json
from os import listdir
from os.path import isfile, join
import spacy
from spacy.tokens import DocBin
from random import shuffle
import json

from TagCount import TagCount

nlp = spacy.blank("pt")


def get_dataset(path: str, dataset_size_percentage: int = None) -> list:
    files = [
        join(path, f)
        for f in listdir(path)
        if isfile(join(path, f)) and f != ".DS_Store"
    ]

    dataset_size: int

    if dataset_size_percentage is not None:
        dataset_size = round(len(files) * (dataset_size_percentage / 100))

    # Shuffle file paths, so every training is different
    shuffle(files)

    spacy_data = []

    # Opening JSON file
    if dataset_size_percentage is not None:
        for file in files[:dataset_size]:
            try:
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
                        spacy_data_items.append(
                            (item["start"], item["end"], item["type"])
                        )

                    spacy_data.append((data["source"], spacy_data_items))
                    aux_used_paths.append(file)
            except Exception as e:
                print(f"There was an error while trying to read {file}")
                print(f"Message: {e}")
    else:
        for file in list(set(files) - set(aux_used_paths)):
            try:
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
                        spacy_data_items.append(
                            (item["start"], item["end"], item["type"])
                        )

                    spacy_data.append((data["source"], spacy_data_items))
            except Exception as e:
                print(f"There was an error while trying to read {file}")
                print(f"Message: {e}")
    return spacy_data


TRAINING_SET_SIZE_PCT = 80

aux_used_paths = []

training_data_list = get_dataset("./dataset", TRAINING_SET_SIZE_PCT)
testing_data_list = get_dataset("./dataset")

# Tag count
training_tag_count = TagCount()
testing_tag_count = TagCount()

for training_item in training_data_list:
    tags = training_item[1]
    training_tag_count.count_tags(tags)

for testing_item in testing_data_list:
    tags = testing_item[1]
    testing_tag_count.count_tags(tags)

f = open("tag-count.txt", "a")
f.write(f"""training:
{training_tag_count.toJSON()}

testing:
{testing_tag_count.toJSON()}""")

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
