
""" Represents traces and event within the program """

class Event(object):
    """"Represents one CSP Event"""

    def __init__(self, channel, parameters = None):
        """ Constructs an event on the given channel communicating the given parameters """
        self.channel = str(channel)

        if parameters != None and type(parameters) != type([]):
            self.parameters = [parameters]
        else:
            self.parameters = parameters


    def to_fdr(self):

        fdr_string = self.channel
        print self.parameters
        if self.parameters != None:
            for p in self.parameters:
                fdr_string = fdr_string + "." + str(p)

        return fdr_string

class Trace(object):
    """ Represents a single CSP trace """

    def __init__(self, initial_trace = None):
        # starts as the empty trace
        if initial_trace == None:
            self.trace = []
        elif type(initial_trace) == type([]):
            self.trace = initial_trace
        else:
            self.trace=[initial_trace]

    def add_event(self, new_event):
        """ Adds an event to the trace """
        assert(new_event != None)

        self.trace.append(new_event)

    def to_list(self):
        """ Returns a list of the events in the trace """

        fdr_list = []
        for event in self.trace:
            fdr_list.append(event.to_fdr())

        return fdr_list




if __name__ == "__main__":

    e1 = Event("speed",100)
    e2 = Event("system_init")

    print e1.to_fdr()
    print e2.to_fdr()

    t1 = Trace()
    print t1.to_list()
    t1.add_event(e1)
    print t1.to_list()

    t2 = Trace(e2)
    print t2.to_list()
