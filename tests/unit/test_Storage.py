from unittest import TestCase
from collections import Iterable
from api.core.storage import Model, Storage
from api.core.exceptions import ModelException, ModelNotFoundException


class Contact(Model):
    pass


class Account(Model):
    pass


class User(Model):
    def contacts(self):
        return self.has_many(Contact)

    def account(self):
        return self.has_one(Account)


class TestStorage(TestCase):
    def setUp(self):
        self.attributes = dict(name="Roland", age="18")
        Storage._data = dict()

    def test_it_determines_the_table_name_based_on_the_class_name(self):
        self.assertEqual(User.table_name(), "user")

    def test_it_sets_model_attributes(self):
        user = User(self.attributes)
        self.assertDictEqual(user.attributes, self.attributes)

    def test_it_adds_an_id_attribute_on_creation(self):
        user = User.create(self.attributes)
        self.assertIn("id", user.attributes)

    def test_it_uses_model_name_as_the_key_in_the_storage_data(self):
        User.create(self.attributes)
        self.assertIn("user", Storage._data)

    def test_it_returns_saved_records(self):
        User.create(self.attributes)
        User.create(self.attributes)
        self.assertEqual(User.all().count(), 2)

    def test_it_updates_and_saves_a_non_existent_user(self):
        user = User()
        user.name = "Roland"
        user.age = 23
        user.save()
        self.assertEqual(User.all().count(), 1)

    def test_it_returns_true_on_saving_an_existing_user(self):
        user = User.create(self.attributes)
        user.name = "Rodgers"
        self.assertTrue(user.save())

    def test_it_fails_on_saving_a_false_id(self):
        user = User.create(self.attributes)
        user.name = "Rodgers"
        user.id = 100
        self.assertFalse(user.save())

    def test_it_removes_the_user_on_deletion(self):
        user = User.create(self.attributes)
        user.delete()
        self.assertEqual(User.all().count(), 0)

    def test_returns_true_on_model_deletion(self):
        user = User.create(self.attributes)
        self.assertTrue(user.delete())

    def test_returns_false_for_false_ids(self):
        user = User.create(self.attributes)
        user.id = 3232
        self.assertFalse(user.delete())

    def test_it_adds_a_user_id_to_account(self):
        user = User.create(self.attributes)
        balance = user.account().create(dict(balance=0))
        self.assertIn("user_id", balance.attributes)

    def test_it_persists_a_one_to_one_relationship(self):
        user = User.create(self.attributes)
        user.account().create(dict(balance=0))
        self.assertEqual(Account.all().count(), 1)

    def test_user_has_many_contacts(self):
        user = User.create(self.attributes)
        user.contacts().create(dict(phone="0703318890"))
        user.contacts().create(dict(phone="0772742016"))
        self.assertEqual(Contact.all().count(), 2)

    def test_it_loads_user_contacts(self):
        user = User.create(self.attributes)
        user.contacts().create(dict(phone="0703318890"))
        user.load("contacts")
        return self.assertIn("contacts", user.attributes)

    def test_it_loads_user_account(self):
        user = User.create(self.attributes)
        user.account().create(dict(balance=1000))
        user.load("account")
        return self.assertIn("account", user.attributes)

    def test_it_throws_an_exception_for_more_than_1_user_account(self):
        user = User.create(self.attributes)
        user.account().create(dict(balance=1000))

        self.assertRaises(
            ModelException,
            user.account().create,
            dict(balance=2000)
        )

    def test_it_filters_using_where(self):
        User.create(dict(name="Roland", age=22))
        User.create(dict(name="Richard", age=22))
        filtered = User.where(age=22)
        self.assertEqual(filtered.count(), 2)

    def test_it_filters_using_or_where(self):
        User.create(dict(name="Roland", age=22))
        User.create(dict(name="Richard", age=21))
        filtered = User.or_where(age=22, name="Richard")
        self.assertEqual(filtered.count(), 2)

    def test_model_collection_length(self):
        User.create(self.attributes)
        User.create(dict(name="Rodgers"))
        User.create(dict(name="Mariam"))
        self.assertEqual(len(User.all()), 3)

    def test_model_collection_is_iterable(self):
        User.create(self.attributes)
        self.assertIsInstance(iter(User.all()), Iterable)

    def test_it_first_or_fail_fails(self):
        self.assertRaises(ModelNotFoundException, User.all().first_or_fail)

    def test_it_first_or_fail_passes(self):
        User.create(self.attributes)
        self.assertEqual(1, len(User.all()))
