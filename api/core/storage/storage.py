from api.core import Utils
from .relationships import HasMany, HasOne, Relationship
from api.core.exceptions import ModelNotFoundException


class Storage:
    _data = dict()

    @classmethod
    def clear(cls):
        cls._data = dict()

    @classmethod
    def insert(cls, table, attributes):
        existing = cls.get_table_data(table)
        new_id = len(existing) + 1
        attributes["id"] = new_id
        existing[new_id] = attributes
        cls._data[table] = existing

        return attributes

    @classmethod
    def update_or_create(cls, table, attributes):
        if "id" not in attributes:
            return cls.insert(table, attributes)
        existing = cls.get_table_data(table)
        id = attributes["id"]
        if id in existing:
            cls._data[table][id].update(attributes)
            return True
        return False

    @classmethod
    def get_table_data(cls, table):
        if table not in cls._data:
            cls._data[table] = {}
        return cls._data[table]

    @classmethod
    def remove(cls, table, id):
        existing = cls.get_table_data(table)
        if id in existing:
            del existing[id]
            cls._data[table] = existing
            return True
        return False

    @classmethod
    def where(cls, table, type, kwargs):
        results = []
        rows = cls.get_table_data(table).values()

        for row in rows:
            # for an and where clause we start with and true value
            passes = (type == "and")
            for key in kwargs:
                if type == "and":
                    passes = passes and (row.get(key, None) == kwargs[key])
                else:
                    passes = passes or (row.get(key, None) == kwargs[key])
            if passes:
                results.append(row)
        return results


class ModelCollection:
    def __init__(self, models=[]):
        self.models = models

    def count(self):
        return len(self.models)

    def __len__(self):
        return self.count()

    def to_json(self):
        return [model.to_json() for model in self.models]

    def first(self):
        try:
            return self.models[0]
        except IndexError as e:
            return None

    def __iter__(self):
        return iter(self.models)

    def __repr__(self):
        return str(self.models)


class Model:
    timestamps = True
    hidden = []

    @classmethod
    def table_name(cls):
        return str(cls.__name__).lower()

    def __init__(self, attributes={}):
        self.set_attributes(attributes)

    @classmethod
    def create(cls, attributes):
        # add timestamps
        model = cls(attributes)
        model._update_timestamps()
        model.set_attributes(
            Storage.insert(model.table_name(), model.attributes)
        )
        return model

    def _update_timestamps(self):
        if not self.timestamps:
            return
        now = Utils.time_now()
        if self.created_at:
            self._update_attributes(dict(updated_at=now))
        self._update_attributes(dict(updated_at=now, created_at=now))

    def delete(self):
        if(not self.id):
            return False
        return Storage.remove(self.table_name(), self.id)

    def update(self, attributes):
        self._update_attributes(attributes)
        self.save()

    def save(self):
        self._update_timestamps()
        return Storage.update_or_create(self.table_name(), self.attributes)

    def has_one(self, child, parent_id="id", child_id=None):
        return HasOne(self, child, parent_id, child_id)

    def has_many(self, child, parent_id="id", child_id=None):
        return HasMany(self, child, parent_id, child_id)

    def load(self, *args):
        for key in args:
            try:
                relationship = getattr(self, key)()
                if isinstance(relationship, Relationship):
                    relationship.load()
                else:
                    raise Exception("{} is not a valid relationship", key)
            except TypeError as e:
                raise Exception("{} is not a valid relationship", key)

    @classmethod
    def find(cls, id):
        return cls.where(id=int(id)).first()

    @classmethod
    def find_or_fail(cls, id):
        question = cls.find(id)
        if question:
            return question
        raise ModelNotFoundException(cls.table_name(), id)

    @classmethod
    def base_where(cls, type, *args, **kwargs):
        filters = kwargs
        if len(args) == 1 and isinstance(args[0], dict):
            filters = args[0]

        models = cls.hydrate(Storage.where(cls.table_name(), type, filters))
        return ModelCollection(models)

    @classmethod
    def where(cls, *args, **kwargs):
        return cls.base_where("and", *args, **kwargs)

    @classmethod
    def or_where(cls, *args, **kwargs):
        return cls.base_where("or", *args, **kwargs)

    @classmethod
    def hydrate(cls, models):
        return list(map(cls, models))

    def to_json(self):

        return {
            key: self.attributes[key]
            for key in self.attributes
            if (key not in self.hidden)
        }

    @classmethod
    def all(cls):
        models = cls.hydrate(Storage.get_table_data(cls.table_name()).values())
        return ModelCollection(models)

    def set_attributes(self, attributes):
        object.__setattr__(self, "attributes", attributes)

    def _update_attributes(self, attributes):
        self.attributes.update(attributes)

    def __getattr__(self, key):
        return self.attributes.get(key, None)

    def __getitem__(self, key):
        return self.attributes.get(key, None)

    def __setattr__(self, key, value):
        self.attributes[key] = value

    def __repr__(self):
        return str(self.attributes)

    def __setitem__(self, key, value):
        self.attributes[key] = value
