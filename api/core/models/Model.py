from api.core.Utils import time_now
from api.core.db.query import DB
from .relationships import HasMany, HasOne, Relationship
from .collections import ModelCollection


class ModelEvents:
    def _creating(self):
        pass


class Model(ModelEvents):
    timestamps = True

    hidden = []

    def __init__(self, attributes=None):
        if not attributes:
            attributes = {}
        self.attributes = attributes

    def id(self):
        return self.attributes.get("id", None)

    @classmethod
    def table_name(cls):
        return cls._model_name()  # pragma: no cover

    @classmethod
    def _model_name(cls):
        return str(cls.__name__).lower()

    @classmethod
    def query(cls):
        return DB.table(cls.table_name())

    @classmethod
    def create(cls, attributes):
        attributes = cls._update_timestamps(attributes)
        model = cls(attributes)
        model._creating()
        model.attributes = cls.query().insert(attributes)
        return model

    @classmethod
    def _update_timestamps(cls, attributes):
        if not cls.timestamps:
            return attributes
        now = time_now()
        if attributes.get("created_at", None):
            attributes.update(dict(updated_at=now))
        else:
            attributes.update(dict(updated_at=now, created_at=now))
        return attributes

    def delete(self):
        if not self.id():
            return False
        return self.query().where({"id": self.id()}).delete()

    def update(self, attributes):
        self.attributes.update(attributes)
        return self.save()

    def save(self):
        self._update_timestamps(self.attributes)
        if self.id():
            self.attributes = self.query().where(
                {"id": self.id()}
            ).update(self.attributes)
            return self
        return self.create(self.attributes)

    def has_one(self, child, parent_id="id", child_id=None):
        return HasOne(self, child, parent_id, child_id)

    def has_many(self, child, parent_id="id", child_id=None):
        return HasMany(self, child, parent_id, child_id)

    def load(self, *args):
        for key in args:
            self._load_relation_ship(key)
        return self

    def _load_relation_ship(self, key):
        relationship = getattr(self, key)()
        if isinstance(relationship, Relationship):
            return relationship.load()
        raise Exception(f"{key} is not a valid relationship")

    @classmethod
    def find(cls, id):
        return cls.query().find(id)

    @classmethod
    def find_or_fail(cls, id):
        return cls(cls.query().find_or_fail(id))

    @classmethod
    def where(cls, *args, **kwargs):
        return cls.query().where(*args, **kwargs)

    @classmethod
    def where_in(cls, column_name, values):
        return cls.query().where_in(column_name, values)

    @classmethod
    def hydrate(cls, models):
        return [cls(model) for model in models]

    def to_json(self):

        return {
            key: self.attributes[key]
            for key in self.attributes
            if (key not in self.hidden)
        }

    @classmethod
    def all(cls):

        models = [cls(record) for record in cls.query().all()]

        return ModelCollection(models)

    def get_attribute(self, name):
        return self.attributes.get(name)

    def __repr__(self):
        return str(self.attributes)

    def __getitem__(self, key):
        return self.attributes.get(key)
