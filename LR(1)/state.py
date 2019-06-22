from copy import deepcopy

class State:
    state_count = -1
    def __init__(self, new_state):
        self.state = deepcopy(new_state)#new state is a list like this     [lhs,rhs,lookaheads]
        self.actions = {} #actions for the state
        self.parent = ()  #parents of the state
        State.state_count += 1
        self.state_num = self.state_count#state's num

    def update_goto(self, X, N):
        self.actions[X] = N.state_num

    def update_parentName(self,I,X):
        self.parent = (I.state_num, X)


