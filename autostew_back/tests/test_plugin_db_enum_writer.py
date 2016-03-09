import json
from unittest import mock

import requests
from django.test import TestCase

from autostew_back.gameserver.server import Server, UnmetPluginDependency
from autostew_back.plugins import db_enum_writer, db
from autostew_back.tests.mocks import FakeApi
from autostew_back.tests.test_assets.settings_no_plugins import SettingsWithoutPlugins
from autostew_web_enums.models import FuelUsageDefinition, SessionAttributeDefinition, MemberAttributeDefinition, \
    ParticipantAttributeDefinition
from autostew_web_session.models import VehicleClass, Vehicle, Livery, Track


class TestEnumWriter(TestCase):
    def test_dependency(self):
        api = FakeApi()
        settings = SettingsWithoutPlugins()
        settings.plugins = [db_enum_writer]
        with mock.patch.object(requests, 'get', api.fake_request):
            self.assertRaises(UnmetPluginDependency, Server, settings, False)

    def test_deletion(self):
        FuelUsageDefinition(name='FOO', ingame_id=1337).save(True)
        self.assertEqual(FuelUsageDefinition.objects.count(), 1)
        db_enum_writer._clear_enums()
        self.assertEqual(FuelUsageDefinition.objects.count(), 0)

    def test_creation(self):
        def check_enums():
            self.assertEqual(
                len(lists['response']['attributes/session']['list']),
                SessionAttributeDefinition.objects.count()
            )
            self.assertEqual(
                len(lists['response']['attributes/member']['list']),
                MemberAttributeDefinition.objects.count()
            )
            self.assertEqual(
                len(lists['response']['attributes/participant']['list']),
                ParticipantAttributeDefinition.objects.count()
            )
            self.assertEqual(
                len(lists['response']['vehicle_classes']['list']),
                VehicleClass.objects.count()
            )
            self.assertEqual(
                len(lists['response']['vehicles']['list']),
                Vehicle.objects.count()
            )
            self.assertEqual(
                len(lists['response']['tracks']['list']),
                Track.objects.count()
            )
            # TODO add test for true enums
        api = FakeApi()
        settings = SettingsWithoutPlugins()
        settings.plugins = [db, db_enum_writer]
        with mock.patch.object(requests, 'get', api.fake_request):
            server = Server(settings, False)
            db_enum_writer._create_enums(server)
        with open('autostew_back/tests/test_assets/lists.json') as f:
            lists = json.load(f)
        check_enums()
        db_enum_writer.env_init(server)
        check_enums()