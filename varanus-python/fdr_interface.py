import os
import platform
import sys
import logging
varanus_logger = logging.getLogger("varanus")

""" Interface to FDR.
 FDR API Usage Example file that I've reused and edited.
Original file available at: https://cocotec.io/fdr/manual/_downloads/ffcc2113bd60df5a33677f5bbe5193da/command_line.py
"""

if platform.system() == "Linux":
    for bin_dir in os.environ.get("PATH", "").split(":"):

        fdr4_binary = os.path.join(bin_dir, "fdr4")
        if os.path.exists(fdr4_binary):

            real_fdr4 = os.path.realpath(os.path.join(bin_dir, "fdr4"))

            #Added by Matt Luckcuck 2019-08-21

            #Take the fdr4 real dir, go up two steps...
            upone = os.path.split(real_fdr4)
            uptwo = os.path.split(upone[0])

            #... join with lib and append to path
            sys.path.append(os.path.join(uptwo[0], "lib"))
            #hasta lasanga don't get any on ya
            break
elif platform.system() == "Darwin":
    for app_dir in ["/Applications", os.path.join("~", "Applications")]:
        if os.path.exists(os.path.join(app_dir, "FDR4.app")):
            sys.path.append(os.path.join(app_dir, "FDR4.app", "Contents", "Frameworks"))
            break
import fdr
from command_line import *


class FDRInterface(object):
    """Interfaces the monitor with FDR"""

    def __init__(self):
        fdr.library_init()

        self.session = fdr.Session()

    def load_model(self, modelPath):
        """Loads the csp model at modelPath into the current session"""

        assert(self.session != None)

        try:
            self.session.load_file(modelPath)

        except fdr.Error, e:
            varanus_logger.error(e)

    def _make_assertion(self, trace):
        #generate assert and dump it into the model
        assert_start = "MASCOT_SAFETY_SYSTEM  :[has trace]: <"
        assert_end = ">"

        varanus_logger.debug("type of trace: " + str(type(trace)))

        assert_check = assert_start
        trace_list = trace.to_list()
        varanus_logger.debug("trace_list: " + str(trace_list))

        for i in range(len(trace_list)):
            # the str is key here. My editor produced unicode which became
            # a unicode object, not a str object so the assertion parsing broke.
            event = str(trace_list[i])
            varanus_logger.debug("event: " + event)
            varanus_logger.debug("event type: " + str(type(event)))
            assert_check = assert_check + event
            if i < len(trace_list)-1:
                assert_check = assert_check + ", "
            elif i == len(trace_list)-1:
                assert_check = assert_check + assert_end

        return assert_check


    def check_trace(self, trace):
        """ parses the trace and executes it in the current session.
            returns True if the assertion passed or
            False if the assertion fails """

        assert(self.session != None)

        assertionString = self._make_assertion(trace)
        varanus_logger.debug("assertionString: "+ assertionString)

        parsedAssert = self.session.parse_assertion(assertionString)

        assertion = parsedAssert.result()

        assertion.execute(None)

        if assertion.passed():
            varanus_logger.info("+++ " + assertion.to_string() + " Passed +++")
            return True
        else:
            varanus_logger.info("+++ " +  assertion.to_string() + " Failed +++")

            for counterexample in assertion.counterexamples():
                describe_counterexample(self.session, counterexample, children=False)

            return False

    def new_session(self):
        self.session = fdr.Session()


    def close(self):
        fdr.library_exit()


if __name__ == '__main__':
    test_process = "a -> b -> SKIP"

    fdr_interface = FDRInterface()
    fdr_interface.load_model("test/simple.csp")

    # evaluate_process runs the process given, in the semantic model given, within the session
    LTS = fdr_interface.session.evaluate_process(test_process, fdr.SemanticModel_Traces, None)
    # Here is an example of calling a process deinfed in simple.csp
    # LTS = fdr_interface.session.evaluate_process("D(0)", fdr.SemanticModel_Traces, None)

    #The result of the evaluate_process call is a state machine
    machine = LTS.result()

    #We can get the root node of a state machine...
    root =  machine.root_node()

    # ... and print it's name (if it has one) ...
    print(fdr_interface.session.machine_node_name(machine, root))

    # ...and get the initial events out of the root node...
    initials_root = machine.initials(root)

    # but we have to uncompile them first.
    #Be careful, lots of methods return tuples, not just compiled events
    print(fdr_interface.session.uncompile_events(initials_root))

    alphabet = machine.alphabet(True)

    print(fdr_interface.session.uncompile_events(alphabet))

    #Transitions from the root node
    transitions_root = machine.transitions(root) # tuple
    for t in transitions_root:
        print(fdr_interface.session.uncompile_event(t.event())) #the event the transition represents
        dest = t.destination() # the node the transition goes to
        initials_dest =  machine.initials(dest) # and the events out of the destination
        print(fdr_interface.session.uncompile_events(initials_dest))
