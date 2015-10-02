import unittest

from regular_sets import finite_automaton
from regular_sets.finite_automaton import DFA, NDFA


class DFATests(unittest.TestCase):
    def setUp(self):
        """delta table

           L = {w | w ∈ Σ*={a, b} and |w| is pair}

           delta |   a   |   b   |
           ------|-------|-------|
           *->q0 |   q1  |  q1   |
              q1 |   q0  |  q0   |
           ----------------------|
        """
        self.delta = {'q0': {'a': {'q1'}, 'b': {'q1'}}, 'q1': {'a': {'q0'}, 'b': {'q0'}}}

        initial_state = 'q0'
        final_states = ['q0']
        self.dfa = DFA(self.delta, initial_state, final_states)

    def test_accept_sentence_abab(self):
        """
        DFA accept sentence 'abab'
        """
        is_accept = self.dfa.validate_sentence('abab')
        self.assertTrue(is_accept)

    def test_reject_sentence_ababa(self):
        """
        DFA reject sentence 'ababa'
        """
        is_accept = self.dfa.validate_sentence('ababa')
        self.assertFalse(is_accept)

    def test_get_alphabet_from_DFA(self):
        """
        get alphabeth from DFA
        alphabeth = {a, b}
        """
        sigma = finite_automaton.get_alphabet(self.dfa)
        self.assertSetEqual({'a', 'b'}, sigma)

    def test_get_states_from_DFA(self):
        """
        get states from DFA
        states {q0, q1}
        """
        states = finite_automaton.get_states(self.dfa)
        self.assertSetEqual({'q0', 'q1'}, states)


class NDFATests(unittest.TestCase):
    def setUp(self):
        """delta table


           L = a+ or (ab)+}

           delta |    a   |   b   |
           ------|--------|-------|
            ->q0 | q1,q2  |   -   |
             *q1 |   q1   |   -   |
              q2 |   -    |  q3   |
             *q3 |   q2   |   -   |
           -----------------------|
        """
        self.delta = {'q0': {'a': {'q1', 'q2'}}, 'q1': {'a': {'q1'}}, 'q2': {'b': {'q3'}}, 'q3': {'a': {'q2'}}}

        initial_state = 'q0'
        final_states = ['q0', 'q1', 'q3']
        self.ndfa = NDFA(self.delta, initial_state, final_states)

    def test_accept_sentence_aaa(self):
        """
        DFA accept sentence 'aaa'
        """
        is_accept = self.ndfa.validate_sentence('aaa')
        self.assertTrue(is_accept)

    def test_accept_sentence_ababab(self):
        """
        DFA accept sentence 'ababab'
        """
        is_accept = self.ndfa.validate_sentence('ababab')
        self.assertTrue(is_accept)

    def test_reject_sentence_aaabab(self):
        """
        DFA reject sentence 'aaabab'
        """
        is_accept = self.ndfa.validate_sentence('aaabab')
        self.assertFalse(is_accept)

    def test_get_alphabet_from_NDFA(self):
        """
        get alphabeth from DFA
        alphabeth = {a, b}
        """
        sigma = finite_automaton.get_alphabet(self.ndfa)
        self.assertSetEqual({'a', 'b'}, sigma)

    def test_get_states_from_NDFA(self):
        """
        get states from DFA
        states {q0, q1}
        """
        states = finite_automaton.get_states(self.ndfa)
        self.assertSetEqual({'q0', 'q1', 'q2', 'q3'}, states)


if __name__ == '__main__':
    unittest.main()
