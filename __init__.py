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
    force_off_at_start = Property.Select("Force off at start", options=["disabled", "enabled"], description="If enabled then this step will switch off the coils and pump when it starts.")
    kettle = StepProperty.Kettle("Kettle")
    pump = StepProperty.Actor("Pump", description="Pump actor gets toogled")

    def __init__(self, *args, **kwds):
        StepBase.__init__(self, *args, **kwds)
        self._logger = logging.getLogger(type(self).__name__)

    def init(self):
        if self.mode == "enabled":
            abstract_end_time = datetime.timedelta(
                hours=int(self.start_hour),
                minutes=int(self.start_minute)
            )
            dt_now = datetime.datetime.now()
            abstract_now_time = datetime.timedelta(
                hours=dt_now.hour,
                minutes=dt_now.minute
            )

            # TODO: set the wakeup time
            if abstract_now_time > abstract_end_time:
                # actual end time is the next day
            else:
                # actual end time is today

            self.end_time = ...
            self.notify("Alarm clock enabled", "Brewing will continue at %s" % self.end_time, timeout=None)

            if self.force_off_at_start == "enabled":
                self.notify("Alarm clock enabled", "Turning pump and kettle off")
                self.actor_off(int(self.pump))
                self.set_target_temp(0, self.kettle)
        else:
            self.notify("Alarm clock not enabled!", "Starting the next step")
            self.next()

    def execute(self):
        if time.time() >= self.end_time:
            self.notify("Alarm clock triggered", "Starting the next step", timeout=None)
            self.next()
