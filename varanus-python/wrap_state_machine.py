from state_machine import *


# the class for creating a "state machine from a dictionary"
# states have names and transitions
# transitions have states
class CSPStateMachine(object):
    class State(object):
        def __init__(self, name):
            self.name = name
            self.transitions = None

        def add_transition(self, transition):
            if self.transitions is None:
                self.transitions = {}
            self.transitions[transition.name] = transition

        def transit(self, tranname):
            if tranname in self.transitions:
                return self.transitions[tranname]
            else:
                return None

        def __str__(self):
            return self.name

    class Transition(object):

        def __str__(self):
            return self.name

        def __init__(self, name):
            self.name = name
            self.states = None
            self.probabilities = None

        def add_state(self, state):
            if self.states is None:
                self.states = {}
                self.probabilities = {}
            self.states[state.name] = state
            self.probabilities[state.name] = 1.0

        def get_first_state(self):
            # just return the first state
            return self.states.values()[0]

    def __init__(self):
        self.states = None
        self.current_state = None
        self.initial_state = None

    def __init__(self,sm_dictionary):
        self.states = None
        self.current_state = None
        self.initial_state = None
        # so this is a state machine dictionary
        # all the keys are states
        # all the tuples are transitions
        for key in sm_dictionary:
            self.add_state(key)

        self.initial_state = self.states['0']

        for key in sm_dictionary:
            for tran in sm_dictionary[key]:
                tranname = tran[0]
                trandest = tran[1]
                self.add_state(trandest)
                self.add_transition_by_name(key,tranname,trandest)



    def init_state(self, statename):
        if statename in self.states:
            self.initial_state = self.states[statename]

    def add_state(self, statename):
        if self.states is None:
            self.states = {}
        if statename not in self.states:
            self.states[statename] = CSPStateMachine.State(statename)

    def add_transition_by_name(self,srcname,tranname,destname):
        tran = CSPStateMachine.Transition(tranname)

        if self.states is None:
            self.add_state(srcname)
        if srcname not in self.states:
            self.add_state(srcname)
        if destname not in self.states:
            self.add_state(destname)
        tran.add_state(self.states[destname])
        self.states[srcname].add_transition(tran)


    def transit(self, tranname):
        if self.current_state is None:
            self.current_state = self.initial_state
        transition = self.current_state.transit(tranname)
        if transition is not None:
            self.current_state = transition.get_first_state()
        else:
            print("Invalid transition")
            return None

        return self.current_state

    def start(self):
        self.current_state = self.initial_state

    def test_machine(self):
        result = {}
        self.start()
        transitions = ['a','b','\xe2\x9c\x93']
        for transition in transitions:
            if(self.current_state.name not in result):
                result[self.current_state.name]=[]
            result[self.current_state.name].append((transition,self.transit(transition).name))


        return result


if __name__ == '__main__':
    # Make some test processes
    test_process = "a -> b -> SKIP"
    test_process_sm = {'0': [('a', '1')], '1': [('b', '2')], '2': [
        ('\xe2\x9c\x93', '3')]}

    test_process2 = "a -> (b -> SKIP [] c -> SKIP)"
    test_process2_sm = {'0': [('a', '1')], '1': [("b", '2'), ("c", "2")], '2': [
        ('\xe2\x9c\x93', '3')]}

    test_process3 = "(b -> SKIP [] c -> SKIP)"
    test_process3_sm = {'1': [('\xe2\x9c\x93', '2')], '0': [
        ('b', '1'), ('c', '1')]}

    # Run some tests. I've only been able to test one process at a time, becasue
    # after one it segfaults...

    #    print(test_process)
    #    result = make_simple_state_machine(test_process)
    #    print("result...")
    #    print(result)
    #    assert (result == test_process_sm)

    print(test_process2)
    result2 = (make_simple_state_machine(test_process2))
    # this is a dictionary where the key is the node number
    # the value is a list of tuples (transition, dest)
    statemachine_wrapper = CSPStateMachine(result2)

    print("result...")
    print(result2)
    assert (result2 == test_process2_sm)

    wrapper_result = statemachine_wrapper.test_machine()
    print("result from wrapper ")
    print(wrapper_result)
    # print(test_process3)
    # result3 = (make_simple_state_machine(test_process3))
    # print("result...")
    # print(result3)
    # assert(result3 == test_process3_sm)
