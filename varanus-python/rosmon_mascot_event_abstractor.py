import json
from event_converter import EventConverter
import logging
varanus_logger = logging.getLogger("varanus")

""" Abstracts the Mascot's status updates to a trace of events """

class ROSMonMascotEventAbstractor(EventConverter):
    """Decodes JSON representation of system's status to produce a trace of events."""

    def __init__(self, event_map_path):
        super(ROSMonMascotEventAbstractor, self).__init__()
        # event_map should be a json map path
        self.event_map = json.load(open(event_map_path))
        # TODO Defaults read in from file
        self. last_values = {"velocity": 0, "footswitch": False}

    def convert_to_internal(self, input_map):
        # input_map should be of the form
        # {"topic":topic_name, "data" : the_data, "time": the_timestamp}
        assert(input_map != None)

        channelName = self.event_map[str(input_map["topic"])]
        params = input_map["data"]
        # Ignoring time for now

        output_map = {}
        output_map["channel"] = str(channelName)
        output_map["params"] = params

        return output_map

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

    def _decode(self, update):

        varanus_logger.debug("update = " + update)

        new_events = str(update["channel"] + "." + str(update["params"]))

        return new_events

if __name__ == "__main__":
    ea = ROSMonMascotEventAbstractor("event_map.json")

    data = (open("../mascot-test/dummy_mascot_data.json"))

    for update in data:
        update_map = json.loads(update)

        varanus_logger.debug("new_traces = " +ea.new_traces(update_map) )
