#! /bin/env python2.7
from datetime import tzinfo, timedelta, datetime
import logging
import time

from modules.core.props import Property, StepProperty
from modules.core.step import StepBase
from modules import cbpi

ZERO = timedelta(0)
HOUR = timedelta(hours=1)

class FixedOffsetTimezone(tzinfo):
    """Fixed offset in minutes east from UTC."""
    @classmethod
    def timezoneminutes_to_fixed_offset_string(cls, timezoneminutes):
        return cls.timezoneseconds_to_fixed_offset_string(timezoneminutes * 60)

    @staticmethod
    def timezoneseconds_to_fixed_offset_string(timezoneseconds):
        minutes = abs(timezoneseconds) % 3600 / 60
        hours = abs(timezoneseconds) / 60 / 60
        sign_bit = int(timezoneseconds < 0)
        sign_char = '-' if sign_bit else '+'
        return "UTC{sign_char}{hours:02d}:{minutes:02d}".format(
            sign_char=sign_char,
            hours=hours,
            minutes=minutes
        )

    @staticmethod
    def server_timezone_in_utc():
        return time.timezone == 0

    @classmethod
    def server_timezone_desc(cls):
        if cls.server_timezone_in_utc():
            return "Server timezone is in UTC, please set your local timezone here"
        else:
            server_timezone = time.timezone
            server_timezone_string = cls.timezoneseconds_to_fixed_offset_string(server_timezone)
            return "Server timezone is {0} and this will be used".format(
                server_timezone_string
            )

    @classmethod
    def fromSeconds(cls, seconds):
        return cls(seconds // 60)

    @classmethod
    def utcTimezone(cls):
        return cls(0)

    def __init__(self, offset):
        """
        Fixed offset in minutes east from UTC.

        offset is int (minutes)
        or string in form of 'UTC[-+]HH:MM'
        """
        if isinstance(offset, int):
            if offset >= 720 or offset <= -720:
                raise ValueError('Offset cannot be >= 720 minutes, try #fromSeconds if creating a fixed offset from seconds')

            self.__offset = timedelta(minutes = offset)
            self.__name = self.timezoneminutes_to_fixed_offset_string(offset)
            return


        if not offset.startswith("UTC"):
            raise ValueError("Please supply offset in minutes as integer or as string in form 'UTC[+-]HH:MM', received: %s" % offset)

        try:
            sign_char = offset[3]
            sign_multiplier = 1 if sign_char == '+' else -1
            hours = offset[4:6]
            minutes = offset[7:]
            self.__offset = timedelta(minutes=(int(minutes) + int(hours) * 60 * sign_multiplier))
            self.__name = offset
        except:
            raise ValueError("Please supply offset in minutes as integer or as string in form 'UTC[+-]HH:MM', received: %s" % offset)


    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return self.__name

    def dst(self, dt):
        return ZERO


SELECTABLE_TIMEZONES =[
    'UTC-11:30',
    'UTC-11:00',
    'UTC-10:30',
    'UTC-10:00',
    'UTC-09:30',
    'UTC-09:00',
    'UTC-08:30',
    'UTC-08:00',
    'UTC-07:30',
    'UTC-07:00',
    'UTC-06:30',
    'UTC-06:00',
    'UTC-05:30',
    'UTC-05:00',
    'UTC-04:30',
    'UTC-04:00',
    'UTC-03:30',
    'UTC-03:00',
    'UTC-02:30',
    'UTC-02:00',
    'UTC-01:30',
    'UTC-01:00',
    'UTC-00:30',
    'UTC+00:00',
    'UTC+00:30',
    'UTC+01:00',
    'UTC+01:30',
    'UTC+02:00',
    'UTC+02:30',
    'UTC+03:00',
    'UTC+03:30',
    'UTC+04:00',
    'UTC+04:30',
    'UTC+05:00',
    'UTC+05:30',
    'UTC+06:00',
    'UTC+06:30',
    'UTC+07:00',
    'UTC+07:30',
    'UTC+08:00',
    'UTC+08:30',
    'UTC+09:00',
    'UTC+09:30',
    'UTC+10:00',
    'UTC+10:30',
    'UTC+11:00'
]

NOTICE_DATE_FORMAT = '%-d %b %y, %-I:%M %p'

@cbpi.step
class AlarmClockStep(StepBase):
    mode = Property.Select("Mode", options=["disabled", "enabled"], description="If enabled then this step will block until after the set time.")

    timezone = Property.Select(
        "Timezone",
        options=SELECTABLE_TIMEZONES,
        description=FixedOffsetTimezone.server_timezone_desc()
    )
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
            end_timedelta = timedelta(
                hours=m_start_hour,
                minutes=m_start_minute
            )
            dt_utc_now = datetime.utcnow()

            if FixedOffsetTimezone.server_timezone_in_utc():
                try:
                    self._logger.info("AlarmClock: Trying to create user set timezone %s" % self.timezone)
                    local_timezone = FixedOffsetTimezone(self.timezone)
                except:
                    self._logger.info("AlarmClock: server is UTC and localtimezone is unset or invalid")
                    self.notify(
                        "Alarm clock not configured",
                        "Server is in UTC, please select a timezone in step configuration",
                        type="danger",
                        timeout=None
                    )
                    self.mode = "disabled"
                    return
            else:
                self._logger.info("AlarmClock: server is localtime, using that timezone")
                local_timezone = FixedOffsetTimezone.fromSeconds(time.timezone)

            self._logger.info("AlarmClock: localtime_timezone: %s" % local_timezone)
            dt_utc_now = dt_utc_now.replace(tzinfo=FixedOffsetTimezone.utcTimezone())
            dt_local_now = dt_utc_now.astimezone(local_timezone)

            self._logger.info("AlarmClock: starting time UTC: %s" % dt_utc_now)
            self._logger.info("AlarmClock: starting localtime: %s" % dt_local_now)
            add_days = 1 if self.start_time_is_tomorrow(dt_local_now, end_timedelta) else 0

            end_datetime_local = self.construct_end_date(
                dt_local_now,
                m_start_hour,
                m_start_minute,
                add_days,
            ).replace(tzinfo=local_timezone)

            self.end_datetime_utc = end_datetime_local.astimezone(FixedOffsetTimezone.utcTimezone())
            self._logger.info("AlarmClock: ending time in UTC: %s" % end_datetime_local)
            self._logger.info("AlarmClock: ending localtime: %s" % self.end_datetime_utc)

            self.notify("Alarm clock enabled", "Current server time is {current_time} and brewing will continue at {end_time}".format(
                current_time=dt_local_now.strftime(NOTICE_DATE_FORMAT),
                end_time=end_datetime_local.strftime(NOTICE_DATE_FORMAT)
            ), timeout=None)

            if self.force_off_at_start == "enabled":
                self.notify("Alarm clock enabled", "Turning pump and kettle off")
                self.actor_off(int(self.pump))
                self.set_target_temp(0, self.kettle)

    @staticmethod
    def start_time_is_tomorrow(dt_now, end_timedelta):
        now_timedelta = timedelta(
            hours=dt_now.hour,
            minutes=dt_now.minute
        )
        return now_timedelta > end_timedelta

    @staticmethod
    def construct_end_date(dt_now, start_hour, start_minute, add_days):
        dt_end_day = dt_now + timedelta(days=add_days)
        return datetime(
            year=dt_end_day.year,
            month=dt_end_day.month,
            day=dt_end_day.day,
            hour=start_hour,
            minute=start_minute
        )

    def execute(self):
        if self.mode != "enabled":
            self._logger.info("AlarmClock: not enabled")
            self.notify("Alarm clock not enabled!", "Starting the next step")
            self.next()
            return

        if datetime.now(FixedOffsetTimezone.utcTimezone()) >= self.end_datetime_utc:
            self._logger.info("AlarmClock: time to wake up!")
            self.notify("Alarm clock triggered", "Starting the next step", timeout=None)
            self.next()
            return
