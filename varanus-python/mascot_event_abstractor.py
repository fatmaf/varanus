import json
from event_converter import EventConverter

""" Abstracts the Mascot's status updates to a trace of events """

class MascotEventAbstractor(EventConverter):
    """Decodes JSON representation of system's status to produce a trace of events."""

    def __init__(self, event_map_path):
        super(MascotEventAbstractor, self).__init__()
        # event_map should be a json map path
        self.event_map = json.load(open(event_map_path))
        # TODO Defaults read in from file
        self. last_values = {"velocity": 0, "footswitch": False}


    def _decode_velocity(self, curr_velocity):
        """Decodes the change in velocity """

        new_event = self.event_map["velocity"]
        # This is an assumption that the speed reading was ok, because the system did it
        # Otherwise, FDR will reject the trace, which is what we want
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

    def _decode(self, update):

## Some of this needs to move to convert_to_internal for this implementation
## Decode should be working on the internal representation of CSP events
        curr_velocity = update["velocity"]
        curr_footswitch = update["footswitch"]

        new_events = None

        # This is hard-coded, needs to be extracted.
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
        else:
            # Assume this is just a speed update
            new_events = self._decode_velocity(curr_velocity)

        return new_events


    def convert_to_internal(self, input_map):
            """Converts a map of an input event (from the monitored system)
                into the internal representation of CSP events """
            pass

if __name__ == "__main__":
    ea = MascotEventAbstractor("event_map.json")

    data = (open("../mascot-test/dummy_mascot_data.json"))

    for update in data:
        update_map = json.loads(update)

        print ea.new_traces(update_map)
