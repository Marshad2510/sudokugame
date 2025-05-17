import random #need a random module to allow random selection
from dataclasses import dataclass #define simple data containers???
from typing import List, Optional #this imports list for types.
 
 
 
#columnlabels for reference
COLUMN_LABELS = {
    4: ["A", "B", "C", "D"], #easy game = 4
    9: ["A", "B", "C", "D", "E", "F", "G", "H", "I"] #hard game = 9
}
 
#data modelling
#sudoku board
@dataclass(frozen=True) #can not change, this makes the dataclass imutable
class SudokuBoard:
    puzzle: List[List[int]] # The puzzle board with blanks
    solution: List[List[int]] # solved board
    size: int # size of the board which is either 4 or 9
    blanks: int # number of blanks filled in the grid
 
#this code generates a fully solved Sudoku board of the give size
def generate_solved_board(size: int) -> List[List[int]]:
    board = [[0] * size for _ in range(size)] # starts the board with 0s
    solve_board(board) #this helps solves the board using backtracking
    return board
 
 
# create the puzzle
# removes numbers creating blanks from the solvedboard
def create_puzzle(full_board: List[List[int]], blanks: int) -> List[List[int]]:
    puzzle = [row[:] for row in full_board]
    size = len(puzzle)
    count = 0
    while count < blanks:
        row, col = random.randint(0, size - 1), random.randint(0, size - 1)
        if puzzle[row][col] != 0: # check is not already blank
            puzzle[row][col] = 0 # set te cell to blank which should be 0 in this case
            count += 1
    return puzzle
 
 
# the full game board generator
def get_board_with_blanks(size: int) -> SudokuBoard:
    blanks = 8 if size == 4 else 40 #easy game has 8 blanks, hard game has 40 blanks
    solution = generate_solved_board(size) #generate the solution board
    puzzle = create_puzzle(solution, blanks)  # create the puzzle with blanks
    return SudokuBoard(puzzle=puzzle, solution=solution, size=size, blanks=blanks)
 
 
