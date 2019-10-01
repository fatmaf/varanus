import json

""" Abstracts the system's status updates to a trace of events """

class EventAbstractor(object):
    """Decodes JSON representation of system's status to produce a trace of events."""

    def __init__(self, event_map_path):
        # event_map should be a json map path
        self.event_map = json.load(open(event_map_path))
        # TODO Defaults read in from file
        self. last_values = {"velocity": 0, "footswitch": False}

        # this tracks the event trace(s)
        self.event_traces = [ ["system_init"]  ]

    def _decode_velocity(self, curr_velocity):
        """Decodes the change in velocity """

        new_event = self.event_map["velocity"]
        new_event = str(new_event) + "." + str(curr_velocity) + ", speed_ok"

        self.last_values["velocity"] = curr_velocity

        return new_event

    def _decode_footswitch(self, curr_footswitch):
        """ Decodes the change in footswitch """

        new_event = self.event_map["footswitch"]

        new_event = str(new_event) + "." + str(curr_footswitch)
        if curr_footswitch:
            new_event = new_event + ", enter_hands_on_mode"
        else:
            new_event = new_event + ", enter_autonomous_mode"

        self.last_values["footswitch"] = curr_footswitch

        return new_event

    def decode(self, update):

        curr_velocity = update["velocity"]
        curr_footswitch = update["footswitch"]

        new_events = None

        if curr_velocity != self.last_values["velocity"] and curr_footswitch != self.last_values["footswitch"]:
            first_trace_fragment = self._decode_velocity(curr_velocity) + ", " + self._decode_footswitch(curr_footswitch)

            new_trace_fragment = self._decode_footswitch(curr_footswitch) + ", " +  self._decode_velocity(curr_velocity)

            new_events = (first_trace_fragment, new_trace_fragment)

        elif curr_velocity != self.last_values["velocity"]:
            # becomes an event
            new_events = self._decode_velocity(curr_velocity)

        elif curr_footswitch != self.last_values["footswitch"]:
            # becomes an event
            new_events = self._decode_footswitch(curr_footswitch)

        return new_events

    def new_traces(self, update):

        new_events = self.decode(update)

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


if __name__ == "__main__":
    ea = EventAbstractor("event_map.json")

    data = (open("../test/dummy_mascot_data.json"))

    for update in data:
        update_map = json.loads(update)

        print ea.new_traces(update_map)
