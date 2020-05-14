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


def build_secnario_0():

    footswitch_events = ['"footswitch": false', '"footswitch": true']
    velocity_events = ['"velocity":100', '"velocity":500']

    trace = Trace(Event("system_init"))

    f = open("scenario0-stress.json", "w")

    footswitch_bool = False
    velocity_num = 0
    

#Set this loop to produce y*10 events, where range(x,y)
    for i in range(0,10):
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

    to_assertion("scenario0", trace)


if __name__ == '__main__':
 
    eventMap = {"velocity": "speed", "footswitch": "foot_pedal_pressed", "system_init" : "system_init"}

    build_secnario_0()

    
    
