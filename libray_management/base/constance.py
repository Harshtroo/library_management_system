from enum import Enum


class Role(Enum):
    student = 'student'
    librarian = 'librarian'


    @classmethod
    def choices(cls):
        return tuple((role.name, role.value) for role in cls)
    