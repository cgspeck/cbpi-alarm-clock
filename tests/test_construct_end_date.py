import unittest

import datetime

from modules.plugins.cbpi_alarm_clock import AlarmClockStep

class TestConstructEndDate(unittest.TestCase):

    def test_ends_today(self):
        dt_now = datetime.datetime(year=2018, month=8, day=13, hour=6, minute=0)
        start_hour = 7
        start_minute = 30
        add_days = 0

        expected = datetime.datetime(year=2018, month=8, day=13, hour=7, minute=30)

        self.assertEqual(
            AlarmClockStep.construct_end_date(dt_now, start_hour, start_minute, add_days),
            expected
        )

    def test_ends_tomorrow(self):
        dt_now = datetime.datetime(year=2018, month=8, day=13, hour=20, minute=0)
        start_hour = 7
        start_minute = 30
        add_days = 1

        expected = datetime.datetime(year=2018, month=8, day=14, hour=7, minute=30)

        self.assertEqual(
            AlarmClockStep.construct_end_date(dt_now, start_hour, start_minute, add_days),
            expected
        )

    def test_ends_next_year(self):
        dt_now = datetime.datetime(year=2018, month=12, day=31, hour=20, minute=0)
        start_hour = 7
        start_minute = 30
        add_days = 1

        expected = datetime.datetime(year=2019, month=1, day=1, hour=7, minute=30)

        self.assertEqual(
            AlarmClockStep.construct_end_date(dt_now, start_hour, start_minute, add_days),
            expected
        )

if __name__ == '__main__':
    unittest.main()
