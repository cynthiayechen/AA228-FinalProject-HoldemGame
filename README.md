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
Three optional parameters for game_master_more_states.py:
- number of iterations (default 5)
- input file name (.policy) for the agent (default big.policy)
- output file name (.csv) to output state transitions (default big.csv)
```
python3 game_master_more_states.py [-n <*iter*>] [-i <*input_name>] [-o <*output_name*>]
```
