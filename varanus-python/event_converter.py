import json

""" Abstract class for the component that converts the system's status updates to a trace of events """

class EventConverter(object):

        def __init__(self):
            # this tracks the event trace(s)
            # Initialised assuiming we're desling with CSP
            self.event_traces = [ ["system_init"]  ]

        def convert_to_internal(self, input_map):
            """Converts a map of an input event (from the monitored system)
                into the internal representation of CSP events """
            pass

        def _decode(self, update):
            pass

        def new_traces(self, update):
            """ Returns the new trace(s) of the system after the update """

            new_events = self._decode(update)
            # This will be a list if we're sure of the order of events or a tuple if we're not
            print new_events

            if isinstance(new_events, tuple):
                #first split
                original_event_trace = self.event_traces[0]

                new_event_traces = []

                for new_event in new_events:

                    new_trace = original_event_trace + [new_event]

                    new_event_traces.append(new_trace)

                self.event_traces = new_event_traces
            elif len(self.event_traces) > 1 :
                #after first split

                if isinstance(new_events, tuple):
                    #split again
                    #TODO
                    pass
                else:
                    #just update what we have
                    for trace in self.event_traces:
                        trace.append(new_events)


            else:
                #no splits
                self.event_traces[0].append(new_events)

            return self.event_traces
