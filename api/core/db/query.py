class DB:
    def __init__(self, table_name):
        self.table_name = table_name
        self.wheres = []

    @classmethod
    def table(cls, table):
        return DB(table)

    def base_where(self, filters, query_type):
        pass

    def where(self, filters):
        return self.base_where(filters, "and")

    def or_where(self, filters):
        return self.base_where(filters, "or")

    def get(self):
        pass

    def insert(self, values):
        raise Exception(values)

    def delete(self):
        pass

    def update(self):
        pass

    def order_by(self):
        pass
