# from django.db import IntegrityError
# from django.test import TestCase
#
# from ..admin import EntityModelAdmin
# from ..models import Entity
# from .test_model import ModelAdminTest
#
#
# _name = 'Entity 1'
#
#
# def get_fields_entity():
#     return {
#         'name': _name
#     }
#
#
# def _create_entity():
#     entity = Entity.objects.create(**get_fields_entity())
#     return entity
#
#
# def get_or_create_entity():
#     if Entity.objects.exists():
#         entity = Entity.objects.first()
#     else:
#         entity = _create_entity()
#     return entity
#
#
# class EntityModelTest(TestCase):
#     def setUp(self):
#         self.entity = get_or_create_entity()
#
#     def test_create(self):
#         self.assertTrue(Entity.objects.exists())
#
#     def test_str(self):
#         self.assertEqual(_name, str(self.entity))
#
#     def test_unique_name(self):
#         with self.assertRaises(IntegrityError):
#             _create_entity()
#
#
# class EntityAdminTest(ModelAdminTest, TestCase):
#     ModelAdmin = EntityModelAdmin
#     Model = Entity
