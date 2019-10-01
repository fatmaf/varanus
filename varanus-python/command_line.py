import os
import platform
import sys

""" Another bit of FDR API that I've resued."""

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

def main():
    fdr.library_init()
    return_code = real_main()
    fdr.library_exit()
    sys.exit(return_code)

def real_main():
    if not fdr.has_valid_license():
        print "Please run refines or FDR4 to obtain a valid license before running this."
        return 1

    print "Using FDR version %s" % fdr.version()

    if len(sys.argv) != 2:
        print "Expected exactly one argument."
        return 1

    file_name = sys.argv[1];
    print "Loading %s" % file_name

    session = fdr.Session()
    try:
        session.load_file(file_name)
    except fdr.FileLoadError, error:
        print "Could not load. Error: %s" % error
        return 1

    # Check each of the assertions
    for assertion in session.assertions():
        print "Checking: %s" % assertion
        try:
            assertion.execute(None)
            print "%s, found %s counterexamples" % \
                ("Passed" if assertion.passed() else "Failed",
                    len(assertion.counterexamples()))

            # Pretty print the counterexamples
            for counterexample in assertion.counterexamples():
                describe_counterexample(session, counterexample)
        except fdr.InputFileError, error:
            print "Could not compile: %s" % error
            return 1

    return 0

"""
Pretty prints the specified counterexample to out.

Children switch added by Matt Luckcuck 5th Sept 2019
"""
def describe_counterexample(session, counterexample, children=True):
    # Firstly, just print a simple description of the counterexample
    if isinstance(counterexample, fdr.DeadlockCounterexample):
        t = "deadlock"
    elif isinstance(counterexample, fdr.DeterminismCounterexample):
        t = "determinism"
    elif isinstance(counterexample, fdr.DivergenceCounterexample):
        t = "divergence"
    elif isinstance(counterexample, fdr.MinAcceptanceCounterexample):
        t = "minimal acceptance refusing {"
        for event in counterexample.min_acceptance():
            t += str(session.uncompile_event(event)) + ", "
        t += "}"
    elif isinstance(counterexample, fdr.TraceCounterexample):
        t = "trace with event "+str(session.uncompile_event(
                counterexample.error_event()))
    else:
        t = "unknown"

    print "Counterexample type: "+t
    if children:
        print "Children:"

        # In order to print the children we use a DebugContext. This allows for
        # division of behaviours into their component behaviours, and also ensures
        # proper alignment amongst the child components.
        debug_context = fdr.DebugContext(counterexample, False)
        debug_context.initialise(None)

        for behaviour in debug_context.root_behaviours():
            describe_behaviour(session, debug_context, behaviour, 2, True)

"""
Prints a vaguely human readable description of the given behaviour to out.
"""
def describe_behaviour(session, debug_context, behaviour, indent, recurse):
    # Describe the behaviour type
    indent += 2;
    if isinstance(behaviour, fdr.ExplicitDivergenceBehaviour):
        print "%sbehaviour type: explicit divergence after trace" % (" "*indent)
    elif isinstance(behaviour, fdr.IrrelevantBehaviour):
        print "%sbehaviour type: irrelevant" % (" "*indent)
    elif isinstance(behaviour, fdr.LoopBehaviour):
        print "%sbehaviour type: loops after index %s" % (" "*indent, behaviour.loop_index())
    elif isinstance(behaviour, fdr.MinAcceptanceBehaviour):
        s = ""
        for event in behaviour.min_acceptance():
            s += str(session.uncompile_event(event)) + ", "
        print "%sbehaviour type: minimal acceptance refusing {%s}" % (" "*indent, s)
    elif isinstance(behaviour, fdr.SegmentedBehaviour):
        print "%sbehaviour type: Segmented behaviour consisting of:" % (" "*indent)
        # Describe the sections of this behaviour. Note that it is very
        # important that false is passed to the the descibe methods below
        # because segments themselves cannot be divded via the DebugContext.
        # That is, asking for behaviourChildren for a behaviour of a
        # SegmentedBehaviour is not allowed.
        for child in behaviour.prior_sections():
            describe_behaviour(session, debug_context, child, indent + 2, False)
        describe_behaviour(session, debug_context, behaviour.last(), indent + 2, False)
    elif isinstance(behaviour, fdr.TraceBehaviour):
        print "%sbehaviour type: loops after index %s" % (" "*indent,
            session.uncompile_event(behaviour.error_event()))

    # Describe the trace of the behaviour
    t = ""
    for event in behaviour.trace():
        if event == fdr.INVALID_EVENT:
            t += "-, "
        else:
            t += str(session.uncompile_event(event)) + ", "
    print "%sTrace: %s" % (" "*indent, t)

    # Describe any named states of the behaviour
    t = ""
    for node in behaviour.node_path():
        if node == None:
            t += "-, "
        else:
            process_name = session.machine_node_name(behaviour.machine(), node)
            if process_name == None:
                t += "(unknown), "
            else:
                t += str(process_name)+", "
    print "%sStates: %s" % (" "*indent, t)

    # Describe our own children recursively
    if recurse:
        for child in debug_context.behaviour_children(behaviour):
            describe_behaviour(session, debug_context, child, indent + 2, recurse)

if __name__ == "__main__":
    main()
