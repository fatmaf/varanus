# Varanus

This is a Runtime Monitoring application for checking programs against CSP specifications. It uses FDR in the back end to check that the incoming events are valid traces of the model

## The Name

Varanus is the genus of Monitor Lizards


## Generic Components

* command_line.py
 - Part of the FDR API, runs FDR
* event_abstractor.py (should be but currently isn't)
 - Reads the event_map.json file to convert incoming system events to model events
* fdr_interface.py
 - Part of the FDR API, slightly modified from the original version to connect the monitor to FDR
* system_interface.py
 - Connects the monitor to the system being monitored
* monitor.py (again, should be but needs tweaking)
 - Controls the monitoring program

## Specific Components

* event_map.json
  - Provide a map from the events the monitor will read from the system to the events inside the model.
