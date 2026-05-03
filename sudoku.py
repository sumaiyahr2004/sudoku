#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys

ROW = "ABCDEFGHI"
COL = "123456789"

def get_neighbors(cell):
    """
    Goal: to return all cells that share a constraint with the given cell.
    Define neighbors as cells in the same row, column, or 3x3 box 
    """
    row = cell[0]
    col = cell[1]

    neighbors = set()

    for c in COL:
        neighbors.add(row + c)

    for r in ROW:
        neighbors.add(r + col)

    row_start = (ROW.index(row)//3)*3
    col_start = (COL.index(col)//3)*3

    for r in ROW[row_start:row_start+3]:
        for c in COL[col_start:col_start+3]:
            neighbors.add(r+c)

    neighbors.remove(cell)
    return neighbors

def get_domains(board):
    """
    Goal: to return the domain of each cell in the board 
    Define domain of a cell as the set of all possible values it can take 
    """
    domains = {}

    for cell in board:
        if board[cell] != 0:
            domains[cell] = {board[cell]}
        else:
            possible = set(range(1,10))

            for neighbor in get_neighbors(cell):
                val = board[neighbor]
                if val != 0 and val in possible:
                    possible.remove(val)

            domains[cell] = possible

    return domains

def select_unassigned_variable(board, domains):
    """
    Implement MRV, choose unassigned variable (cell with value 0)
    that has smallest domain 
    """
    unassigned = [v for v in board if board[v] == 0]
    return min(unassigned, key=lambda v: len(domains[v]))

def forward_check(cell, value, domains, neighbors):
    """
    Goal is to perform forward checking after assigning a value

    Also want to remove the assigned value from the domains of neighboring cells
    Also If any neighbor loses all possible values, fails.
    """
    removed = []

    for n in neighbors[cell]:
        if value in domains[n]:
            domains[n].remove(value)
            removed.append((n,value))

            if len(domains[n]) == 0:
                return False, removed

    return True, removed

def restore_domains(domains, removed):
    """
    Will restore domain values removed during forward checking when backtracking occurs 
    """
    for var,val in removed:
        domains[var].add(val)

def backtrack(board, domains, neighbors):
    """
    This is recursive backtracking search for solving the Sudoku 
    """

    if all(board[v] != 0 for v in board):
        return True

    var = select_unassigned_variable(board, domains)

    for value in sorted(domains[var]):

        board[var] = value

        old_domain = domains[var] 
        domains[var] = {value} 

        ok, removed = forward_check(var, value, domains, neighbors)

        if ok:
            if backtrack(board, domains, neighbors):
                return True

        restore_domains(domains, removed)
        domains[var] = old_domain
        board[var] = 0


    return False


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def backtracking(board):
    """Takes a board and returns solved board."""
    # TODO: implement this
    domains = get_domains(board)

    neighbors = {}
    for cell in board:
        neighbors[cell] = get_neighbors(cell)

    backtrack(board, domains, neighbors)
    solved_board = board
    return solved_board


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if len(sys.argv[1]) != 81:
            print("Input string must be exactly 81 characters long")
            exit()

        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(sys.argv[1][9*r+c])
                  for r in range(9) for c in range(9)}       
        
        solved_board = backtracking(board)
        
        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')
    else:
        print("Usage: python3 sudoku.py <input string>")
    
    print("Finishing all boards in file.")
