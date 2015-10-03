import unittest

from regular_sets.finite_automaton import DFA, NDFA

def create_dfa():
    """ create DFA to help the tests
        new_delta |     a    |     b    |
       -----------|----------|----------|
          ->{q0}  | {q1,q2}  |     -    |
          *{q1,q2}|   {q1}   |   {q3}   |
           *{q1}  |   {q1}   |     -    |
           *{q3}  |   {q2}   |     -    |
            {q2}  |     -    |   {q3}   |
       ---------------------------------|
    :return: {DFA}
    """
    # It's needed use frozenset on states to iterate by element in DFA
    # for not use iterate in hashes
    delta = {frozenset({'q0'}): {'a': frozenset({'q1','q2'})},
             frozenset({'q1', 'q2'}): {'a': frozenset({'q1'}), 'b': frozenset({'q3'})},
             frozenset({'q1'}): {'a': frozenset({'q1'})},
             frozenset({'q3'}): {'a': frozenset({'q2'})},
             frozenset({'q2'}): {'b': frozenset({'q3'})}}

    initial_state = frozenset({'q0'})
    accept_states = [frozenset({'q1', 'q2'}),
                     frozenset({'q1'}),
                     frozenset({'q3'})]

    return DFA(delta, initial_state, accept_states)

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
        accept_states = ['q0']
        self.dfa = DFA(self.delta, initial_state, accept_states)

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
        sigma = self.dfa.get_alphabet()
        self.assertSetEqual({'a', 'b'}, sigma)

    def test_get_states_from_DFA(self):
        """
        get states from DFA
        states {q0, q1}
        """
        states = self.dfa.get_states()
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
        self.delta = {
            'q0': {'a': {'q1', 'q2'}},
            'q1': {'a': {'q1'}},
            'q2': {'b': {'q3'}},
            'q3': {'a': {'q2'}}
        }

        initial_state = 'q0'
        accept_states = ['q1', 'q3']
        self.ndfa = NDFA(self.delta, initial_state, accept_states)

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
        get alphabet from DFA
        alphabet = {a, b}
        """
        sigma = self.ndfa.get_alphabet()
        self.assertSetEqual({'a', 'b'}, sigma)

    def test_get_states_from_NDFA(self):
        """
        get states from DFA
        states {q0, q1}
        """
        states = self.ndfa.get_states()
        self.assertSetEqual({'q0', 'q1', 'q2', 'q3'}, states)

    def test_determinization(self):
        """
        transform this NDFA to compatible DFA

        new delta table determinate

           L = a+ or (ab)+}

           delta |    a   |   b   |             new_delta |     a    |     b    |
           ------|--------|-------|              ---------|----------|----------|
            ->q0 | q1,q2  |   -   |       \       ->{q0}  | {q1,q2}  |     -    |
             *q1 |   q1   |   -   |    ----\      *{q1,q2}|   {q1}   |   {q3}   |
              q2 |   -    |  q3   |    ----/       *{q1}  |   {q1}   |     -    |
             *q3 |   q2   |   -   |       /        *{q3}  |   {q2}   |     -    |
           -----------------------|                 {q2}  |     -    |   {q3}   |
                                                 -------------------------------|

        """
        ndfa_determinized = self.ndfa.determinization()

        self.assertIsInstance(ndfa_determinized, DFA)

        expected_dfa = create_dfa()
        self.assertDictEqual(expected_dfa.delta, ndfa_determinized.delta) # check delta transitions
        self.assertSetEqual(expected_dfa.accept_states, ndfa_determinized.accept_states) # check accept states
        self.assertEqual(expected_dfa.initial_state, ndfa_determinized.initial_state) # check initial state

        # check states and alphabet from DFA generated
        self.assertSetEqual(expected_dfa.get_states(), ndfa_determinized.get_states())
        self.assertSetEqual(expected_dfa.get_alphabet(), ndfa_determinized.get_alphabet())

    def test_is_epsilon_free(self):
        self.assertTrue(self.ndfa.is_epsilon_free())

    def create_epsilon_ndfa(self):
        """
           delta |    a   |   b   |   &   |
           ------|--------|-------|-------|
            ->q0 |    -   |   -   | q1,q3 |
             *q1 |   q2   |   -   |   -   |
              q2 |   q1   |   -   |   -   |
             *q3 |    -   |   q4  |   -   |
              q4 |    -   |   q3  |   -   |
           -------------------------------|

        :return:{NDFA} non epsilon free
        """
        initial_state = 'q0'
        accept_states = ['q1', 'q3']

        delta_with_epsilon = {
            'q0': {'&': {'q1', 'q3'}},
            'q1': {'a': {'q2'}},
            'q2': {'a': {'q1'}},
            'q3': {'b': {'q4'}},
            'q4': {'b': {'q3'}}
        }

        return NDFA(delta_with_epsilon, initial_state, accept_states)

    def test_epsilon_closure_from_q0(self):
        epsilon_ndfa = self.create_epsilon_ndfa()
        _epsilon_closure = epsilon_ndfa.epsilon_closure('q0')
        expected_closure = {'q0','q1','q3'}
        self.assertSetEqual(expected_closure, _epsilon_closure)



if __name__ == '__main__':
    unittest.main()
