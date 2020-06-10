from fdr_interface import FDRInterface
from system_interface import *
from event_converter import *
from rosmon_mascot_event_abstractor import *
from mascot_event_abstractor import *
from trace_representation import Event, Trace
import json
import time

#"MASCOT_SAFETY_SYSTEM :[has trace]: <system_init>"
#"model/mascot-safety-system.csp"


class Monitor(object):
    """The main class of the program, controls the process """

    def __init__(self, model_path, event_map_path):
        self.fdr = FDRInterface()
        self.model_path = model_path
        self.fdr.load_model(self.model_path)
        self.eventMapper = MascotEventAbstractor(event_map_path)

    def _run_offline_traces_single(self, trace_path):
        """ Runs Varanus Offline, taking a single trace and sending it to FDR"""

        system = OfflineInterface(trace_path)
        trace_file = system.connect()
        trace = Trace()

        # Take a single line
        trace_line = trace_file.read()
        # parse to list
        event_list =json.loads(trace_line)
        print event_list

        # built trace from list
        for event in event_list:
            event = str(event)
            if event.find(".") == -1:
                channel, params = event, None
                new_event = Event(channel, params)
                trace.add_event(new_event)
            else:
                channel, params = event.split(".",1)
                new_event = Event(channel, params)
                trace.add_event(new_event)

        print trace

        # throw at FDR
        result = self.fdr.check_trace(trace)
        print result

        if not result:
            system.close()
            return result

        return result


# This Doesn't Work As Expected.
# Takes last event from each line and accumulates
# so we get a failure:
# MASCOT_SAFETY_SYSTEM
#    :[has trace]: <system_init, speed.1250, protective_stop, speed_ok> Failed
#Counterexample type: minimal acceptance refusing {safe_stop_cat1, }
#Obvious bullshit
    def _run_offline_traces(self, log_path):
        system = OfflineInterface(log_path)

        trace_file = system.connect()
        trace = Trace()

        for json_line in trace_file:
            if json_line == '\n':
                continue
            print json_line
            # No convert_to_internal here becasue it's for a file of traces
            event_list =json.loads(json_line)
            print event_list
            last_event = event_list[-1]
            print last_event

            if last_event.find(".") == -1:
                channel, params = last_event, None
                event = Event(channel, params)
                trace.add_event(event)
            else:
                channel, params = last_event.split(".",1)
                event = Event(channel, params)
                trace.add_event(event)

            print trace
            print type(trace)

            result = self.fdr.check_trace(trace)
            print result

            if not result:
                system.close()
                return result

        return result

    def run_offline_rosmon(self, log_path):
        system = OfflineInterface(log_path)

        # get the trace file
        trace_file = system.connect()
        trace = Trace()

        # check the traces
        for json_line in trace_file:
            if json_line == '\n':
                continue

            print json_line

            event_map = self.eventMapper.convert_to_internal(json.loads(json_line))

            print event_map
            #### THIS IS A BAD PLACE FOR THIS
            event = Event(event_map["channel"], event_map["params"])
            trace.add_event(event)
            print event

            if event_map["channel"] == "speed" :
                speed_ok = Event("speed_ok")
                trace.add_event(speed_ok)

            if event_map["channel"] == "foot_pedal_pressed" and event_map["params"] == True :
                mode_change = Event("enter_hands_on_mode")
                trace.add_event(mode_change)
            elif event_map["channel"] == "foot_pedal_pressed" and event_map["params"] == False :
                mode_change = Event("enter_autonomous_mode")
                trace.add_event(mode_change)

            ####


            #trace = eventMapper.new_traces(event)

            print trace
            ###############

            result = self.fdr.check_trace(trace)
            print result

            if not result:
                system.close()
                return result

        return result


    def run_online_traces_accumulate(self, ip, port):
        """Accepts traces (as json lists) transferred across a socket, checks each one in FDR. """

        ##connect to the system
        system = TCPInterface(ip, port)
        conn = system.connect()

        trace = Trace()

        # How to terminate? What is the end program signal?
        while 1:

            #get the data from the system
            data = conn.recv(1024)
            # break if it's empty
            if not data: break

            print("+++ Varanus received:" + data + " +++")
            conn.send(data)  # echo

            if data.find(".") == -1:
                channel, params = data, None
                new_event = Event(channel, params)
                trace.add_event(new_event)
            else:
                channel, params = data.split(".",1)
                new_event = Event(channel, params)
                trace.add_event(new_event)


            #Send to FDR
            result = self.fdr.check_trace(trace)

            print result


        pass

    def run_online(self, ip, port):


        ##connect to the system
        system = TCPInterface(ip, port)
        conn = system.connect()

        # How to terminate? What is the end program signal?
        while 1:

            #get the data from the system
            data = conn.recv(1024)
            # break if it's empty
            if not data: break

            print "received data:", data
            conn.send(data)  # echo


            new_traces = self.eventMapper.new_traces(json.loads(data))
            print new_traces

            results = []
            for new_trace in new_traces:
                print new_trace
                result = self.fdr.check_trace(new_trace)

                print result
                results.append(result)

            num_of_results = len(results)
            num_of_t = 0
            for r in results:
                if r: #is true
                    num_of_t = num_of_t + 1

            percentage_true = (float(num_of_t) / num_of_results) * 100

            if percentage_true == 0 :
                print "False (100%)"
            else:
                print "True (" + str(percentage_true) + "%)"
# TODO if we get to here: UnboundLocalError: local variable 'result' referenced before assignment

        return result

    def run_online_websocket(self, ip, port):
        """ Run as an Online Monitor, connecting via WebSocket """

        ##connect to the system
        system = WebSocketInterface(self.websockect_check_event, port)
        system.connect()
        #conn = system.connect()

    def websockect_check_event(self, client, server, message):
        """Called when a client sends a message, callback method"""
        print("Monitor got: ", message)

        json_original_message = json.loads(str(message))
        for key in json_original_message.keys():
            tmp =  json_original_message[key]
            del json_original_message[key]
            json_original_message[str(key)] = tmp

        json_reply_message = json_original_message

        new_traces = self.eventMapper.new_traces(json_original_message)
        print new_traces

        results = []
        for new_trace in new_traces:
            print new_trace
            result = self.fdr.check_trace(new_trace)

            print result
            results.append(result)

        num_of_results = len(results)
        num_of_t = 0
        for r in results:
            if r: #is true
                num_of_t = num_of_t + 1

        percentage_true = (float(num_of_t) / num_of_results) * 100

        if percentage_true == 0:
            print "False (100%)"
            json_reply_message["error"] = True
        else:
            print "True (" + str(percentage_true) + "%)"
            json_reply_message["error"] = False

        print("+++ Monitor Sending ", json_reply_message)
        server.send_message(client, str(json_reply_message))

        # if check_event(message):
        #     server.send_message(client, message)
        # else:
        #     message_dict['error'] = True
        #     message_dict['spec'] = property.PROPERTY
        #     server.send_message(client, json.dumps(message_dict))



    def close(self):

        self.fdr.close()
