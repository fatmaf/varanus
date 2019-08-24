from fdr_interface import FDRInterface
import json

#"MASCOT_SAFETY_SYSTEM :[has trace]: <system_init>"
#"model/mascot-safety-system.csp"


class Monitor(object):

    def __init__(self, model_path):
        self.fdr = FDRInterface()
        self.model_path = model_path
        self.fdr.load_model(self.model_path)

    def run_offline(self, log_path):
        trace_file = open("trace.json")

        for json_line in trace_file:
            trace = json.loads(json_line)

            result = self.fdr.check_trace(trace)
            print result

            if not result:
                trace_file.close()
                return result

        return result



    def close(self):

        self.fdr.close()


mon = Monitor("model/mascot-safety-system.csp")
mon.run_offline("trace.json")
