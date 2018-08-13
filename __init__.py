#! /bin/env python2.7
import datetime
import logging
import time

from modules.core.props import Property, StepProperty
from modules.core.step import StepBase
from modules import cbpi

@cbpi.step
class AlarmClockStep(StepBase):
    mode = Property.Select("Mode", options=["disabled", "enabled"], description="If enabled then this step will block until after the set time.")
    start_hour = Property.Select("Start Hour", options=list(range(23)))
    start_minute = Property.Select("Start Minute", options=list(range(0, 60, 5)))
    force_off_at_start = Property.Select("Force off at start", options=["disabled", "enabled"], description="If enabled then this step will switch off pump and set temp to 0 when it starts.")
    kettle = StepProperty.Kettle("Kettle")
    pump = StepProperty.Actor("Pump", description="Pump actor which gets switched off")

    def __init__(self, *args, **kwds):
        StepBase.__init__(self, *args, **kwds)
        self._logger = logging.getLogger(type(self).__name__)

    def init(self):
        if self.mode == "enabled":
            m_start_hour = int(self.start_hour)
            m_start_minute = int(self.start_minute)
            end_timedelta = datetime.timedelta(
                hours=m_start_hour,
                minutes=m_start_minute
            )
            dt_now = datetime.datetime.now()

            add_days = 1 if self.start_time_is_tomorrow(dt_now, end_timedelta) else 0

            self.end_datetime = self.construct_end_date(dt_now, m_start_hour, m_start_minute, add_days)

            self.notify("Alarm clock enabled", "Brewing will continue at %s" % self.end_datetime, timeout=None)

            if self.force_off_at_start == "enabled":
                self.notify("Alarm clock enabled", "Turning pump and kettle off")
                self.actor_off(int(self.pump))
                self.set_target_temp(0, self.kettle)
        else:
            self.notify("Alarm clock not enabled!", "Starting the next step")
            self.next()

    @staticmethod
    def start_time_is_tomorrow(dt_now, end_timedelta):
        now_timedelta = datetime.timedelta(
            hours=dt_now.hour,
            minutes=dt_now.minute
        )
        return now_timedelta > end_timedelta

    @staticmethod
    def construct_end_date(dt_now, start_hour, start_minute, add_days):
        dt_end_day = dt_now + datetime.timedelta(days=add_days)
        return datetime.datetime(
            year=dt_end_day.year,
            month=dt_end_day.month,
            day=dt_end_day.day,
            hour=start_hour,
            minute=start_minute
        )

    def execute(self):
        if self.mode != "enabled":
            self.notify("Alarm clock not enabled!", "Starting the next step")
            self.next()
            return

        if datetime.datetime.now() >= self.end_datetime:
            self.notify("Alarm clock triggered", "Starting the next step", timeout=None)
            self.next()
