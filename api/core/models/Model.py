from api.core.Utils import time_now
from api.core.db.query import DB
from .relationships import HasMany, HasOne, Relationship
from .collections import ModelCollection


class Model:
    timestamps = True

    hidden = []

    def __init__(self, attributes=None):
        if not attributes:
            attributes = {}
        self.attributes = attributes
        self.is_persisted = False

    def id(self):
        return self.attributes.get("id", None)

    @classmethod
    def table_name(cls):
        return cls._model_name()

    @classmethod
    def _model_name(cls):
        return str(cls.__name__).lower()

    @classmethod
    def query(cls):
        return DB.table(cls.table_name())

    @classmethod
    def create(cls, attributes):
        cls._update_timestamps(attributes)
        cls.query().insert(attributes)
        return cls(attributes)

    @classmethod
    def _update_timestamps(cls, attributes):
        if not cls.timestamps:
            return attributes
        now = time_now()
        if attributes.get("created_at", None):
            return attributes.update(dict(updated_at=now))
        return attributes.update(dict(updated_at=now, created_at=now))

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
            self.query().where({"id": self.id()}).update(self.attributes)
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

    def __repr__(self):
        return str(self.attributes)

    def __getitem__(self, key):
        return self.attributes.get(key)
