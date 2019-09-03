from fdr_interface import FDRInterface
from system_interface import *
import json

#"MASCOT_SAFETY_SYSTEM :[has trace]: <system_init>"
#"model/mascot-safety-system.csp"


class Monitor(object):

    def __init__(self, model_path):
        self.fdr = FDRInterface()
        self.model_path = model_path
        self.fdr.load_model(self.model_path)

    def _run_offline_traces(self, log_path):
        system = OfflineInterface(log_path)

        trace_file = system.connect()

        for json_line in trace_file:
            trace = json.loads(json_line)

            result = self.fdr.check_trace(trace)
            print result

            if not result:
                system.close()
                return result

        return result

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


    def close(self):

        self.fdr.close()


mon = Monitor("model/mascot-safety-system.csp")
#mon._run_offline_traces("trace.json")
mon.run_online('127.0.0.1', 5005)
mon.close()
