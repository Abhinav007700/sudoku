from flask import Flask, render_template, jsonify, session
import random
import copy
def is_valid(board, row, col, num):
    # Check if the number can be placed in the given position
    for i in range(9):
        if board[row][i] == num or board[i][col] == num or board[3 * (row // 3) + i // 3][3 * (col // 3) + i % 3] == num:
            return False
    return True

def solve_sudoku(board):
    # Find an empty position
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                # Try placing numbers 1-9
                for num in range(1, 10):
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        # Recursively try to solve the rest of the puzzle
                        if solve_sudoku(board):
                            return True
                        # If placing the number leads to an invalid solution, backtrack
                        board[i][j] = 0
                return False
    return True

def generate_sudoku_solution():
    # Start with an empty 9x9 grid
    board = [[0 for _ in range(9)] for _ in range(9)]

    # Solve the Sudoku puzzle
    solve_sudoku(board)

    return board

def print_sudoku(board):
    for row in board:
        print(row)

def remove_numbers(board, difficulty):
    # Flatten the board for easier manipulation
    flat_board = [num for row in board for num in row]

    # Determine the number of cells to remove based on difficulty
    cells_to_remove = int(difficulty * 81)  # Convert to integer for slicing

    # Create a list of indices to choose cells to remove
    indices = list(range(81))
    random.shuffle(indices)

    # Remove numbers while ensuring the puzzle remains unique and solvable
    for index in indices[:cells_to_remove]:
        row, col = divmod(index, 9)  # Convert flat index to row and column
        original_value = board[row][col]
        board[row][col] = 0

        # Check if the puzzle still has a unique solution
        if not has_unique_solution(board):
            board[row][col] = original_value  # Revert the change if the solution is not unique

    return board


def has_unique_solution(board):
    # Check if the Sudoku puzzle has a unique solution
    solutions = []
    solve_sudoku_1(board, solutions)
    return len(solutions) == 1

def solve_sudoku_1(board, solutions):
    # Backtracking algorithm to find all solutions to the Sudoku puzzle
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for num in range(1, 10):
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        solve_sudoku_1(board, solutions)
                        board[i][j] = 0
                return
    # If no empty cell is found, add the solution to the list
    solutions.append(board)

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    solved_board = generate_sudoku_solution()
    tmp=copy.deepcopy(solved_board)
    difficulty_level = 0.5
    puzzle_board = remove_numbers(tmp, difficulty_level)
    session['sb']=solved_board
    return render_template('game.html', puzzle_board=puzzle_board)

@app.route('/get_solution_matrix', methods=['GET'])
def get_solution_matrix():
    solved_board=session.get('sb')
    print(solved_board)
    return jsonify({'solved_board': solved_board})

if __name__ == '__main__':
    app.run(debug=True)