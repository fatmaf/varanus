import json
from trace_representation import Trace

""" Abstract class for the component that converts the system's status updates to a trace of events """

class EventConverter(object):

    def __init__(self):
        # this tracks the event trace(s)
        # Initialised assuiming we're dealing with CSP
        self.event_traces = [ Trace("system_init")  ]

    def convert_to_internal(self, input_map):
        """Converts a map of an input event (from the monitored system)
            into the internal representation of CSP events """
        pass

    def _decode(self, update):
        pass

    def new_traces(self, update):
        pass

    def convert_to_internal(self, input_map):
        """Converts a map of an input event (from the monitored system)
            into the internal representation of CSP events """
        pass
