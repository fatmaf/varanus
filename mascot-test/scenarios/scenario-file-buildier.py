import random
import json
from trace_representation import *

def to_assertion(scenarioName, trace):

    assert_start = "assert MASCOT_SAFETY_SYSTEM  :[has trace]: <"
    assert_end = ">"

    assert_check = assert_start
    trace_list = trace.to_list()
    print "trace_list", trace_list

    for i in range(len(trace_list)):
    # the str is key here. My editor produced unicode which became
    # a unicode object, not a str object so the assertion parsing broke.
        event = str(trace_list[i])
        print "event", event
        print "event type" , type(event)
        assert_check = assert_check + event
        if i < len(trace_list)-1:
            assert_check = assert_check + ", "
        elif i == len(trace_list)-1:
            assert_check = assert_check + assert_end

    f = open(scenarioName+"-assertion.csp", "w")

    f.write(assert_check)
    f.close()

def _split_and_convert_event(eventStr):

    print(eventStr)
    eventList = eventStr.split(":")

    system_event = eventList[0]
    #This gets rid of the extra quotes around the event name
    system_event = system_event.strip("\"")
    print(system_event)
    print(type(system_event))
    fdr_event =  str(eventMap[str(system_event)])

    param = eventList[1]

    return fdr_event, param


def build_scenario_0(traceLength):

    velocity_events = ['"velocity":100', '"velocity":500']

    trace = Trace(Event("system_init"))

    f = open("scenario0-"+str(traceLength)+"-stress.json", "w")

    footswitch_bool = False
    velocity_num = 0


#traceLength/10 because each of these loops produces 10 events (+ system_init for the csp file)
    for i in range(0,traceLength/10):
#This loop produces 10 events in the trace
#Both in the json file and in the csp file.
        footswitch_bool = not footswitch_bool
        footswitch = footswitch_events[footswitch_bool]

        fsEvent, fsParam = _split_and_convert_event(footswitch_events[footswitch_bool])
        newFSEvent = Event(fsEvent, fsParam)
        trace.add_event(newFSEvent)

        velocity = velocity_events[velocity_num]

        f.write("{"+ velocity +" , "+ footswitch +"}\n")


        for j in range(0,4):
            velocity_num = random.randint(-1, 1)
            velocity = velocity_events[velocity_num]

            velEvent, velParam = _split_and_convert_event(velocity)
            newVelEvent = Event(velEvent, velParam)
            trace.add_event(newVelEvent)
            speed_ok_event = Event("speed_ok", None)
            trace.add_event(speed_ok_event)

            f.write("{"+ velocity +" , "+ footswitch +"}\n")
            f.write("{"+ velocity +" , "+ footswitch +"}\n")

        footswitch_bool = not footswitch_bool
        footswitch = footswitch_events[footswitch_bool]

        fsEvent, fsParam = _split_and_convert_event(footswitch_events[footswitch_bool])
        newFSEvent = Event(fsEvent, fsParam)
        trace.add_event(newFSEvent)

        velocity = velocity_events[velocity_num]

        f.write("{"+ velocity +" , "+ footswitch +"}\n")


    f.close()

    to_assertion("scenario0-"+str(traceLength), trace)

def build_collecting_or_replaceing_tools_section(trace, fileHandle, velocity_events):
    """builds a trace of 20 low-speed, 'speed_ok' pairs with the footswitch set to false """

    footswitch = footswitch_events[0]
    for i in range(0,10):
        velocity_num = random.randint(-1, 1)
        velocity = velocity_events[velocity_num]

        velEvent, velParam = _split_and_convert_event(velocity)
        newVelEvent = Event(velEvent, velParam)
        trace.add_event(newVelEvent)
        speed_ok_event = Event("speed_ok", None)
        trace.add_event(speed_ok_event)

        fileHandle.write("{"+ velocity +" , "+ footswitch +"}\n")
        fileHandle.write("{"+ velocity +" , "+ footswitch +"}\n")

    return trace

