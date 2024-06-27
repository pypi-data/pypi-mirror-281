from enum import Enum


# TODO We should create this class automatically using Sql2Code
#TODO Please create this structure using database-mysql-local-package Sql2Code and write the command used here so we will add it to the GHA
class GenderEnum(Enum):
    MALE_EN = ('Male', 2)
    FEMALE_EN = ('Female', 1)
    NON_BINARY_EN = ('Non- Binary', 4)
    TRANSGENDER_EN = ('Transgender', 16)

    MALE_HE = ('זכר', 2)
    FEMALE_HE = ('נקבה', 1)
    NON_BINARY_HE = ('לא מוגדר', 4)
    TRANSGENDER_HE = ('טראנגנדר', 16)

    def __init__(self, title: str, id: int):
        self._title = title
        self._id = id

    @property
    def title(self):
        return self._title

    @property
    def id(self):
        return self._id