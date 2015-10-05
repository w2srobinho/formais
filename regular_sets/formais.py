import sys

from regular_grammar import regular_grammar
from finite_automaton import DFA, NDFA

def make_it_proper_to_grammar(x):
    """ 
    :param x: {string} grammar
    """
    grammar = x.split(' ')
    initial_simbol = grammar[0]
    non_terminals = set()
    terminals = set()
    temporary_alfa = ''
    temporary_beta = set()

    productionDict = dict()

    grammar_length = len(grammar)

    for i in range(0, grammar_length):
        if grammar[i].isupper():            
            non_terminals.add(grammar[i])

        if not grammar[i] == '|' and not grammar[i] == '->' and not i == 0 and not grammar[i].isupper():
            temporary_beta.add(grammar[i])
            terminals.add(grammar[i][0])

        if grammar[i] == '->' or i == grammar_length - 1:
            if len(temporary_beta) > 0:
                productionDict[temporary_alfa] = temporary_beta

            temporary_beta = set()
            temporary_alfa = grammar[i-1]

    return regular_grammar(non_terminals, terminals, productionDict, initial_simbol)

def main():
    gramatica = "S1 -> aA | aB | aC | bB | bC | cC | a | b | c | & "\
                 "A -> aA | aB | aC | a "\
                 "B -> bB | bC | b "\
                 "C -> cC | c"

    grammar = make_it_proper_to_grammar(gramatica)
    
    delta = grammar.to_automata()

    ndfa = NDFA(delta, 'S1', ['qAccept'])

    nfa_true_sentence = ndfa.validate_sentence('aabbbbcc')
    nfa_false_sentence = ndfa.validate_sentence('aaccbb')

    dfa = ndfa.determinization()

    dfa_true_sentence = ndfa.validate_sentence('aabbbbcc')
    dfa_false_sentence = ndfa.validate_sentence('aaccbb')

    regular = dfa.to_grammar()

if __name__ == "__main__":
    sys.exit(int(main() or 0))
