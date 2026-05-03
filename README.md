# sudoku solver 

This project entails a backtracking Sudoku solver that uses the Minimum Remaining Value (MRV) heuristic and forward checking to solve puzzles fast. Tested against hundreds of boards from easy to near-impossible difficulty. This project is intended to model a constrant satisfaction problem.  [Try the game yourself here!](sudoku.com)

## about this project 
Sudoku is modeled as a Constraint Satisfaction Problem (CSP) with 81 variables (one per cell) each with a domain of 1 through 9. The constraints are the following: no two cells in the same row, column, or 3x3 box can share the same value. The board is represented as a Python dictionary where keys are cell names like A1, B3, I9 and values are the digits placed there. Empty cells are initialized to zero.

## algorithm 
uses: backtracking search with MRV, forward checking

- Rather than trying every possible combination blindly, the solver picks the next cell to fill using the Minimum Remaining Value heuristic; it always chooses the cell with the fewest legal values left in its domain. This dramatically cuts down the search space because the most constrained cells get resolved first, catching dead ends early.
- After placing a value, forward checking immediately updates the domains of all related cells in the same row, column, and box. If any cell's domain becomes empty, the solver backtracks right away instead of continuing down a dead end.
- The combination of these two techniques means most puzzles solve in well under a second

## project structure 
```
sudoku-solver/
    sudoku.py              # Core solver, backtracking, MRV heuristic, forward checking
    sudoku_tester.py       # Batch tests solver against all boards and reports stats
    sudokus_start.txt      # Hundreds of unsolved puzzle boards
    sudokus_finish.txt     # Corresponding solved boards for verification
    README.txt             # Runtime statistics across all puzzles
```

## how to run: 
1. Solve a single board by passing it as a string argument:
`python3 sudoku.py 003020600900305001001806400008102900700000008006708200002609500800203009005010300` 
2. This generates output.txt containing the completed board on a single line: 483921657967345821251876493548132976729564138136798245372689514814253769695417382
3. Run against all boards in the test file:
`python3 sudoku_tester.py` 
4. Input Format: Boards are passed as an 81-character string, read left to right, top to bottom. Zeros represent empty cells (for example:
```
003020600
900305001
001806400
008102900
700000008
006708200
002609500
800203009
005010300
becomes 003020600900305001001806400008102900700000008006708200002609500800203009005010300
```

## performance: 
- Boards solved (out of total in sudokus_start.txt), Mean runtime, Min runtime, Max runtime, Std deviation

## hard mode: 
- The solver also handles some of the hardest known Sudoku puzzles. This one is considered one of the most difficult ever constructed:
800000000003600000070090200050007000000045700000100030001000068008500010090000400
- Solution: 812753649943682175675491283154237896369845721287169534521974368438526917796318452

Requirements: Python 3, no external dependencies

Notes
- Brute force approaches will time out. The MRV heuristic combined with forward checking is what keeps the solver fast enough to handle hundreds of boards without breaking a sweat. If you want to push it further, AC-3 constraint propagation is a natural next step for reducing domains before search even begins.
