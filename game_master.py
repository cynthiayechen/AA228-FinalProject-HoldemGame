from ast import Tuple
import random

COLOR = [0, 1, 2, 3] # club, spade, heart, dimond
NUMBER = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

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
        self.card1 = None
        self.card2 = None
        self.current_call = 0

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
        return 'Player has used {} chips, and has cards {} and {}\n'.format(self.chips, self.card1, self.card2)


'''
This class defines the behavior of the agent.
The parameter is the file containing the strategy, default to be random.
'''
class agent:
    def __init__(self, strategy='random') -> None:
        self.strategy = strategy
        self.strategy_from_file = None
        self.chips = 0 # used chips
        self.card1 = None
        self.card2 = None
        self.current_call = 0

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
        return 'Agent has used {} chips and has cards {} and {}\n'.format(self.chips, self.card1, self.card2)

    def get_randon_action(self) -> int:
        return 1
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
Game State:
0 Before Start
1 Compulsory Bets
2 Pre Flop
3 Flop
4 Turn
5 River

For simplicity, let small blind to be player -2, and big blind to be player -1.
Need to pass in the player number of the agent, default to be 0.
'''
class game:
    def __init__(self, agent_no = 0, num_player = 4, raise_amount = 3) -> None:
        self.num_player = num_player
        self.players = dict([(i,player(3, 7)) for i in range(num_player)]) # clockwise
        self.agent = agent_no
        self.raise_amount = raise_amount
        self.players[self.agent] = agent()
        self.CD1 = None # CD: community card
        self.CD2 = None
        self.CD3 = None
        self.CD4 = None
        self.CD5 = None
        self.state = 0
        self.chips_in_pool = 0
        self.card_in_use = set()
        self.current_call = 0

    def start_game(self) -> int:
        self.compulsory_bets()
        if self.pre_flop():
            return -1 * self.players[self.agent].chips

        # clear out
        for _, p in self.players.items():
            p.current_call = 0
        self.current_call = 0
        if self.flop():
            return -1 * self.players[self.agent].chips

        # clear out
        for _, p in self.players.items():
            p.current_call = 0
        self.current_call = 0
        if self.turn():
            return -1 * self.players[self.agent].chips

        # clear out
        for _, p in self.players.items():
            p.current_call = 0
        self.current_call = 0
        if self.river():
            return -1 * self.players[self.agent].chips

        return self.compute_reward()

    def compulsory_bets(self) -> None:
        for i, p in self.players.items():
            if i == self.num_player - 2:
                p.chips = 1
                p.current_call = 1
            if i == self.num_player - 1:
                p.chips = 2
                p.current_call = 2
        self.state = 1
        self.chips_in_pool = 3
        self.current_call = 2
    
    def pre_flop(self) -> bool:
        # deal two cards
        # each player acts
        self.state = 2
        for i, p in self.players.items():
            p.card1, p.card2 = self.deal_card(), self.deal_card()
        return self.betting_round()

    def flop(self) -> bool:
        # 3 community cards
        # each player acts
        self.state = 3
        self.CD1, self.CD2, self.CD3 = self.deal_card(), self.deal_card(), self.deal_card()
        return self.betting_round()
        

    def turn(self) -> bool:
        # 4th community card
        # each player acts
        self.state = 4
        self.CD4 = self.deal_card()
        return self.betting_round()

    def river(self) -> None:
        # 5th community card
        # each player acts
        self.state = 5
        self.CD5 = self.deal_card()
        if self.betting_round(): return True
        return self.betting_round()

    '''
    Read information from the cards field in player.
    '''
    def get_rank(self, player) -> int:
        return random.randint(0, 10)

    '''
    Only computes the reward of the agent.
    Assume to be at state 5.
    '''
    def compute_reward(self) -> int:
        num = 1
        rank = self.get_rank(self.players[self.agent])
        for i, p in self.players.items():
            if i == self.agent: continue
            r = self.get_rank(p)
            # if other player wins
            if r < rank:
                return -1 * self.players[self.agent].chips
            # if ties
            if r == rank:
                num += 1
        return self.chips_in_pool // num

    '''
    The method actually draws the card.
    '''
    def deal_card(self) -> Tuple(int, int):
        while True:
            color, number = random.choice(COLOR), random.choice(NUMBER)
            if (color, number) not in self.card_in_use:
                self.card_in_use.add((color, number))
                return ((color, number))

    '''
    This method simulates the betting rounds.
    '''
    def betting_round(self) -> bool:
        finished = False

        # first round
        temp_dict = dict(self.players)
        for i, p in temp_dict.items():
            # agent
            if i == self.agent:
                action = p.get_action(self.state)
                if action == 2:
                    return True
            # non agent
            else:
                action = p.get_action(self.get_rank(p))
                if action == 2:
                    del self.players[i]
            
            # not folding
            if action == 0:
                self.chips_in_pool += (self.raise_amount + self.current_call)
                self.players[i].chips += (self.raise_amount + self.current_call)
                self.current_call += self.raise_amount
                self.players[i].current_call = self.current_call
                finished = False
            elif action == 1:
                self.chips_in_pool += (self.current_call - self.players[i].current_call)
                self.players[i].chips += (self.current_call - self.players[i].current_call)
                self.players[i].current_call = self.current_call
                finished &= True
        self.players = dict(temp_dict)
        if finished: return False

        # second round -> only check or fold
        temp_dict = dict(self.players)
        for i, p in temp_dict.items():
            # agent
            if i == self.agent:
                action = p.get_action(self.state)
                if action == 2:
                    return True
            # non agent
            else:
                action = p.get_action(self.get_rank(p))
                if action == 2:
                    del self.players[i]

            # not folding
            if action == 0 or action == 1:
                self.chips_in_pool += (self.current_call - self.players[i].current_call)
                self.players[i].chips += (self.current_call - self.players[i].current_call)
                self.players[i].current_call = self.current_call
        self.players = dict(temp_dict)

        return False

if __name__ == "__main__":
    g = game()
    print(g.start_game())
    print(g.players)
    print(g.CD1, g.CD2, g.CD3, g.CD4, g.CD5)
    print(g.chips_in_pool)