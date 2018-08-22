from abc import ABC, abstractmethod


class DataType:
    pass


class Integer(DataType):
    pass


class String(DataType):
    pass


class TimeStamps(DataType):
    pass


class Table:
    def __init__(self, table_name):
        self.table_name = table_name

    def integer(self):
        return Integer(self)


class Migraion(ABC):
    def __init__(self):
        self.table = Table(self.table_name())

    @abstractmethod
    def up():
        pass

    @abstractmethod
    def table_name():
        pass

    @abstractmethod
    def down(self):
        pass
