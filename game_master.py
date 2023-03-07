import random

'''
The class defines the behavior of a player. It needs the parameters num1, num2 
to define the actions, where 1 <= num1 < num2 < 10, and num1 and num2 are rankings.
- When the card ranks higher than or equal to num1:
    70% raise; 20% check; 10% fold
- When the card ranks lower than num1, but higher than or equal to num2:
    20% raise; 70% check; 10% fold
- Otherwise:
    10% raise; 20% check; 70% fold

The above numbers (10, 20, 70) can be modified.
'''
class player:
    def __init__(self, n1, n2) -> None:
        assert 1 <= n1
        assert n1 < n2
        assert n2 < 10
        self.n1 = n1
        self.n2 = n2
        self.chips = 0 # used chips

    '''
    0: raise
    1: check
    2: fold
    '''
    def get_action(self, ranks) -> int:
        p = random.randint(0, 99)
        if ranks <= self.n1:
            return ([0]*70 + [1]*20 + [2]*10)[p]
        elif ranks <= self.n2:
            return ([1]*70 + [0]*20 + [2]*10)[p]
        else:
            return ([2]*70 + [1]*20 + [0]*10)[p]

    def __repr__(self) -> str:
        return 'Player has used {} chips.'.format(self.chips)


'''
This class defines the behavior of the agent.
The parameter is the file containing the strategy, default to be random.
'''
class agent:
    def __init__(self, strategy='random') -> None:
        self.strategy = strategy
        self.strategy_from_file = None
        self.chips = 0 # used chips

    def get_action(self, s) -> int:
        assert s <= 6
        if self.strategy == 'random':
            return self.get_randon_action()
        elif not self.strategy_from_file:
            # already read from file
            return random.choice(self.strategy_from_file[s])
        else:
            # read from file first
            self.get_strategy_from_file(self.strategy)
            return random.choice(self.strategy_from_file[s])

    def __repr__(self) -> str:
        return 'Agent has used {} chips.'.format(self.chips)

    def get_randon_action(self) -> int:
        return random.randint(0, 2)
    
    '''
    This function reads the strategy from the file, and stores the strategy
    as a dict() into the class field.
    '''
    def get_strategy_from_file(self, file_name) -> None:
        pass

'''
This class defines the entire game (one round) with the perspective of 
the agent. The game follows the MDP model.
'''
class game:
    def __init__(self, agent_no = 0, small_blind_no = 0, num_player = 4) -> None:
        self.small_blind_no = small_blind_no
        self.num_player = num_player
        self.players = dict([(i,player(3, 7)) for i in range(num_player)]) # counter clockwise
        self.agent = agent_no
        self.players[self.agent] = agent()

    def start_game(self) -> None:
        self.compulsory_bets()

    def compulsory_bets(self) -> None:
        for i, p in self.players.items():
            if i == self.small_blind_no:
                p.chips = 1
            if i == (self.small_blind_no + 1) % self.num_player:
                p.chips = 2
    
    def pre_flop(self) -> None:
        pass

    def flop(self) -> None:
        pass

    def turn(self) -> None:
        pass

    def river(self) -> None:
        pass

    def fold(self) -> None:
        pass

if __name__ == "__main__":
    g = game()
    g.start_game()
    print(g.players)