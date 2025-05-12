import random #need a random module to allow random selection
from dataclasses import dataclass #define simple data containers???
from typing import List, Optional #???



#columnlabels for reference
COLUMN_LABELS = {
    4: ["A", "B", "C", "D"], #easy game = 4 
    9: ["A", "B", "C", "D", "E", "F", "G", "H", "I"] #hard game = 9
}

#data modelling 
#sudoku board
@dataclass(frozen=True) #can not change 
class SudokuBoard:
    puzzle: List[List[int]]
    solution: List[List[int]]
    size: int
    blanks: int


# create a fully solved board using backtracking
def generate_solved_board(size: int) -> List[List[int]]:
    board = [[0] * size for _ in range(size)]
    solve_board(board)
    return board


# create the puzzle 
# removes numbers creating blanks from the solvedboard
def create_puzzle(full_board: List[List[int]], blanks: int) -> List[List[int]]:
    puzzle = [row[:] for row in full_board]
    size = len(puzzle)
    count = 0
    while count < blanks:
        row, col = random.randint(0, size - 1), random.randint(0, size - 1)
        if puzzle[row][col] != 0:
            puzzle[row][col] = 0
            count += 1
    return puzzle


# the full game
def get_board_with_blanks(size: int) -> SudokuBoard:
    blanks = 8 if size == 4 else 40 #easy games = 8 blanks and harder games= 40 blanks
    solution = generate_solved_board(size)
    puzzle = create_puzzle(solution, blanks)
    return SudokuBoard(puzzle=puzzle, solution=solution, size=size, blanks=blanks)


# print the the board
def print_board(board: List[List[int]]) -> None:
    size = len(board)
    labels = COLUMN_LABELS[size]

    print("\n   " + "  ".join(labels)) 
    
    for i in range(size):
        if i % int(size ** 0.5) == 0 and i != 0:
            print("   " + "-" * (size * 2 + (size // int(size ** 0.5)) - 1))
        row_str = f"{i + 1}  "
        for j in range(size):
            if j % int(size ** 0.5) == 0 and j != 0:
                row_str += "| "
            cell = board[i][j]
            row_str += str(cell) if cell != 0 else "."
            row_str += " "
        print(row_str)


#validation
#check if move is valid
def is_valid(board: List[List[int]], row: int, col: int, num: int) -> bool:
    size = len(board)
    box = int(size ** 0.5)
    if num in board[row]: return False
    if num in [board[i][col] for i in range(size)]: return False
    
    start_row, start_col = (row // box) * box, (col // box) * box
    
    for i in range(box):
        for j in range(box):
            if board[start_row + i][start_col + j] == num:
                return False
    return True


#solve the board using backtracking
def solve_board(board: List[List[int]]) -> bool:
    size = len(board) #get the size of the board
    for row in range(size): #go one by one thry the row
        for col in range(size):#go one by one thry the col
            if board[row][col] == 0: #checks if that spot is empty row/col
                for num in range(1, size + 1): #places numbers from 1> 
                    if is_valid(board, row, col, num): #>validation checks if thats the right number
                        board[row][col] = num #>place that number
                        if solve_board(board): #>tries to solve the board with the placed number
                            return True #>if it can be solved then send true back up this call stack
                        board[row][col] = 0 #>if cant solve then return false> backtrack to start set number to 0 and try next number
                return False #if tried all numbers and no solution then we backtrack returing false
    return True#this means boards solutions found, completed therefore return true


#main logic to play sudoku
def play_sudoku(name: str, size: int):
    board_model = get_board_with_blanks(size)
    board = [row[:] for row in board_model.puzzle]
    solution = board_model.solution

    print(f"\n{name}, here is your Sudoku puzzle!")
    print_board(board)
    print("Enter moves like 'A1 2'. Enter 'q' to quit.")

    wrong_attempts = 0
    while True:
        move = input("Move (e.g A1 2): ").strip().upper()

        if move.lower() == 'q':
            print("You have quit the game.")
            return
        try:
            parts = move.split()
            if len(parts) != 2: raise ValueError
            col_letter, row_char = parts[0][0], parts[0][1]
            row = int(row_char) - 1
            col = COLUMN_LABELS[size].index(col_letter)
            num = int(parts[1])

            if row not in range(size) or col not in range(size) or num not in range(1, size + 1):
                print("Invalid input. Check row, column, or number range.")
                continue

            if board_model.puzzle[row][col] != 0:
                print("You can't change original numbers.")
                continue

            if is_valid(board, row, col, num):
                board[row][col] = num
                print_board(board)
                if board == solution:
                    print(f"Well done {name}! Puzzle solved.")
                    return
            else:
                wrong_attempts += 1
                print("Incorrect. Lives left:", 3 - wrong_attempts)
                if wrong_attempts == 3:
                    print("Game over! You've used all attempts.")
                    return
        except (ValueError, IndexError):
            print("Invalid format. Please use e.g. A1 2")


#function to solve users sudoku
def solve_sudoku_input():
    try:
        choice = input("Please enter 'e' if you want to solve an easy 4x4 board or enter 'h' for a hard 9x9 board: ").lower()

        if choice == 'e':
            size = 4
        elif choice == 'h':
            size = 9
        else:
            print("Invalid input. Please enter 'e' for 4x4 or 'h' for 9x9.")
            return

        print("Perfect! Now enter your Sudoku row by row, and use 0 for the blanks (e.g 1001)")

        board = [] # creates an empty list
        for i in range(size):
            while True:
                row_input = input(f"Row {i + 1}: ") #ask the user row by row>
                if len(row_input) != size or not row_input.isdigit(): #ensure if number given is within limit
                    print(f"Sorry, ensure that it's exactly {size} digits.") #message to tell them to correct it
                
                # create list caled row>converts  string to interger then inputs it into the list row
                else:
                    row = [int(n) for n in row_input] 
                    board.append(row) #adds to the board list which builds the board 
                    break #break so move to next row

        print_board(board) 

        if solve_board(board):
            print("\nThis is the solved board:")
            print_board(board) #once complete print the solved board
        else:
            print("Sorry, can't solve. Please check your input and try again.") 
    except ValueError:
        print("Something went wrong. Please check and try again.") #incase if user enters letters...


# Main menu to control the game
def main():
    print("Welcome to Sudoku!")
    name = input("Please enter your name: ")
    print(f"Hello, {name}! Let the Sudoku games begin...\n")

    while True:
        print("~~~~~Main Menu~~~~~")
        print("'p' to play\n'i' for instructions\n's' to solve\n'q' to quit")
        choice = input("Enter your choice: ").lower()

        if choice == 'p':
            difficulty = input("Choose difficulty - 'e' for Easy (4x4), 'h' for Hard (9x9): ").lower()
            if difficulty in ['e', 'h']:
                size = 4 if difficulty == 'e' else 9
                play_sudoku(name, size)
            else:
                print("Invalid difficulty.")
        elif choice == 'i':
            print("\n---Instructions ---")
            print("- Fill all cells with correct numbers without repetition.")
            print("- Use format: 'A1 2' to place number 2 at A1.")
            print("- You have 3 attempts to fail before game over.")
            print("- Enter 's' to solve the puzzle instantly.\n")
        elif choice == 's':
            solve_sudoku_input()
        elif choice == 'q':
            print("Thanks for playing! Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
