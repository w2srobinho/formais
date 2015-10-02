from functools import reduce


def get_alphabet(machine):
    """Returns the NFA's or DFA's input alphabet, generated on the fly.
    execute 'or (union)' between foreach two elements set from symbols of the machine

    :param machine: {dict} NFA or DFA
    :return: {set} alphabet
    """
    sigma = reduce(
        (lambda a_symbol, b_symbol: set(a_symbol) | set(b_symbol)),
        [dicts.keys() for dicts in machine.delta.values()]
    )
    return sigma


def get_states(machine):
    """Returns the NFA's or DFA's input states, generated on the fly.
    execute 'or union' between foreach two states set from machine

    :param machine: {dict} NFA or DFA
    :return: {set} states
    """
    states_list = reduce((lambda a_list, b_list: a_list + b_list),
                         [list(symbols.values()) for symbols in machine.delta.values()])

    _states = {machine.initial_state} | set(machine.delta.keys()) | reduce((lambda a, b: a | b), states_list)

    return _states


class DFA:
    """Class that encapsulates a DFA."""

    def __init__(self, delta_transitions, initial_state, accept_states):
        """DFA Constructor
        :param delta_transitions: {dict} transitions
            ex. {'q0': {'a': {'q1'}, 'b': {'q1'}}, 'q1': {'a': {'q0'}}}
        :param initial_state: {str}
        :param accept_states: {list} with {str} accept states
        """
        self.delta = delta_transitions
        self.initial_state = initial_state
        self.accept_states = set(accept_states)

    def compute(self, state, input_string):
        """ compute strings in DFA
        :param state: is actual state
        :param input_string: string to compute
        :return: last state computed
        """
        _state = {state}
        for a in input_string:
            _state = self.delta[next(iter(_state))][a]
        return next(iter(_state))

    def validate_sentence(self, input_string):
        """
        :param input_string: sentence to validate
        :return: True, if is a valid sentence
                 False, otherwise
        """
        return self.compute(self.initial_state, input_string) in self.accept_states


class NDFA(DFA):
    """Class that encapsulates an NFA.
    inherit from DFA
    """

    def compute(self, state, input_string):
        """override compute from {DFA}
        compute strings in NDFA
        :param state: is actual state
        :param input_string: string to compute
        :return: empty set if transition isn't defined
                else set with states
        """
        _states = {state}
        for a in input_string:
            new_states = set([])
            for _state in _states:
                try:
                    new_states |= self.delta[_state][a]
                except KeyError:
                    pass
            _states = new_states
        return _states

    def validate_sentence(self, input_string):
        """override validate_sentence from {DFA}
        :param input_string: sentence to validate
        :return: True, if is a valid sentence
                 False, otherwise
        """
        return len(self.compute(self.initial_state, input_string) & self.accept_states) > 0

    def determinization(self):
        """Converts the input NFA into a DFA.
        :return: {DFA} compatible with this NDFA
        """
        _initial_state = frozenset([self.initial_state])  # define _initial_state as immutable
        _states = set([_initial_state])
        unprocessed_states = _states.copy()  # unprocessed_states tracks states for which delta is not yet defined
        new_delta = {}
        accept_states = []
        sigma = get_alphabet(self)

        while len(unprocessed_states) > 0:
            actual_states_set = unprocessed_states.pop()
            new_delta[actual_states_set] = {}
            for symbol in sigma:
                next_states_list = [self.compute(q, symbol) for q in actual_states_set] # it gets list of next states
                next_states = reduce(lambda x, y: x | y, next_states_list) # union foreach list elements
                next_states = frozenset(next_states)
                if len(next_states):
                    new_delta[actual_states_set][symbol] = next_states

                    if not next_states in _states: # if new state found, add to unprocessed list for it processes in future
                        _states.add(next_states)
                        unprocessed_states.add(next_states)

        for actual_states_set in _states:
            if len(actual_states_set & self.accept_states) > 0:
                accept_states.append(actual_states_set)

        return DFA(new_delta, _initial_state, accept_states)
