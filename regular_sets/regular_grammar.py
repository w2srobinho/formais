class regular_grammar():
    
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
