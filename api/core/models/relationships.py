from abc import ABC, abstractmethod
from inspect import stack
from api.core.exceptions import ModelException


class Relationship(ABC):
    def __init__(self, parent, child, parent_id, child_id):
        self.parent = parent
        self.child = child
        self.parent_id = parent_id
        if not child_id:
            child_id = "{}_id".format(parent._model_name())
        self.child_id = child_id
        self.child_key = stack()[2][3]

    @abstractmethod
    def _load_data(self):
        raise NotImplementedError

    def ensure_can_persist(self):
        pass

    def create(self, attributes):
        self.ensure_can_persist()
        attributes[self.child_id] = self.parent.attributes[self.parent_id]
        model = self.child(attributes)
        model.save()
        return model

    def children(self):
        return self.child.where({
            self.child_id: self.parent.attributes[self.parent_id]
        })

    def load(self):
        self.parent.attributes[self.child_key] = self._load_data()
        return self.parent


class HasMany(Relationship):
    def _load_data(self):
        return self.children().get()


class HasOne(Relationship):
    def _load_data(self):
        return self.children().first()

    def ensure_can_persist(self):
        # for one to one relationships, a single child should exist
        if self.children().count() > 0:
            raise ModelException(
                "{} already has a {}".format(
                    self.parent.table_name(),
                    self.child.table_name()
                ),
            )
