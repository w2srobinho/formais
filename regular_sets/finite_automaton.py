
from functools import reduce


def get_alphabet(machine):
    """Returns the NFA's or DFA's input alphabet, generated on the fly.
    execute 'or (union)' foreach two set elements from simbols

    :param machine: {dict} NFA or DFA
    :return:{set} alphabet
    """
    sigma = reduce(
        (lambda a, b: set(a) | set(b)),
        [x.keys() for x in machine.delta.values()]
    )
    return sigma


class DFA:
    """Class that encapsulates a DFA."""

    def __init__(self, delta_transitions, initial_state, accept_states):
        self.delta = delta_transitions
        self.initial_state = initial_state
        self.accept_states = set(accept_states)

    def compute(self, state, input_string):
        """ compute strings in DFA
        :param state: is actual state
        :param input_string: string to compute
        :return: last state computed
        """
        state = {state}
        for a in input_string:
            state = self.delta[next(iter(state))][a]
        return next(iter(state))

    def validate_sentence(self, input_string):
        """
        :param input_string: sentence to validate
        :return: True, if is a valid sentence
                 False, otherwise
        """
        return self.compute(self.initial_state, input_string) in self.accept_states


