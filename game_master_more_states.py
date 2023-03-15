from ast import Tuple
import random
import sys
import csv
import argparse

COLOR = [0, 1, 2, 3] # club, spade, heart, dimond
NUMBER = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
FOLD = 42
FLOP = 10
TURN = 20
RIVER = 30

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
    def __init__(self, n1, n2, l1, l2, l3) -> None:
        assert 1 <= n1
        assert n1 < n2
        assert n2 < 10
        self.n1 = n1
        self.n2 = n2
        self.chips = 0 # used chips
        self.card1 = None
        self.card2 = None
        self.current_call = 0
        self.rank = 9
        assert l1 >= l2
        assert l2 >= l3
        assert l1 + l2 + l3 == 100
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3

    '''
    0: raise
    1: check
    2: fold
    '''
    def get_action(self, ranks) -> int:
        p = random.randint(0, 99)
        l1, l2, l3 = self.l1, self.l2, self.l3
        if ranks <= self.n1:
            return ([0]*l1 + [1]*l2 + [2]*l3)[p]
        elif ranks <= self.n2:
            return ([1]*l1 + [0]*l2 + [2]*l3)[p]
        else:
            return ([2]*l1 + [1]*l2 + [0]*l3)[p]

    def __repr__(self) -> str:
        return 'Player has used {} chips, and has cards {} and {}\n'.format(self.chips, self.card1, self.card2)


'''
This class defines the behavior of the agent.
The parameter is the file containing the strategy, default to be random.
'''
class agent:
    def __init__(self, strategy='random') -> None:
        self.strategy = strategy
        self.strategy_from_file = dict()
        self.chips = 0 # used chips
        self.card1 = None
        self.card2 = None
        self.current_call = 0
        self.rank = 9
        self.state = 40

    def get_action(self, s) -> int:
        if self.strategy == 'random':
            return self.get_randon_action()
        elif len(self.strategy_from_file.keys()) != 0:
            # already read from file
            if s not in self.strategy_from_file.keys():
                print(s)
                print(self.strategy_from_file)
            return self.strategy_from_file[s]
        else:
            # read from file first
            self.get_strategy_from_file(self.strategy)
            return self.strategy_from_file[s]

    def __repr__(self) -> str:
        return 'Agent has used {} chips and has cards {} and {}\n'.format(self.chips, self.card1, self.card2)

    def get_randon_action(self) -> int:
        return random.randint(0, 2)
    
    '''
    This function reads the strategy from the file, and stores the strategy
    as a dict() into the class field.
    '''
    def get_strategy_from_file(self, file_name) -> None:
        with open(file_name, 'r') as f:
            reader = csv.reader(f)
            for i, action in enumerate(reader):
                self.strategy_from_file[i] = int(action[0])

