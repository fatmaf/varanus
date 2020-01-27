from fdr_interface import FDRInterface
from system_interface import *
from event_converter import *
from rosmon_mascot_event_abstractor import *
import json

#"MASCOT_SAFETY_SYSTEM :[has trace]: <system_init>"
#"model/mascot-safety-system.csp"


class Monitor(object):
    """The main class of the program, controls the process """

    def __init__(self, model_path):
        self.fdr = FDRInterface()
        self.model_path = model_path
        self.fdr.load_model(self.model_path)

    def _run_offline_traces(self, log_path):
        system = OfflineInterface(log_path)

        trace_file = system.connect()

        for json_line in trace_file:
            trace = json.loads(json_line)
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
        eventMapper = ROSMonMascotEventAbstractor("event_map.json")

        # get the trace file
        trace_file = system.connect()

        # check the traces
        for json_line in trace_file:
            print json_line

            event = eventMapper.convert_to_internal(json.loads(json_line))

            print event

            trace = eventMapper.new_traces(event)

            print trace
            ###############

            result = self.fdr.check_trace(trace)
            print result

            if not result:
                system.close()
                return result

        return result


    def run_online(self, ip, port):

        eventMapper = MascotEventAbstractor("event_map.json")

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


            new_traces = eventMapper.new_traces(json.loads(data))

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

        return result


    def close(self):

        self.fdr.close()


mon = Monitor("model/mascot-safety-system.csp")
mon.run_offline_rosmon("../rosmon-test/rosmon-mascot-pass.json")
#mon._run_offline_traces("trace.json")
#mon.run_online('127.0.0.1', 5005)
mon.close()
