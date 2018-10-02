import unittest

import datetime

from modules.plugins.cbpi_alarm_clock import AlarmClockStep

class TestNormaliseActorBlacklist(unittest.TestCase):

    def test_blank_list(self):
        property_value = ""
        expected = []

        self.assertEqual(
            AlarmClockStep.normalise_actor_blacklist(property_value),
            expected
        )

    def test_single_item(self):
        property_value = "some actor"
        expected = ["some actor"]

        self.assertEqual(
            AlarmClockStep.normalise_actor_blacklist(property_value),
            expected
        )

    def test_multiple_items(self):
        property_value = "  some ACTOR,   some OTHER thing  "
        expected = ["some actor", "some other thing"]

        self.assertEqual(
            AlarmClockStep.normalise_actor_blacklist(property_value),
            expected
        )

if __name__ == '__main__':
    unittest.main()
