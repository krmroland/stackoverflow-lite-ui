class Query:
    def __init__(self, table_name):
        self.table_name = table_name

    @classmethod
    def table(cls, table):
        return Query(table)

    def where(self, keywords):
        pass

    def get(self):
        pass

    def insert(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass

    def order_by(self):
        pass
