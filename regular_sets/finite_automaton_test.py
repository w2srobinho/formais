import unittest

from regular_sets.finite_automaton import DFA

class DFATests(unittest.TestCase):
    def setUp(self):
        """delta table

           L = {w | w ∈ Σ⋆={a, b} and |w| is pair}

           delta |   a   |   b   |
           ------|-------|-------|
           *->q0 |   q1  |  q1   |
              q1 |   q0  |  q0   |
           ----------------------|
        """
        self.delta = {'q0': {'a': {'q1'}, 'b': {'q1'}}, 'q1': {'a': {'q0'}, 'b': {'q0'}}}
        self.dfa = DFA(self.delta, 'q0', ['q0'])

    def test_accept_sentence(self):
        """
        DFA accept sentence 'abab'
        """
        is_accept = self.dfa.validate_sentence('abab')
        self.assertTrue(is_accept)

    def test_reject_sentence(self):
        """
        DFA reject sentence 'ababa'
        """
        is_accept = self.dfa.validate_sentence('ababa')
        self.assertFalse(is_accept)


if __name__ == '__main__':
    unittest.main()
