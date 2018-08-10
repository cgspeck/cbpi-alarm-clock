import logging
import time

from modules import cbpi
from modules.core.controller import KettleController
from modules.core.props import Property

@cbpi.controller
class PIDSmartBoilWithPump(KettleController):

    mode = Property.Select("Mode", options=["disabled", "enabled"], description="If enabled then this step will block until after the set time.")
    start_hour = Property.Select("Start Hour", options=list(range(23)))
    start_minute = Property.Select("Start Minute", options=list(range(0, 60, 5)))

    def __init__(self, *args, **kwds):
        KettleController.__init__(self, *args, **kwds)
        self._logger = logging.getLogger(type(self).__name__)

    def stop(self):
        '''
        Invoked when the automatic is stopped.
        Normally you switch off the actors and clean up everything
        :return: None
        '''
        super(KettleController, self).stop()
        # self.heater_off()


    def run(self):
        enabled = self.mode == "enabled"
        while self.is_running():
            self._logger.debug("started")

            if enabled:
                self._logger.debug("alarm clock is enabled")
                self.start_time = time.time()
                self._logger.debug("start time: %s" % self.start_time)

                self.end_time = ...
                self._logger.debug("end time: %s" % self.start_time)

                while time.time() < self.end_time:
                    self._logger.debug("alarm clock sleeping")
                    self.sleep(10)
