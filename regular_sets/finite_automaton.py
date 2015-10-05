from functools import reduce
from regular_sets.regular_grammar import regular_grammar


def _union_sets(self, x, y):
    if (len(x) or len(y)):
        return (x | y)


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
        :param state: is current state
        :param input_string: string to compute
        :return: last state computed
        """
        _state = state

        try:
            if (not isinstance(_state, frozenset)):
                for a in input_string:
                    _state = next(iter(self.delta[_state][a]))
            else:
                for a in input_string:
                    _state = self.delta[_state][a]
        except KeyError:
            return {'reject'}
        return _state

    def validate_sentence(self, input_string):
        """
        :param input_string: sentence to validate
        :return: True, if is a valid sentence
                 False, otherwise
        """
        return self.compute(self.initial_state, input_string) in self.accept_states

    def get_alphabet(self):
        """Returns the NFA's or DFA's input alphabet, generated on the fly.
        execute 'or (union)' between foreach two elements set from symbols of the machine

        :return: {set} alphabet
        """
        sigma = reduce(
            (lambda a_symbol, b_symbol: set(a_symbol) | set(b_symbol)),
            [dicts.keys() for dicts in self.delta.values()])

        return sigma

    def get_states(self):
        """Returns the NFA's or DFA's input states, generated on the fly.
        execute 'or union' between foreach two states set from machine

        :return: {set} states
        """
        states_list = reduce((lambda a_list, b_list: a_list + b_list),
                             [list(symbols.values()) for symbols in self.delta.values()])

        _states = {self.initial_state} | set(self.delta.keys()) | reduce((lambda a, b: a | b), states_list)

        return _states

    def to_grammar(self):
        """
        :return: Productions of grammar
        """
        terminals = self.get_alphabet()
        initial_simbol = self.initial_state
        non_terminals = set()
        productions = dict()
        temp = list()
        string = ''
        next_state = set()

        for current_state in self.delta:  # each state
            non_terminals.add(current_state)
            for alphabet_simbol in self.delta[current_state]:  # each simbol of the alphabet
                for next_state_simbol in self.delta[current_state][alphabet_simbol]:  # each next state
                    string += next_state_simbol
                    next_state.add(next_state_simbol)
                    if next_state in self.accept_states and alphabet_simbol not in temp:
                        temp.append(alphabet_simbol)
                temp.append(alphabet_simbol + string)
                string = ''
            productions[current_state] = temp
            temp = list()
            next_state = set()

        return regular_grammar(non_terminals, terminals, productions, initial_simbol)


class NDFA(DFA):
    """Class that encapsulates an NFA.
    inherit from DFA
    """

    def compute(self, state, input_string):
        """override compute from {DFA}
        compute strings in NDFA
        :param state: is current state
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
        closure = {_state: self.epsilon_closure(_state) for _state in self.get_states()}

        _initial_state = frozenset(closure[self.initial_state])  # define _initial_state as immutable
        _states = {_initial_state}
        unprocessed_states = _states.copy()  # unprocessed_states tracks states for which delta is not yet defined
        new_delta = {}
        accept_states = []
        sigma = self.get_alphabet()

        while unprocessed_states:
            current_state = unprocessed_states.pop()
            new_delta[current_state] = {}
            for symbol in sigma:
                if symbol == '&':
                    continue
                next_states_list = [self.compute(q, symbol)
                                    for q in current_state
                                    if len(self.compute(q, symbol))]  # it gets list of next states
                try:
                    next_states = reduce(lambda x, y: _union_sets(closure[x], closure[y]),
                                         next_states_list)  # union foreach list elements
                except TypeError:
                    next_states = set([])

                next_states = frozenset(next_states)
                if len(next_states):
                    new_delta[current_state][symbol] = next_states

                    if not next_states in _states:  # if new state found, add to unprocessed list for it processes in future
                        _states.add(next_states)
                        unprocessed_states.add(next_states)

        for current_state in _states:
            if len(current_state & self.accept_states) > 0:
                accept_states.append(current_state)

        return DFA(new_delta, _initial_state, accept_states)

    def epsilon_closure(self, state):
        epsilon_transitions = {_state: self.delta[_state]['&']
                               for _state, symbol in self.delta.items()
                               if '&' in symbol}
        unprocessed_states = {state}
        _epsilon_closure = {state}

        while unprocessed_states:
            current_state = unprocessed_states.pop()
            if current_state in epsilon_transitions:
                state_to_add = {_state for _state in epsilon_transitions[current_state]
                                if _state not in _epsilon_closure}
                _epsilon_closure |= state_to_add
                unprocessed_states.add(s for s in state_to_add)

        return _epsilon_closure
