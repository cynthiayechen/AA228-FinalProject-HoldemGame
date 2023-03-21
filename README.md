# AA228-FinalProject-HoldemGame
Final Project for CS238/AA228 Decision Making Under Uncertainty

Policy Learner for poker Texas Holdem with our self implemented game simulator

## File Structure

```
.
├── LICENSE
├── README.md                   // this file
├── small.csv                   // example input file to the policy learner; example output file from the game master
├── small.policy                // example output file to the policy learner; example input file from the game master
├── game_master.py              // the game simulator for Texas Holdem
├── big.csv                     // example input file to the policy learner; example output file from the game master (more states)
├── big.policy                  // example output file to the policy learner; example input file from the game master (more states)
├── game_master_more_states.py  // the game simulator with more transition states for Texas Holdem
├── policy_model.py             // the policy model contains sarsa & q-learning algorithm
├── random_policy_big.policy    // the random policy for big.csv (52-state dataset) for model evaluation
├── random_policy_small.policy  // the random policy for small.csv (6-state dataset) for model evaluation
├── big_q_learning.policy       // the trained q-learning policy for big.csv (52-state dataset)
├── big_sarsa_learning.policy   // the trained sarsa policy for big.csv (52-state dataset)
├── small_q_learning.policy     // the trained q-learning policy for small.csv (6-state dataset)
└── small_sarsa_learning.policy // the trained sarsa policy for small.csv (6-state dataset)
```

## Running the simulator
`game_master.py` and `game_master_more_states.py` are the two simulators. The first one runs the simulator for the 6-state simulator, while the latter onr refers to the 52-state simulator. They have the same set of potential command line arguments. Here is the explanation for `game_master.py`:
Four optional command line arguments:
- -s: whether in simulator mode or not
- -n: number of iterations (default 10000)
- -i: input file name (.policy) for the agent (default small.policy)
- -o: output file name (.csv) to output state transitions (default small.csv)
- -g: the position of the agent player (default 0)
- -a: the raise amount (default 5)
- -n1n2: two ints indicating the rank division (default [3, 7])
- -p1: three ints indicating raising, checking, folding probabilities in rank 1 (default [90, 9, 1])
- -p2: three ints indicating raising, checking, folding probabilities in rank 2 (default [40, 50, 10])
- -p3: three ints indicating raising, checking, folding probabilities in rank 3 (default [10, 80, 10])
```
python3 game_master.py [-s] [-n <*iter*>] [-i <*input_name>] [-o <*output_name*>] [-g <*agent_number*>] [-a <*raise_amount*>] [-n1n2 <*n1 n2*>] [-p1 <*a b c*>] [-p2 <*a b c*>] [-p3 <*a b c*>]
```
For more information, try `python3 game_master.py -h` for the helper information.

## Note
The .policy file for *game_master* should contain exactly 6 lines, where the 2nd to 5th line contain useful information.
The .policy file for *game_master_more_states* should contain exactly 52 lines, where the 1st to 50th line contain useful information.

## Running the policy model
`policy_model.py` is our reinforcement learning model (q-learning and sarsa). The command to run the model is: 
```
python3 policy_model.py
```
which will output new `big_q_learning.policy`, `big_sarsa_learning.policy`, `small_q_learning.policy`, and `small_sarsa_learning.policy` that trained based on current `big.csv` and `small.csv`.
