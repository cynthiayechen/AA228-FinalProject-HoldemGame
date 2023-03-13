# AA228-FinalProject-HoldemGame
Final Project for CS238/AA228 Decision Making Under Uncertainty
Policy Learner for poker Texas Holdem with our self implemented game simulator

## File Structure

```
.
├── LICENSE
├── README.md      // this file
├── small.csv      // input file to the policy learner; output file from the game master
├── small.policy   // output file to the policy learner; input file from the game master
└── game_master.py // the game simulator for Texas Holdem
```

## Running the simulator
Three optional parameters:
- number of iterations (default 5)
- input file name (.policy) for the agent (default small.policy)
- output file name (.csv) to output state transitions (Default small.csv)
```
python3 game_master.py <*iter*> [-i <*input_name>] [-o <*output_name*>]
```
