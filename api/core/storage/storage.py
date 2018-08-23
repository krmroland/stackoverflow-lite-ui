from api.core.Utils import time_now, Fluent
from .relationships import HasMany, HasOne, Relationship
from api.core.db.query import DB


class Model:
    timestamps = True
    hidden = []

    def __init__(self, attributes={}):
        self.attributes = Fluent()
        self.is_persisted = False

    @classmethod
    def table_name(cls):
        return str(cls.__name__).lower()

    @classmethod
    def query(cls):
        return DB.table(cls.table_name())

    @classmethod
    def create(cls, attributes):
        # add timestamps
        model = cls(attributes)
        model._update_timestamps()
        model.attributes.update(id=cls.builder.insert(model.attributes))
        model.is_persisted = True
        return model

    def _update_timestamps(self):
        if not self.timestamps:
            return
        now = time_now()
        if self.created_at:
            self.attributes.update(dict(updated_at=now))
        self.attributes.update(dict(updated_at=now, created_at=now))

    def delete(self):
        if(not self.id):
            return False
        return self.builder().where(id=self.id).delete()

    def update(self, attributes):
        self.attributes(attributes)
        return self.save()

    def save(self):
        self._update_timestamps()
        if self.is_persisted:
            self.builder().where(id=self.id).update(self.attributes)
            return self.attributes
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
        return cls.builder.find(id)

    @classmethod
    def find_or_fail(cls, id):
        return cls.builder().find_or_fail(id)

    @classmethod
    def where(cls, ** kwargs):
        return cls.builder().where(**kwargs)

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
        return cls.builder().get()