def build_tiles_or_bolts_section(trace, fileHandle, velocity_events, footswitchUsed=False, unsafe_velocity_events=None):
    """ builds a trace of 50 events including velocity, 'speed_ok', and potentially footswitch changes.
        unsafeSpeeds says wether we might generate a speed too fast for the mode"""

    footswitch = footswitch_events[0]

    if unsafe_velocity_events != None:
        assert(type(unsafe_velocity_events) == type([]))

        for i in range(0,5):
            velocity_num = random.randint(-1, (len(velocity_events)-1))
            velocity = velocity_events[velocity_num]

            velEvent, velParam = _split_and_convert_event(velocity)
            newVelEvent = Event(velEvent, velParam)
            trace.add_event(newVelEvent)
            speed_ok_event = Event("speed_ok", None)
            trace.add_event(speed_ok_event)

            fileHandle.write("{"+ velocity +" , "+ footswitch +"}\n")
            fileHandle.write("{"+ velocity +" , "+ footswitch +"}\n")

        joined_velocity_events =  velocity_events.extend(unsafe_velocity_events)
        for j in range(0,20):
                velocity_num = random.randint(-1, (len(velocity_events)-1))
                velocity = velocity_events[velocity_num]

                velEvent, velParam = _split_and_convert_event(velocity)
                newVelEvent = Event(velEvent, velParam)
                trace.add_event(newVelEvent)
                speed_ok_event = Event("speed_ok", None)
                trace.add_event(speed_ok_event)

                fileHandle.write("{"+ velocity +" , "+ footswitch +"}\n")
                fileHandle.write("{"+ velocity +" , "+ footswitch +"}\n")

    else:
        for i in range(0,25):
            velocity_num = random.randint(-1, (len(velocity_events)-1))
            velocity = velocity_events[velocity_num]

            velEvent, velParam = _split_and_convert_event(velocity)
            newVelEvent = Event(velEvent, velParam)
            trace.add_event(newVelEvent)
            speed_ok_event = Event("speed_ok", None)
            trace.add_event(speed_ok_event)

            fileHandle.write("{"+ velocity +" , "+ footswitch +"}\n")
            fileHandle.write("{"+ velocity +" , "+ footswitch +"}\n")

    return trace

def build_scenario_1():
    """ Builds Scenario 1, where the Operator stays in hands on mode and the speed is fine """

    velocity_events = ['"velocity":100', '"velocity":500']
    trace = Trace(Event("system_init"))
    f = open("scenario1.json", "w")

    build_collecting_or_replaceing_tools_section(trace, f, velocity_events)

    build_tiles_or_bolts_section(trace, f, velocity_events)
    build_tiles_or_bolts_section(trace, f, velocity_events)
    build_tiles_or_bolts_section(trace, f, velocity_events)

    build_collecting_or_replaceing_tools_section(trace, f, velocity_events)

    f.close()

    to_assertion("scenario1", trace)

def build_scenario_2():
    """ Builds Scenario 2, where the Operator stays in hands on mode, but speed
    exceeds limit after completing some of the mission's tasks. """

    velocity_events = ['"velocity":100', '"velocity":500']

    trace = Trace(Event("system_init"))
    f = open("scenario2.json", "w")

    build_collecting_or_replaceing_tools_section(trace, f, velocity_events)

    build_tiles_or_bolts_section(trace, f, velocity_events)
    build_tiles_or_bolts_section(trace, f, velocity_events, unsafe_velocity_events=['"velocity":750'] )
    build_tiles_or_bolts_section(trace, f, velocity_events)

    build_collecting_or_replaceing_tools_section(trace, f, velocity_events)

    f.close()

    to_assertion("scenario2", trace)

if __name__ == '__main__':

    eventMap = {"velocity": "speed", "footswitch": "foot_pedal_pressed", "system_init" : "system_init"}
    footswitch_events = ['"footswitch": false', '"footswitch": true']

    #Parameter is the trace length
    #build_scenario_0(10)

    #build_scenario_1()

    #build_scenario_2()
