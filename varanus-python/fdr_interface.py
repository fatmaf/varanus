import os
import platform
import sys

""" Interface to FDR. Based on: https://www.cs.ox.ac.uk/projects/fdr/manual/api/api.html#getting-started-with-python"""

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
            print e

    def _make_assertion(self, trace):
        #generate assert and dump it into the model
        assert_start = "MASCOT_SAFETY_SYSTEM  :[has trace]: <"
        assert_end = ">"

        print type(trace)

        assert_check = assert_start

        for i in range(len(trace)):
            # the str is key here. My editor produced unicode which became
            # a unicode object, not a str object so the assertion parsing broke.
            event = str(trace[i])
            print event
            print type(event)
            assert_check = assert_check + event
            if i < len(trace)-1:
                assert_check = assert_check + ", "
            elif i == len(trace)-1:
                assert_check = assert_check + assert_end

        return assert_check




    def check_trace(self, trace):
        """ parses the trace and executes it in the current session.
            returns True if the assertion passed or
            False if the assertion fails """

        assert(self.session != None)

        assertionString = self._make_assertion(trace)
        print assertionString

        parsedAssert = self.session.parse_assertion(assertionString)

        assertion = parsedAssert.result()

        assertion.execute(None)

        if assertion.passed():
            print assertion.to_string() + " Passed"
            return True
        else:
            print assertion.to_string() + " Failed"

            for counterexample in assertion.counterexamples():
                describe_counterexample(self.session, counterexample, children=False)

            return False


    def close(self):
        fdr.library_exit()