'''
This class defines the entire game (one round) with the perspective of 
the agent. The game follows the MDP model.
Agent State:
40 Before Start
41 Compulsory Bets
0-9 Pre Flop
10-19 Flop
20-29 Turn
30-39 River

42 Folding State

Game State:
0 Pre Flop
1 Flop
2 Turn
3 River
4 Before Start
5 Compulsory Bets
6 Fold

For simplicity, let small blind to be player -2, and big blind to be player -1.
Need to pass in the player number of the agent, default to be 0.
'''
class game:
    def __init__(self, agent_no = 0, num_player = 4, raise_amount = 5, agent_policy = 'random', iter = 0, n1 = 8, n2 = 9, l1 = 70, l2 = 20, l3 = 10) -> None:
        self.num_player = num_player
        self.players = dict([(i,player(n1, n2, l1, l2, l3)) for i in range(num_player)]) # clockwise
        self.agent = agent_no
        self.raise_amount = raise_amount
        self.players[self.agent] = agent(strategy=agent_policy)
        self.CD1 = None # CD: community card
        self.CD2 = None
        self.CD3 = None
        self.CD4 = None
        self.CD5 = None
        self.state = 4
        self.chips_in_pool = 0
        self.card_in_use = set()
        self.current_call = 0
        self.trajectory = []
        self.iter = iter # use for output to file

    def start_game(self) -> int:
        self.compulsory_bets()
        prev_chips = self.players[self.agent].chips
        d = dict()
        if self.pre_flop():
            d['s'] = self.state * 10 + self.players[self.agent].rank
            self.players[self.agent].state = d['s']
            d['sp'] = FOLD
            d['a'] = 2
            if self.num_player == 1:
                d['r'] = self.chips_in_pool
            else:
                d['r'] = -1 * self.players[self.agent].chips
            self.trajectory.append(d)
            return d['r']

        # clear out
        for _, p in self.players.items():
            p.current_call = 0
        self.current_call = 0
        d = dict()
        if self.flop():
            d['s'] = self.state * 10 + self.players[self.agent].rank
            self.players[self.agent].state = d['s']
            d['sp'] = FOLD
            d['a'] = 2
            if self.num_player == 1:
                d['r'] = self.chips_in_pool
            else:
                d['r'] = -1 * self.players[self.agent].chips
            self.trajectory.append(d)
            return d['r']

        d = dict()
        d['s'] = self.state * 10 + self.players[self.agent].rank
        self.players[self.agent].state = d['s']
        d['sp'] = (self.state + 1) * 10 + self.players[self.agent].rank
        d['a'] = 1
        if self.num_player == 1: 
            d['r'] = self.chips_in_pool
            self.trajectory.append(d)
            return d['r']
        d['r'] = -1 * self.players[self.agent].chips
        self.trajectory.append(d)

        # clear out
        for _, p in self.players.items():
            p.current_call = 0
        self.current_call = 0
        d = dict()
        if self.turn():
            d['s'] = self.state * 10 + self.players[self.agent].rank
            self.players[self.agent].state = d['s']
            d['sp'] = FOLD
            d['a'] = 2
            if self.num_player == 1:
                d['r'] = self.chips_in_pool
            else:
                d['r'] = -1 * self.players[self.agent].chips
            self.trajectory.append(d)
            return d['r']

        d = dict()
        d['s'] = self.state * 10 + self.players[self.agent].rank
        self.players[self.agent].state = d['s']
        d['sp'] = (self.state + 1) * 10 + self.players[self.agent].rank
        d['a'] = 1
        if self.num_player == 1: 
            d['r'] = self.chips_in_pool
            self.trajectory.append(d)
            return d['r']
        d['r'] = -1 * self.players[self.agent].chips
        self.trajectory.append(d)

        # clear out
        for _, p in self.players.items():
            p.current_call = 0
        self.current_call = 0
        d = dict()
        if self.river():
            d['s'] = self.state * 10 + self.players[self.agent].rank
            self.players[self.agent].state = d['s']
            d['sp'] = FOLD
            d['a'] = 2
            if self.num_player == 1:
                d['r'] = self.chips_in_pool
            else:
                d['r'] = -1 * self.players[self.agent].chips
            self.trajectory.append(d)
            return d['r']
        
        d = dict()
        d['s'] = self.state * 10 + self.players[self.agent].rank
        self.players[self.agent].state = d['s']
        d['sp'] = (self.state + 1) * 10 + self.players[self.agent].rank
        d['a'] = 1
        if self.num_player == 1: 
            d['r'] = self.chips_in_pool
            self.trajectory.append(d)
            return d['r']
        d['r'] = -1 * self.players[self.agent].chips
        self.trajectory.append(d)

        d = dict()
        d['s'] = 30 + self.players[self.agent].rank
        self.players[self.agent].state = d['s']
        d['sp'] = 30 + self.players[self.agent].rank
        d['r'] = self.compute_reward()
        d['a'] = 1
        self.trajectory.append(d)

        return d['r']

    def compulsory_bets(self) -> None:
        for i, p in self.players.items():
            if i == self.num_player - 2:
                p.chips = 1
                p.current_call = 1
            if i == self.num_player - 1:
                p.chips = 2
                p.current_call = 2
        self.state = 5
        self.chips_in_pool = 3
        self.current_call = 2
    
    def pre_flop(self) -> bool:
        # deal two cards
        # each player acts
        for i, p in self.players.items():
            p.card1, p.card2 = self.deal_card(), self.deal_card()
        self.state = 0
        return self.betting_round()

    def flop(self) -> bool:
        # 3 community cards
        # each player acts
        self.state = 1
        self.CD1, self.CD2, self.CD3 = self.deal_card(), self.deal_card(), self.deal_card()
        return self.betting_round()
        

    def turn(self) -> bool:
        # 4th community card
        # each player acts
        self.state = 2
        self.CD4 = self.deal_card()
        return self.betting_round()

    def river(self) -> None:
        # 5th community card
        # each player acts
        self.state = 3
        self.CD5 = self.deal_card()
        return self.betting_round()

    '''
    Read information from the cards field in player.

    1: Royal Flush
    2: Straight Flush
    3: Four of a Kind
    4: Full House
    5: Flush
    6: Straight
    7: Three of a Kind
    8: Two Pair
    9: One Pair
    10: High Card
    '''
    def get_rank(self, player) -> None:
        # fill to 7 cards
        cards = set()
        cards.add(player.card1)
        cards.add(player.card2)

        cards.add(self.CD1)
        cards.add(self.CD2)
        cards.add(self.CD3)
        cards.add(self.CD4)
        cards.add(self.CD5)

        cards = set(filter(lambda item: item is not None, cards))

        while len(cards) != 7:
            cards.add((random.choice(COLOR), random.choice(NUMBER)))

        # start working on finding highest rank
        cards = list(cards)

        # find (royal) straight flush
        cards.sort(key = lambda x: (x[0], x[1]))
        cards_based_on_color = [[], [], [], []]
        for color, number in cards:
            cards_based_on_color[color].append((color, number))
        has_straight_flush = False
        straight_flush = []
        for l in cards_based_on_color:
            if len(l) < 5: continue
            # same color more than or equal to 5 cards
            if l[-1][1] - l[-5][1] == 4:
                has_straight_flush = True
                straight_flush = l[-5:-1]
                straight_flush.append(l[-1])
                break
            elif len(l) == 6:
                if l[-2][1] - l[-6][1] == 4:
                    has_straight_flush = True
                    straight_flush = l[-6:-1]
                    break
            elif len(l) == 7:
                if l[-3][1] - l[-7][1] == 4:
                    has_straight_flush = True
                    straight_flush = l[-7:-2]
                    break
        if has_straight_flush:
            if straight_flush[-1][1] == 13:
                player.rank = 0
                return
            player.rank = 1
            return

        # find four of a kind (number 4+1)
        cards.sort(key = lambda x: (x[1], x[0]))
        cards_based_on_number = [[] for _ in range(13)]
        for color, number in cards:
            cards_based_on_number[number - 1].append((color, number))
        if any([len(n) >= 4 for n in cards_based_on_number]):
            player.rank = 2
            return

        # find full house (number 3+2)
        has_3 = any([len(n) >= 3 for n in cards_based_on_number])
        if has_3:
            # need 2 pairs to ensure 3+2
            has_2 = 0
            for n in cards_based_on_number:
                if len(n) >= 2:
                    has_2 += 1
            if has_2 >= 2:
                player.rank = 3
                return

        # find flush (color 5)
        if any([len(n) >= 5 for n in cards_based_on_color]):
            player.rank = 4
            return

        # find straight
        has_straight = False
        for i in range(9):
            if len(cards_based_on_number[i]) == 0: continue
            if len(cards_based_on_number[i + 1]) == 0: continue
            if len(cards_based_on_number[i + 2]) == 0: continue
            if len(cards_based_on_number[i + 3]) == 0: continue
            if len(cards_based_on_number[i + 4]) == 0: continue
            has_straight = True
            break
        if has_straight:
            player.rank = 5
            return

        # find three of a kind (number 3+1+1)
        if has_3:
            player.rank = 6
            return

        # find two pairs (number 2+2+1)
        has_2 = 0
        for n in cards_based_on_number:
            if len(n) >= 2:
                has_2 += 1
        if has_2 >= 2:
            player.rank = 7
            return

        # find pair
        if any([len(n) >= 2 for n in cards_based_on_number]):
            player.rank = 8
            return

        player.rank = 9
        return 9

    '''
    Breaks the tie.
    If the agent loses with the same rank, return False and any number.
    If the agent wins the tie, return True and the number of other candidates with the same winning status.
    '''
    def get_winner(self, rank, candidates) -> Tuple(bool, int):
        cards = [self.CD1, self.CD2, self.CD3, self.CD4, self.CD5]

        agent_set = list(cards)
        agent_set.append(self.players[self.agent].card1)
        agent_set.append(self.players[self.agent].card2)
        agent_set.sort(key = lambda x: (x[1], x[0]))

        # high card
        if rank == 9:
            num = 1
            for p in candidates:
                p_set = list(cards)
                p_set.append(p.card1)
                p_set.append(p.card2)
                p_set.sort(key = lambda x: (x[1], x[0]))
                tie = True
                for i in [-1, -2, -3, -4, -5]:
                    if agent_set[i][1] > p_set[i][1]:
                        tie = False
                        break
                    elif agent_set[i][1] < p_set[i][1]:
                        return False, 0
                if tie: num += 1
            return True, num
        # one pair
        elif rank == 8:
            agent_set_based_on_number = [0 for _ in range(13)]
            agent_pair_max = 1
            num = 1
            for _, number in agent_set:
                agent_set_based_on_number[number - 1] += 1
                if agent_set_based_on_number[number - 1] == 2: agent_pair_max = number
            for p in candidates:
                p_set = list(cards)
                p_set.append(p.card1)
                p_set.append(p.card2)
                p_set.sort(key = lambda x: (x[1], x[0]))
                p_set_based_on_number = [0 for _ in range(13)]
                p_pair_max = 1
                for _, number in p_set:
                    p_set_based_on_number[number - 1] += 1
                    if p_set_based_on_number[number - 1] == 2: p_pair_max = number
                if p_pair_max > agent_pair_max: return False, 0
                if p_pair_max < agent_pair_max: continue
                a_list = [s for (_, s) in agent_set]
                a_list.remove(agent_pair_max)
                a_list.remove(agent_pair_max)
                p_set = [s for (_, s) in p_set]
                p_set.remove(p_pair_max)
                p_set.remove(p_pair_max)
                tie = True
                a_list.sort()
                p_set.sort()
                for i in [-1, -2, -3]:
                    if a_list[i] > p_set[i]:
                        tie = False
                        break
                    if a_list[i] < p_set[i]: return False, 0
                if tie: num += 1
            return True, num
        # two pairs
        elif rank == 7:
            agent_set_based_on_number = [0 for _ in range(13)]
            agent_pair_max_list = []
            num = 1
            for _, number in agent_set:
                agent_set_based_on_number[number - 1] += 1
                if agent_set_based_on_number[number - 1] == 2: agent_pair_max_list.append(number)
            agent_pair_max_list.sort()
            for p in candidates:
                p_set = list(cards)
                p_set.append(p.card1)
                p_set.append(p.card2)
                p_set.sort(key = lambda x: (x[1], x[0]))
                p_set_based_on_number = [0 for _ in range(13)]
                p_pair_max_list = []
                for _, number in p_set:
                    p_set_based_on_number[number - 1] += 1
                    if p_set_based_on_number[number - 1] == 2: p_pair_max_list.append(number)
                p_pair_max_list.sort()
                if p_pair_max_list[-1] > agent_pair_max_list[-1]: return False, 0
                if p_pair_max_list[-1] < agent_pair_max_list[-1]: continue
                if p_pair_max_list[0] > agent_pair_max_list[0]: return False, 0
                if p_pair_max_list[0] < agent_pair_max_list[0]: continue
                a_list = [s for (_, s) in agent_set]
                a_list.remove(agent_pair_max_list[0])
                a_list.remove(agent_pair_max_list[0])
                a_list.remove(agent_pair_max_list[1])
                a_list.remove(agent_pair_max_list[1])
                p_set = [s for (_, s) in p_set]
                p_set.remove(p_pair_max_list[0])
                p_set.remove(p_pair_max_list[0])
                p_set.remove(p_pair_max_list[1])
                p_set.remove(p_pair_max_list[1])
                if max(a_list) > max(p_set): continue
                if max(a_list) < max(p_set): return False, 0
                num += 1
            return True, num
        # three of a kind
        elif rank == 6:
            agent_set_based_on_number = [0 for _ in range(13)]
            agent_three_max = 1
            num = 1
            for _, number in agent_set:
                agent_set_based_on_number[number - 1] += 1
                if agent_set_based_on_number[number - 1] == 3: agent_three_max = number
            for p in candidates:
                p_set = list(cards)
                p_set.append(p.card1)
                p_set.append(p.card2)
                p_set.sort(key = lambda x: (x[1], x[0]))
                p_set_based_on_number = [0 for _ in range(13)]
                p_three_max = 1
                for _, number in p_set:
                    p_set_based_on_number[number - 1] += 1
                    if p_set_based_on_number[number - 1] == 2: p_three_max = number
                if p_three_max > agent_three_max: return False, 0
                if p_three_max < agent_three_max: continue
                tie = True
                a_list = [s for (_, s) in agent_set]
                a_list.remove(agent_three_max)
                a_list.remove(agent_three_max)
                a_list.remove(agent_three_max)
                p_set = [s for (_, s) in p_set]
                p_set.remove(p_three_max)
                p_set.remove(p_three_max)
                p_set.remove(p_three_max)
                for i in [-1, -2]:
                    if a_list[i] < p_set[i]: return False, 0
                    if a_list[i] > p_set[i]:
                        tie = False
                        break
                if tie: num += 1
            return True, num
        # straight or straight flush
        elif (rank == 5) or (rank == 1):
            agent_highest_straight = 1
            agent_set_based_on_number = [0 for _ in range(13)]
            num = 1
            for _, number in agent_set:
                agent_set_based_on_number[number - 1] += 1
            for i in [12, 10, 9, 8, 7, 6, 5]:
                if agent_set_based_on_number[i] == 0: continue
                if agent_set_based_on_number[i - 1] == 0: continue
                if agent_set_based_on_number[i - 2] == 0: continue
                if agent_set_based_on_number[i - 3] == 0: continue
                if agent_set_based_on_number[i - 4] == 0: continue
                agent_highest_straight = i
                break
            for p in candidates:
                p_set = list(cards)
                p_set.append(p.card1)
                p_set.append(p.card2)
                p_set.sort(key = lambda x: (x[1], x[0]))
                p_set_based_on_number = [0 for _ in range(13)]
                p_highest_straight = 1
                for _, number in p_set:
                    p_set_based_on_number[number - 1] += 1
                for i in [12, 10, 9, 8, 7, 6, 5]:
                    if p_set_based_on_number[i] == 0: continue
                    if p_set_based_on_number[i - 1] == 0: continue
                    if p_set_based_on_number[i - 2] == 0: continue
                    if p_set_based_on_number[i - 3] == 0: continue
                    if p_set_based_on_number[i - 4] == 0: continue
                    p_highest_straight = i
                    break
                if p_highest_straight > agent_highest_straight: return False, 0
                if p_highest_straight == agent_highest_straight:
                    num += 1
            return True, num
        # flush
        elif rank == 4:
            agent_based_on_color = [[], [], [], []]
            for color, number in agent_set:
                agent_based_on_color[color].append(number)
            if len(agent_based_on_color[0]) >= 5: agent_cards = agent_based_on_color[0]
            elif len(agent_based_on_color[1]) >= 5: agent_cards = agent_based_on_color[1]
            elif len(agent_based_on_color[2]) >= 5: agent_cards = agent_based_on_color[2]
            else: agent_cards = agent_based_on_color[3]
            agent_cards.sort()
            num = 1
            for p in candidates:
                p_set = list(cards)
                p_set.append(p.card1)
                p_set.append(p.card2)
                p_based_on_color = [[], [], [], []]
                for color, number in p_set:
                    p_based_on_color[color].append(number)
                if len(p_based_on_color[0]) >= 5: p_cards = p_based_on_color[0]
                elif len(p_based_on_color[1]) >= 5: p_cards = p_based_on_color[1]
                elif len(p_based_on_color[2]) >= 5: p_cards = p_based_on_color[2]
                else: p_cards = p_based_on_color[3]
                p_cards.sort()
                tie = True
                for i in [4, 3, 2, 1, 0]:
                    if p_cards[i] > agent_cards[i]: return False, 0
                    if p_cards[i] < agent_cards[i]:
                        tie = False
                        break
                if tie: num += 1
                return True, num
        # full house
        elif rank == 3:
            agent_set_based_on_number = [0 for _ in range(13)]
            agent_three = 1
            agent_two = 1
            num = 1
            for _, number in agent_set:
                agent_set_based_on_number[number - 1] += 1
            for i, n in enumerate(agent_set_based_on_number):
                if n == 3: agent_three = i + 1
                if n == 2: agent_two = i + 1
            for p in candidates:
                p_set = list(cards)
                p_set.append(p.card1)
                p_set.append(p.card2)
                p_set.sort(key = lambda x: (x[1], x[0]))
                p_set_based_on_number = [0 for _ in range(13)]
                p_three = 1
                p_two = 1
                for _, number in p_set:
                    p_set_based_on_number[number - 1] += 1
                for i, n in enumerate(p_set_based_on_number):
                    if n == 3: p_three = i + 1
                    if n == 2: p_two = i + 1
                if p_three > agent_three: return False, 0
                if p_three < agent_three: continue
                if p_two > agent_two: return False, 0
                if p_two < agent_two: continue
                num += 1
            return True, num
        # four of a kind
        elif rank == 2:
            agent_set_based_on_number = [0 for _ in range(13)]
            agent_four = 1
            num = 1
            for _, number in agent_set:
                agent_set_based_on_number[number - 1] += 1
                if agent_set_based_on_number[number - 1] == 4: agent_four = number
            for p in candidates:
                p_set = list(cards)
                p_set.append(p.card1)
                p_set.append(p.card2)
                p_set.sort(key = lambda x: (x[1], x[0]))
                p_set_based_on_number = [0 for _ in range(13)]
                p_four = 1
                for _, number in p_set:
                    p_set_based_on_number[number - 1] += 1
                    if p_set_based_on_number[number - 1] == 2: p_four = number
                if p_four > agent_four: return False, 0
                if p_four < agent_four: continue
                tie = True
                a_list = [s for (_, s) in agent_set]
                a_list.remove(agent_four)
                a_list.remove(agent_four)
                a_list.remove(agent_four)
                a_list.remove(agent_four)
                p_set = [s for (_, s) in p_set]
                p_set.remove(p_four)
                p_set.remove(p_four)
                p_set.remove(p_four)
                p_set.remove(p_four)
                a_list.sort()
                if max(a_list) < max(p_set): return False, 0
                if max(a_list) > max(p_set): continue
                num += 1
            return True, num
        # royal flush
        else:
            return True, len(candidates)

    '''
    Only computes the reward of the agent.
    Assume to be at state 5.
    '''
    def compute_reward(self) -> int:
        if self.num_player == 1: return self.chips_in_pool
        tie_list = []
        self.get_rank(self.players[self.agent])
        for i, p in self.players.items():
            if i == self.agent: continue
            self.get_rank(p)
            # if other player wins
            if p.rank < self.players[self.agent].rank:
                return -1 * self.players[self.agent].chips
            # if ties
            if p.rank == self.players[self.agent].rank:
                tie_list.append(p)
        if len(tie_list) == 0: return self.chips_in_pool
        win, num = self.get_winner(self.players[self.agent].rank, tie_list)
        if win: return self.chips_in_pool // num
        return -1 * self.players[self.agent].chips

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
                self.get_rank(p)
                action = p.get_action(self.players[self.agent].state)
                if action == 2:
                    return True
            # non agent
            else:
                self.get_rank(p)
                action = p.get_action(p.rank)
                if action == 2:
                    self.num_player -= 1
                    del self.players[i]
            
            # not folding
            if action == 0:
                self.players[i].current_call += self.raise_amount
                self.chips_in_pool += self.raise_amount
                self.players[i].chips += self.raise_amount
                self.current_call = self.players[i].current_call
                finished = False

                # update trajectory
                if i == self.agent:
                    d = dict()
                    d['s'] = self.state * 10 + self.players[self.agent].rank
                    self.players[self.agent].state = d['s']
                    d['a'] = action
                    d['r'] = -1 * self.players[self.agent].chips
                    d['sp'] = self.state * 10 + self.players[self.agent].rank
                    self.trajectory.append(d)
            elif action == 1:
                self.chips_in_pool += (self.current_call - self.players[i].current_call)
                self.players[i].chips += (self.current_call - self.players[i].current_call)
                self.players[i].current_call = self.current_call
                finished &= True

                # update trajectory
                if i == self.agent:
                    d = dict()
                    d['s'] = self.state * 10 + self.players[self.agent].rank
                    self.players[self.agent].state = d['s']
                    d['a'] = action
                    d['r'] = -1 * self.players[self.agent].chips
                    d['sp'] = self.state * 10 + self.players[self.agent].rank
                    self.trajectory.append(d)
        if finished: return False

        # second round -> only check or fold
        temp_dict = dict(self.players)
        for i, p in temp_dict.items():
            # agent
            if i == self.agent:
                self.get_rank(p)
                action = p.get_action(self.players[self.agent].state)
                if action == 2:
                    return True
            # non agent
            else:
                self.get_rank(p)
                action = p.get_action(p.rank)
                if action == 2:
                    self.num_player -= 1
                    del self.players[i]

            # not folding
            if action == 0 or action == 1:
                self.chips_in_pool += (self.current_call - self.players[i].current_call)
                self.players[i].chips += (self.current_call - self.players[i].current_call)
                self.players[i].current_call = self.current_call

        return False

    def output_to_file(self, file_name) -> None:
        fields = ['s', 'r', 'a', 'sp']
        if self.iter == 0:
            with open(file_name, 'w', newline='') as file: 
                writer = csv.DictWriter(file, fieldnames = fields)
                writer.writeheader() 
                writer.writerows(self.trajectory)
        else:
            with open(file_name, 'a', newline='') as file: 
                writer = csv.DictWriter(file, fieldnames = fields)
                writer.writerows(self.trajectory)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--iterations", help="number of iterations", type=int, required=False, default=5)
    parser.add_argument("-i", "--input", help="input file", type=str, required=False, default='big.policy')
    parser.add_argument("-o", "--output", help="output file", type=str, required=False, default='big.csv')
    parser.add_argument("-g", "--agent_number", help="agent number", type=int, required=False, default=0)
    parser.add_argument("-a", "--raise_amount", help="raise amount", type=int, required=False, default=5)
    parser.add_argument("-n1", "--n1", help="n1", type=int, required=False, default=8)
    parser.add_argument("-n2", "--n2", help="n2", type=int, required=False, default=9)
    parser.add_argument("-l1", "--l1", help="l1", type=int, required=False, default=70)
    parser.add_argument("-l2", "--l2", help="l2", type=int, required=False, default=20)
    parser.add_argument("-l3", "--l3", help="l3", type=int, required=False, default=10)
    args = parser.parse_args()
    for i in range(args.iterations):
        print("Round {}:".format(i))
        g = game(agent_no = args.agent_number, agent_policy = args.input, iter = i, raise_amount= args.raise_amount, n1 = args.n1, n2 = args.n2, l1 = args.l1, l2 = args.l2, l3 = args.l3)
        print(g.start_game())
        # print(g.players)
        # print(g.CD1, g.CD2, g.CD3, g.CD4, g.CD5)
        # print(g.chips_in_pool)
        # print(g.trajectory)
        g.output_to_file(args.output)
    # l = [(2, 4), (3, 8), (1, 11), (1, 1), (3, 3), (0, 5), (1, 9)]
    # g = game(agent_policy='random')
    # g.CD1 = l[0]
    # g.CD2 = l[1]
    # g.CD3 = l[2]
    # g.CD4 = l[3]
    # g.CD5 = l[4]
    # g.players[g.agent].card1 = l[5]
    # g.players[g.agent].card2 = l[6]
    # g.get_rank(g.players[g.agent])
    # print(g.players[g.agent].rank)