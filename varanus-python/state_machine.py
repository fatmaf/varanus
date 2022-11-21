from fdr_interface import *

""" Utilities for machine CSP into useful State Machines
Matt Luckcuck 2022
"""


def make_simple_state_machine(process):

    state_machine = []

    fdr_interface = FDRInterface()
    #This loads the whole model (channels and all)
    fdr_interface.load_model("test/simple.csp")

    #This evaluates a process (say, the trace)
    LTS = fdr_interface.session.evaluate_process(
        process, fdr.SemanticModel_Traces, None)

    #The result of the evaluate_process call is a state machine
    machine = LTS.result()
    root = machine.root_node()

    #process_map = get_events(fdr_interface, machine, root)
    process_map = get_process_map(fdr_interface, machine, root)

    fdr_interface.close()

    return process_map

#    transitions_root = machine.transitions(root)  # tuple
#    for t in transitions_root:
    # the event the transition represents
#        print(fdr_interface.session.uncompile_event(t.event()))
#        dest = t.destination()  # the node the transition goes to
    # and the events out of the destination
#        initials_dest = machine.initials(dest)
#        print(fdr_interface.session.uncompile_events(initials_dest))


# Currently just doing strings
def get_process_map(fdr_interface, machine, this_node):

    transitions = machine.transitions(this_node)
    machine_map = {}

    for t in transitions:
        label_next_pairs = []

        next_state = str(t.destination().hash_code())
        event = str(fdr_interface.session.uncompile_event(t.event()))
        next_events = fdr_interface.session.uncompile_events(
            this_node.initials())

        this_node_num = str(this_node.hash_code())

        if (this_node_num in machine_map.keys()):
            current_list = machine_map[this_node_num]
            update_list = current_list.append((event, next_state))
            machine_map.update({this_node_num: update_list})
        else:
            machine_map.update({this_node_num: [(event, next_state)]})

# recurse with the next nodes

    return machine_map


def get_events(fdr_interface, machine, this_node):

    transitions = machine.transitions(this_node)
    transition_pairs = []
    for t in transitions:
        # the event the transition represents
        trans_event = fdr_interface.session.uncompile_event(t.event())

        print(trans_event)
        dest = t.destination()  # the node the transition goes to
        print("hash code = " + str(dest.hash_code()))
        # and the events out of the destination
        initials_dest = machine.initials(dest)
        next_events = fdr_interface.session.uncompile_events(
            initials_dest)  # tuple
        print(next_events)

        for e in next_events:
            transition_pairs.append((trans_event.to_string(), e.to_string()))
            print(transition_pairs)
        if(next_events):
            transition_pairs += get_events(fdr_interface, machine, dest)

    return transition_pairs


if __name__ == '__main__':
    test_process = "a -> b -> SKIP"
    # test_process_sm = [("a", "b"), ("b", '\xe2\x9c\x93')]
    test_process_sm = {'0': [('a', '1')]}

    test_process2 = "a -> (b -> SKIP [] c -> SKIP)"
    test_process2_sm = [("a", "b"), ("a", "c"),
                        ("b", '\xe2\x9c\x93'), ("c", '\xe2\x9c\x93')]

    result = make_simple_state_machine(test_process)
    print("result...")
    print(result)
    assert (result == test_process_sm)

    #result2 = (make_simple_state_machine(test_process2))
#    print("result...")
#    print(result2)
#    assert(result2 == test_process2_sm)

    #fdr_interface = FDRInterface()
    #fdr_interface.load_model("test/simple.csp")

    # evaluate_process runs the process given, in the semantic model given, within the session
    #LTS = fdr_interface.session.evaluate_process(
    #    test_process, fdr.SemanticModel_Traces, None)
    # Here is an example of calling a process deinfed in simple.csp
    # LTS = fdr_interface.session.evaluate_process("D(0)", fdr.SemanticModel_Traces, None)

    #The result of the evaluate_process call is a state machine
    #machine = LTS.result()

    #We can get the root node of a state machine...
    #root = machine.root_node()

    # ... and print it's name (if it has one) ...
    #print(fdr_interface.session.machine_node_name(machine, root))

    # ...and get the initial events out of the root node...
    #initials_root = machine.initials(root)

    # but we have to uncompile them first.
    #Be careful, lots of methods return tuples, not just compiled events
    #print(fdr_interface.session.uncompile_events(initials_root))

    #alphabet = machine.alphabet(True)

    #print(fdr_interface.session.uncompile_events(alphabet))

    #Transitions from the root node
    #transitions_root = machine.transitions(root)  # tuple
    #for t in transitions_root:
    # the event the transition represents
    #    print(fdr_interface.session.uncompile_event(t.event()))
    #    dest = t.destination()  # the node the transition goes to
    # and the events out of the destination
    #    initials_dest = machine.initials(dest)
    #    print(fdr_interface.session.uncompile_events(initials_dest))
