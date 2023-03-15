# AA228-FinalProject-HoldemGame
Final Project for CS238/AA228 Decision Making Under Uncertainty

Policy Learner for poker Texas Holdem with our self implemented game simulator

## File Structure

```
.
├── LICENSE
├── README.md                  // this file
├── small.csv                  // example input file to the policy learner; example output file from the game master
├── small.policy               // example output file to the policy learner; example input file from the game master
├── game_master.py             // the game simulator for Texas Holdem
├── big.csv                    // example input file to the policy learner; example output file from the game master (more states)
├── big.policy                 // example output file to the policy learner; example input file from the game master (more states)
└── game_master_more_states.py // the game simulator with more transition states for Texas Holdem
```

## Running the simulator
Three optional parameters for game_master.py:
- number of iterations (default 5)
- input file name (.policy) for the agent (default small.policy)
- output file name (.csv) to output state transitions (default small.csv)
```
python3 game_master.py [-n <*iter*>] [-i <*input_name>] [-o <*output_name*>]
```
For more information, try `python3 game_master.py -h` for the helper information.
Ten optional parameters for game_master_more_states.py:
- number of iterations (default 5)
- input file name (.policy) for the agent (default big.policy)
- output file name (.csv) to output state transitions (default big.csv)
- the number of the agent assming big blind has number -2 and small blind has number -1 (default 0)
- the amount per raise (default 5)
- 5 parameters defining behavior of a non-agent player (default 8 9 70 20 10)
    - n1 and n2 define three disjoint intervals of the ranking
    - l1 through l3 define three percentages, need to add up to 100
```
python3 game_master_more_states.py [-n <*iter*>] [-i <*input_name>] [-o <*output_name*>] [-g <*agent_number*>] [-a <*raise_amount*>] [-n1 <*n1*>] [-n2 <*n2*>] [-l1 <*l1*>] [-l2 <*l2*>] [-l3 <*l3*>]
```
For more information, try `python3 game_master_more_states.py -h` for the helper information.


## Note
The .policy file for *game_master* should contain exactly 6 lines, where the 2nd to 5th line contain useful information.
The .policy file for *game_master_more_states* should contain exactly 42 lines, where the 1st to 40th line contain useful information.