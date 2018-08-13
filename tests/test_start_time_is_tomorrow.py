import unittest

import datetime

from modules.plugins.cbpi_alarm_clock import AlarmClockStep

class TestStartDateIsTomorrow(unittest.TestCase):

    def test_is_tomorrow(self):
        dt_now = datetime.datetime(year=2018, month=1, day=1, hour=5, minute=0)
        end_timedelta = datetime.timedelta(hours=4, minutes=0)

        self.assertTrue(
            AlarmClockStep.start_time_is_tomorrow(dt_now, end_timedelta)
        )

    def test_is_today(self):
        dt_now = datetime.datetime(year=2018, month=1, day=1, hour=5, minute=0)
        end_timedelta = datetime.timedelta(hours=6, minutes=0)

        self.assertFalse(
            AlarmClockStep.start_time_is_tomorrow(dt_now, end_timedelta)
        )

if __name__ == '__main__':
    unittest.main()
