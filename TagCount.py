import json


class TagCount:
    def __init__(self) -> None:
        self.TYPE_OF_APPEAL = 0
        self.SUBJECT = 0
        self.RATIO_DECIDENDI = 0
        self.NOT_HEARD = 0
        self.RENDERED_MOOT = 0
        self.SUSPENDED = 0
        self.NOT_ENTERTAINED = 0
        self.GRANTED_TO_REVOKE = 0
        self.NOT_GRANTED = 0
        self.GRANTED = 0
        self.GRANTED_AND_INDICATE = 0

        self.result_collections = {
            "NOT_HEARD": [],
            "RENDERED_MOOT": [],
            "SUSPENDED": [],
            "NOT_ENTERTAINED": [],
            "GRANTED_TO_REVOKE": [],
            "NOT_GRANTED": [],
            "GRANTED": [],
            "GRANTED_AND_INDICATE": [],
        }

    def count_tags(self, items: list):
        self.TYPE_OF_APPEAL = sum(1 for tag in items if tag[2] == "TYPE_OF_APPEAL")
        self.SUBJECT = sum(1 for tag in items if tag[2] == "SUBJECT")
        self.RATIO_DECIDENDI = sum(1 for tag in items if tag[2] == "RATIO_DECIDENDI")
        self.NOT_HEARD = sum(1 for tag in items if tag[2] == "NOT_HEARD")
        self.RENDERED_MOOT = sum(1 for tag in items if tag[2] == "RENDERED_MOOT")
        self.SUSPENDED = sum(1 for tag in items if tag[2] == "SUSPENDED")
        self.NOT_ENTERTAINED = sum(1 for tag in items if tag[2] == "NOT_ENTERTAINED")
        self.GRANTED_TO_REVOKE = sum(
            1 for tag in items if tag[2] == "GRANTED_TO_REVOKE"
        )
        self.NOT_GRANTED = sum(1 for tag in items if tag[2] == "NOT_GRANTED")
        self.GRANTED = sum(1 for tag in items if tag[2] == "GRANTED")
        self.GRANTED_AND_INDICATE = sum(
            1 for tag in items if tag[2] == "GRANTED_AND_INDICATE"
        )

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
