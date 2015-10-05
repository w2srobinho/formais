import unittest

from regular_sets import regular_grammar

from regular_sets.finite_automaton import NDFA


class RegularGrammarTests(unittest.TestCase):
    def setUp(self):
        transitions_str = "S1 -> aA | aB | aC | bB | bC | cC | a | b | c | & " \
                          "A -> aA | aB | aC | a " \
                          "B -> bB | bC | b " \
                          "C -> cC | c"

        self.grammar = regular_grammar.make_it_proper_to_grammar(transitions_str)

    def test_grammar_to_automata(self):
        delta = self.grammar.to_automata()
        ndfa = NDFA(delta, 'S1', ['qAccept'])

        self.assertTrue(ndfa.validate_sentence('aabbbbcc'))
        self.assertFalse(ndfa.validate_sentence('aaccbb'))

        dfa = ndfa.determinization()

        self.assertTrue(ndfa.validate_sentence('aabbbbcc'))
        self.assertFalse(ndfa.validate_sentence('aaccbb'))

        regular = dfa.to_grammar()


if __name__ == "__main__":
    unittest.main()
