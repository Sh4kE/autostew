from unittest import mock
from unittest.mock import Mock

import requests
from django.test import TestCase

from autostew_back.gameserver.api import ApiConnector
from autostew_web_enums.models import DamageDefinition

simple_translation = [
    {'model_field': 'practice1_length', 'api_field': 'Practice1Length'}
]

enum_translation = [
    {'model_field': 'damage', 'api_field': 'DamageType', 'enum_model': DamageDefinition},
]


class NoApi:
    def _call(self):
        pass


class FakeModel:
    def __init__(self):
        self.practice1_length = None
        self.damage = None


class TestApiConnector(TestCase):
    def setUp(self):
        pass

    def test_simple_connector_pull(self):
        api_result = {'Practice1Length': 'foo'}
        fake_model = FakeModel()
        translator = ApiConnector(NoApi(), fake_model, simple_translation)
        translator.pull_from_game(api_result)
        self.assertEqual(fake_model.practice1_length, api_result['Practice1Length'])

    def test_simple_connector_push(self):
        api = NoApi
        api._call = Mock(return_value=None)
        fake_model = FakeModel()
        fake_model.practice1_length = 'foo'
        translator = ApiConnector(api, fake_model, simple_translation)
        translator.push_to_game('type')
        api._call.assert_called_once_with(
            'session/set_attributes',
            params={'type_Practice1Length': 'foo', 'copy_to_next': False}
        )

    def test_connector_pull_with_enum(self):
        api_result = {'DamageType': '2'}
        DamageDefinition.objects.create(name='foo', ingame_id=1)
        expected = DamageDefinition.objects.create(name='bar', ingame_id=2)
        fake_model = FakeModel()
        translator = ApiConnector(NoApi(), fake_model, enum_translation)
        translator.pull_from_game(api_result)
        self.assertEqual(fake_model.damage, expected)

    def test_connector_push_with_enum(self):
        api = NoApi
        api._call = Mock(return_value=None)
        fake_model = FakeModel()
        fake_model.damage = DamageDefinition.objects.create(name='bar', ingame_id=2)
        translator = ApiConnector(api, fake_model, enum_translation)
        translator.push_to_game('type')
        api._call.assert_called_once_with(
            'session/set_attributes',
            params={'type_DamageType': 2, 'copy_to_next': False}
        )
