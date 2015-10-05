
def make_it_proper_to_grammar(transitions_str):
        """
        :param transitions_str: {string} grammar
        """
        grammar = transitions_str.split(' ')
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

class regular_grammar:
    
    def __init__(self, non_terminals, terminals, dict_of_productions, initial_simbol):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = dict_of_productions
        self.initial_simbol = initial_simbol


        
    def to_automata(self):
        """
        :return: productions of automata
        """
        states = self.non_terminals
        states.add('qAccept')
        delta = dict()
        temp = dict()

        for _alfa in self.productions:
            for _beta in self.productions[_alfa]:
                if _beta[0] in temp:
                    if len(_beta) == 2:
                        temp[_beta[0]].add(_beta[1])
                    else:
                        temp[_beta[0]].add('qAccept')
                else:
                    if len(_beta) == 2:
                        temp[_beta[0]] = {_beta[1]}
                    else:
                        temp[_beta[0]] = {'qAccept'}
            delta[_alfa] = temp
            temp = dict()

        return delta