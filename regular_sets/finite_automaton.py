from functools import reduce


def get_alphabet(machine):
    """Returns the NFA's or DFA's input alphabet, generated on the fly.
    execute 'or (union)' between foreach two elements set from symbols of the machine

    :param machine: {dict} NFA or DFA
    :return: {set} alphabet
    """
    sigma = reduce(
        (lambda symbol_a, symbol_b: set(symbol_a) | set(symbol_b)),
        [dicts.keys() for dicts in machine.delta.values()]
    )
    return sigma


def get_states(machine):
    """Returns the NFA's or DFA's input states, generated on the fly.
    execute 'or union' between foreach two states set from machine

    :param machine: {dict} NFA or DFA
    :return: {set} states
    """
    list_states = reduce((lambda list_a, list_b: list_a + list_b),
                         [list(symbols.values()) for symbols in machine.delta.values()])

    _states = set([machine.initial_state]) | \
              set(machine.delta.keys()) | \
              reduce((lambda a, b: a | b), list_states)

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
        return (self.compute(self.initial_state, input_string) in self.accept_states)