# print the the board
def print_board(board: List[List[int]]) -> None:
    size = len(board)
    labels = COLUMN_LABELS[size]
 
    print("\n   " + "  ".join(labels)) #print column lables
   
    #print board row by row
    for i in range(size):
        if i % int(size ** 0.5) == 0 and i != 0: #this is for the seperator between the boxes
            print("   " + "-" * (size * 2 + (size // int(size ** 0.5)) - 1))
        row_str = f"{i + 1}  "  #lables for rows
        for j in range(size):
            if j % int(size ** 0.5) == 0 and j != 0:  #print a vertival lines between boxes
                row_str += "| "
            cell = board[i][j] # get the value of cell
            row_str += str(cell) if cell != 0 else "." # used "." for the blan cell
            row_str += " "  #Adding spaces between numbers
        print(row_str)  # tis print the formtted row
 
 
#validation
#check if move is valid
def is_valid(board: List[List[int]], row: int, col: int, num: int) -> bool:
    size = len(board) #this helps get the size of the board when user enter their prefernce
    box = int(size ** 0.5) #calculate the boxe sizes if its 4x4 grid its 2, if 9x9 grid it should be 3
 
    #check if the number already exists in the cells particular row or column
    if num in board[row]: return False
 
    #check if the number already exists in the cells particular row or row
    if num in [board[i][col] for i in range(size)]: return False
   
    #this calculate the starting point of the sub-grid the cell is in
    start_row, start_col = (row // box) * box, (col // box) * box
   
    #this is the loop function throughnthe sub-gris check if the number already there.
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
    board_model = get_board_with_blanks(size)   #generate a puzzle with blanks and solution
    board = [row[:] for row in board_model.puzzle]  #create a copy of the puzzle
    solution = board_model.solution #store the answers
 
   
    #display the start of the sudoku borad
    print(f"\n{name}, here is your Sudoku puzzle!")
    print_board(board)
    print("Enter moves like 'A1 2'. Enter 'q' to quit.")
 
    wrong_attempts = 0  #count how many wrong attempts wre attempted
    while True:  #main game loop
        move = input("Move (e.g A1 2): ").strip().upper() #Ask the player for their move
 
        if move.lower() == 'q': # to quit the game if the player press q to quit the game
            print("You have quit the game.")
            return
        try:
            #ths splits the input into pares such as A1, and then the number users want to input
            parts = move.split()
 
            #Validate input length
            if len(parts) != 2: raise ValueError
 
            # extract column letter and row number from input
            col_letter, row_char = parts[0][0], parts[0][1]
            row = int(row_char) - 1 # convert to 0 based index
            col = COLUMN_LABELS[size].index(col_letter) #find the column index
            num = int(parts[1])  #extract ythe number to place
 
 
            # check if the inputs are within the range
            if row not in range(size) or col not in range(size) or num not in range(1, size + 1):
                print("Invalid input. Check row, column, or number range.")
                continue
 
            # check if the user iinput any value on the pre-filled cell
            if board_model.puzzle[row][col] != 0:
                print("You can't change original numbers.")
                continue
           
            #validate and place the number if its valid
            if is_valid(board, row, col, num):
                board[row][col] = num
                print_board(board)
 
                #if the board matches the solution, the game is complete
                if board == solution:
                    print(f"Well done {name}! Puzzle solved.")
                    return
            else:
                #tracks the incorrct attempts and count how many lives left
                wrong_attempts += 1
                print("Incorrect. Lives left:", 3 - wrong_attempts)
 
                #if three wrong attempts are made, end the game
                if wrong_attempts == 3:
                    print("Game over! You've used all attempts.")
                    return
        except (ValueError, IndexError):
            print("Invalid format. Please use e.g. A1 2")
 
 
#function to solve users sudoku
def solve_sudoku_input():
    try:
 
        #User inputs the choice of difficulty level
        choice = input("Please enter 'e' if you want to solve an easy 4x4 board or enter 'h' for a hard 9x9 board: ").lower()
 
        #set the size of the grid depending on their choice
        if choice == 'e':
            size = 4
        elif choice == 'h':
            size = 9
        else:
            print("Invalid input. Please enter 'e' for 4x4 or 'h' for 9x9.")
            return
       
 
        #this gives the information on how to fill the grid in  the correct format
        print("Perfect! Now enter your Sudoku row by row, and use 0 for the blanks (e.g 1001)")
 
        board = [] # creates an empty list
        for i in range(size): # loop to accept each row of inpus
            while True:
                row_input = input(f"Row {i + 1}: ") #ask the user row by row>
                if len(row_input) != size or not row_input.isdigit(): #ensure if number given is within limit
                    print(f"Sorry, ensure that it's exactly {size} digits.") #message to tell them to correct it
               
                # create list caled row>converts  string to interger then inputs it into the list row
                else:
                    row = [int(n) for n in row_input]
                    board.append(row) #adds to the board list which builds the board
                    break #break so move to next row
 
        print_board(board) #print the board and solve it
 
        if solve_board(board):
            print("\nThis is the solved board:")
            print_board(board) #once complete print the solved board
        else:
            print("Sorry, can't solve. Please check your input and try again.")
    except ValueError:
        print("Something went wrong. Please check and try again.") #incase if user enters letters...
 
 
# Main menu to control the game
def main():
    print("Welcome to Sudoku!") # print welcome message as the user enter
    name = input("Please enter your name: ") #ask user to input their name
    print(f"Hello, {name}! Let the Sudoku games begin...\n") # this display welcome message
 
 
    #main menu loop
    while True:
 
        #print the main menu option
        print("~~~~~Main Menu~~~~~")
        print("'p' to play\n'i' for instructions\n's' to solve\n'q' to quit")
 
        #this ask the user to choose an option
        choice = input("Enter your choice: ").lower()
 
        #if the user choose play sudoku
        if choice == 'p':
 
            #Ask the user to seect the difficulty level
            difficulty = input("Choose difficulty - 'e' for Easy (4x4), 'h' for Hard (9x9): ").lower()
 
            #if the choice is valid, set the board size and the start game
            if difficulty in ['e', 'h']:
                size = 4 if difficulty == 'e' else 9
                play_sudoku(name, size) #call the play_sudoku function with chpsen size
            else:
 
                #if the user enters an invalid option, display an error message
                print("Invalid difficulty.")
 
                #if the user chooses to view the instructions
        elif choice == 'i':
 
            #Shows the game instructions to the users
            print("\n---Instructions ---")
            print("- Fill all cells with correct numbers without repetition.")
            print("- Use format: 'A1 2' to place number 2 at A1.")
            print("- You have 3 attempts to fail before game over.")
            print("- Enter 's' to solve the puzzle instantly.\n")
       
        #if the user chooses to solve a custom puzzle
        elif choice == 's':
            solve_sudoku_input()  # call the solve_sudoku_input function
 
            #if the user chooses to quit the game
        elif choice == 'q':
            print("Thanks for playing! Goodbye!") #print a goodbye message
            break
 
        #this shows if the user enters an invalid option, display an erro message
        else:
            print("Invalid choice. Try again.")
 
    #ensures the main() function runs only if this cript is executes directly
 
if __name__ == "__main__":
    main()