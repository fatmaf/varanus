import json


class EventAbstractor(object):

    def __init__(self, event_map_path):
        # event_map should be a json map path
        self.event_map = json.load(open(event_map_path))
        # TODO Defaults read in from file
        self. last_values = {"velocity": 0, "footswitch": False}

        self.event_trace = ["system_init"]

    def decode(self, update):

        curr_velocity = update["velocity"]
        curr_footswitch = update["footswitch"]

        new_event = None

        if curr_velocity != self.last_values["velocity"]:
            # becomes an event

            new_event = self.event_map["velocity"]
            new_event = str(new_event) + "." + str(curr_velocity)

            self.last_values["velocity"] = curr_velocity

        elif curr_footswitch != self.last_values["footswitch"]:

            # becomes an event
            new_event = self.event_map["footswitch"]
            new_event = str(new_event) + "." + str(curr_footswitch)

            self.last_values["footswitch"] = curr_footswitch

        return new_event

    def new_trace(self, update):

        new_event = self.decode(update)
        self.event_trace.append(new_event)

        return self.event_trace


if __name__ == "__main__":
    ea = EventAbstractor("event_map.json")

    data = (open("../test/dummy_mascot_data.json"))

    for update in data:
        update_map = json.loads(update)

        print ea.new_trace(update_map)
