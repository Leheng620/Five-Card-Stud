# Five Card Stud

## Online Demo (currently only support two players, one human player and one AI player)
[Try it out: Five Card Stud Online Demo](https://five-card-stud.herokuapp.com/)

## Test the game locally
**Make sure you are in the master branch**
#### Run the game simulation locally
- Clone the repository

    ```git clone https://github.com/Leheng620/Five-Card-Stud.git```

- Install dependencies:

    ```pip install -r requirements.txt```

- At the root directory, run

    ```python five_card_stud/game.py <option> <num_of_game_play>```
    
    Replace `<option>` with the following:
    
    - To run simulation between Random agent and Uniform agent:
    
        `<option>`: `random_vs_uniform`
        
    - To run simulation between MCTS agent and Uniform agent:
    
        `<option>`: `mcts_vs_uniform <iteration>`, `<iteration>` is the number of iterations the MCTS agents will run. Minimum 100.
    
    - To run simulation between MCTS agent and Random agent:
    
        `<option>`: `mcts_vs_random <iteration>`
        
    - To run simulation between MCTS agent and MCTS agent:
    
        `<option>`: `mcts_vs_mcts <iteration> <iteration>`
        The first `<iteration>` is the number of iterations the first MCTS agent will run.
        The second `<iteration>` is the number of iterations the second MCTS agent will run.

    `<num_of_game_play>` is the number of games to simulate. A game ends when an agent runs out of balance.

    After the simulation ends, a counter object will be printed out. The player 0 is the player before "vs" in `<option>`, player 1 is the player after "vs" in `<option>`

#### Play games with a MCTS agent (Our best agent so far) in command line. You can also try the online demo
`python five_card_stud/test_human.py`

#### Run tests
`test_efficiency.py` contains the script to test algorithm running time, the argument is the same as `game.py` except that we fix the number of game plays to be 100.

`test_mcts_iter.py` tests the MCTS agent with different iteration numbers.

`test_mcts_ucb.py` tries different values of the constant `c` in the UCB score in MCTS algorithm.

---

## Concepts
### Agent
#### Uniform agent
Takes available actions randomly with no bias.

#### Random agent
Takes available actions randomly based on weighted probability. The weight is the heuristics.

#### MCTS agent
An agent that is equipped with Monte Carlo Tree Search algorithm to take the best actions given the current state of the game.



### Environment
Defined in `gameState.py`. Currently there can be two players only, and the card deck only contains 26 cards from 8 to A.


## Simulation Result

- Random Agent vs Uniform Agent
    - Run with command `python five_card_stud/game.py random_vs_uniform 1000`
    - Result: Counter({0: 896, 1: 104})

- MCTS Agent with iteration == 100 vs Uniform Agent
    - Run with command `python five_card_stud/game.py mcts_vs_uniform 100 1000`
    - Result: Counter({0: 913, 1: 87})

- MCTS Agent with iteration == 100 vs Random Agent
    - Run with command `python five_card_stud/game.py mcts_vs_random 100 1000`
    - Result: Counter({0: 601, 1: 399})

- MCTS Agent with iteration == 100 vs MCTS Agent with iteration == 1000
    - Run with command `python five_card_stud/game.py mcts_vs_mcts 100 1000 1000`
    - Result: Counter({0: 505, 1: 495})
