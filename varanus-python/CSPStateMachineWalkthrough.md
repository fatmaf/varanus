# A walkthrough of the class called CSPStateMachine
### Files used: 
* `wrap_state_machine.py`
* `CSPStateMachine.py` 
* `state_machine.py`
* `sm_config.yaml`

### Walkthrough 
#### `wrap_state_machine.py`
This does all the work, so this is the bit I will attempt to explain. 
* Assuming we have a CSP process `a->b->SKIP` 
* We can use `make_simple_state_machine` from `state_machine` to generate a dictionary representation of the FDR TS. 
* This dictionary contains all the states as keys and a list of transition-state pairs as values i.e. each state has a list of tranistion-state pairs associated with it. 
* We can then create a `CSPStateMachine` object initialised using this dictionary
* **The constructor simply assumes that the first state it adds to it's list is the initial state**
* Through this object we can: 
  * set an initial state 
  * add states 
  * add transitions 
  * apply transitions 

#### `CSPStateMachine.py` 
This file has 3 classes:State,Transition and CSPStateMachine 

##### State 
* constructor takes in a state name
* `add_transition` adds a transition to the state (expected object `Transition`)
* `transit` takes an *event* or *transition name* and returns the corresponding transition object or None 

##### Transition 
* construction takes the name, if the name matches a tick then this is a terminating transition
* `add_state` adds a state to the transition with probability 1 
* `get_first_state` returns the first state of a transtion 
* Also has a class variable `_ACCEPTINGSTATE` of type `State` with the name accepting 

##### CSPStateMachine 
* constructor -> empty where everything is set to None or False / takes a dictionary object and iterates over it's keys adding each state/ transition-state list. 
* 
