# Varanus

This is a Runtime Monitoring application for checking programs against CSP specifications. It uses FDR in the back end to check that the incoming events are valid traces of the model

## Generic Components

* `command_line.py`
 - Part of the FDR API, runs FDR
* `event_converter.py`
 - Reads the event_map.json file to convert incoming system events to model events
* `fdr_interface.py`
 - Part of the FDR API, slightly modified from the original version to connect the monitor to FDR
* `system_interface.py`
 - Connects the monitor to the system being monitored
* `monitor.py` (again, should be but needs tweaking)
 - Controls the monitoring program

## Specific Components

* `mascot_event_abstractor.py`
  - Implements EventConverter for Mascot

* `event_map.json`
  - Provide a map from the events the monitor will read from the system to the events inside the model.
