from enum import Enum


class Role(Enum):
    Student = 'Student'
    librarian = 'librarian'


    @classmethod
    def choices(cls):
        return tuple((role.name, role.value) for role in cls)
    