# Alarm Clock Custom Step

[![Build Status](https://travis-ci.org/cgspeck/cbpi-alarm-clock.svg?branch=master)](https://travis-ci.org/cgspeck/cbpi-alarm-clock)

This allows you to set up your equipment and water in advance and have the process pause until a set time. It will automatically find your kettles and set them to 0, and find your actors and switch them off.

## Parameters

* `mode`: `enable` to activate the pause step, `disable` will skip
* `timezone`: you must select your local timezone from the dropdown. Only fixed a timezone is supported, you will need to adjust this for Daylight Savings.
* `start_hour` and `start_minute`: when to resume the brew
* `force_off_at_start`: if `enabled` will switch off pump and set target temp to 0 at start of paused period
* `actors_to_ignore`: a comma seperated list of actors to ignore while scanning if `force_off_at_start` is enabled

## Version History

2.0.0 - This version removes pump & kettle selection and instead
        uses the cache to find your brewing equipment.

1.0.0 - Initial release, control a single pump and kettle only.
