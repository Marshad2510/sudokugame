# Import random module to generate random numbers for the Sudoku puzzle
from cProfile import label
import random

# Labels for columns
Column_lbl_9 = "A B C D E F G H I".split()  # Labels for hard 9x9 board
Column_lbl_4 = "A B C D".split()  # Labels for easier 4x4 board


# Main function to start the game
def main():
    print("Welcome to Sudoku!")


    # Ask for players name
    user_name = input("Please enter your name: ")
    print(f"Hello, {user_name}! let the Sudoku games begin...\n")


###

    # Main Menu loop
    while True:
        print("---Main Menu---")
        print("Press 'p' to play")
        print("Press 's' to solve")
        print("Press 'i' for instructions")
        print("Press 'q' to quit")

        # Get user choice
        choice = input("Enter your choice: ").lower()

        # If player wants to play
        if choice == 'p':
            difficulty = input("Choose difficulty - 'e' for Easy (4x4), 'h' for Hard (9x9): ").lower()
            
            if difficulty == 'e':
                play_sudoku(size=4, name=user_name)  # start an easy game
            
            elif difficulty == 'h':
                play_sudoku(size=9, name=user_name)  # start the hard game
            
            else:
                print("Sorry thats an invalid choice. Please enter either 'e' for an easy game or 'h' for harder game.")
        
        
        
        # If player wants to solve an puzzle
        elif choice == 's':
            solve_sudoku_input()




        # If player wants instructons
        elif choice == 'i':
            print("\n---Instructions ---")

            print("- Welcome to Sudoku.")
            print("- Sudoku is a number puzzle where you need to fill in empty cells of a grid so that")
            print(" each column, row and miniboxs contains all the numbers (either from 1-4 or 1-9 depending on dificulty level) without repetition.")
            print("- In Easy mode, a small grid which will use numbers 1 to 4. In Hard mode, it will use numbers 1 to 9.")
            print("- Also you cannot change the original numbers.")
            print("- Use format like 'A1 2'. This will place the number 2 in column A, row 1.")
            print("- Each game you'll only have 3 chances to make wrong moves then the game will end. Good luck!\n")

        # If user wants to quit the game
        elif choice == 'q':
            print("thanks for playing! Goodbye!")
            break
        else:
            print("Sorry thats an invalid choice. Please try again.")


# Functions to play Sudoku 
def play_sudoku(size, name):
    # Create an empty solution board
    solution = [[0] * size for _ in range(size)]  

    fill_board(solution)  # Use backtracking to fill the board with the correct solution

    # Number of blanks to remove for each difficulty
    #easy game 4x4 will have 8 blanks and hard game 9x9 will have 40
    blank = 8 if size == 4 else 40

    # create Sudoku puzzle by removing numbers from solution
    puzzle = create_puzzle(solution, blank)
    board = [row[:] for row in puzzle]  # Copy puzzle to create player's board

    print(f"\n{name}, here is your Sudoku puzzle!")
    print("Enter moves like 'A1 2'. Enter 'q' to quit.")

    # display the initial board
    print_board(board) 

    # track no of wrong attempts
    wrong_atmpts = 0  

    
    
    
    
    # Start playing the game
    while True:
        move = input("Enter your move: ").strip().upper()

        # have this at the top if user wants to quit
        if move.lower() == 'q': 
            print("You quit the game.")
            return

        try:
            parts = move.split()
            # Ensure the input has the correct format
            if len(parts) != 2:  
                raise ValueError

            column_letter = parts[0][0] #colum letter 
            row_number = int(parts[0][1]) # row number
            num = int(parts[1]) #number

            row = row_number - 1  # Convert row number to index as it starts at 0
            col = column_letter_to_index(column_letter, size)  # Convert column letter to index

            # Check if input is valid
            if row not in range(size) or col == -1 or num not in range(1, size + 1):
                print("Sorry thats an nvalid move. the format is 'A1 2'. This will place the number 2 in column A, row 1.")
                continue #skip to next 

            if puzzle[row][col] != 0:  # Can't change original numbers
                print("You can't change original numbers.")
                continue #skip to next

            # Vaalidate and update
            if is_valid(board, row, col, num):
                board[row][col] = num
                print_board(board)

                # Check if puzzle is solved
                if is_solved(board, solution):
                    print(f"\n Congratulations {name}! You have successfully solved the puzzle! Taking you back to the main menu now...")
                    return
            
            
            else:
                print("Sorry, that's incorrect. Please try again.")
                wrong_atmpts += 1 #add 1 to wrong attempts
                print(f"lives left: {wrong_atmpts}/3") #show the gamer how many attempts hes got left

                
                # end the game after 3 wrong attempts
                if wrong_atmpts == 3:  
                    print("Game over! You've reached the maximum number of mistakes.")
                    return
        except:
            print("Sorry thats a invalid input. Please try again.")


# Function to print the board
def print_board(board):
    size = len(board)
    lables = Column_lbl_4 if size == 4 else Column_lbl_9
    
############################################################################
    
    # Print column headers
    print("\n   " + "  ".join(label))

    # Print rows
    for i in range(size):
        if i % int(size ** 0.5) == 0 and i != 0:
            print("   " + "-" * (size * 2 + (size // int(size ** 0.5)) - 1))  # Box separation line

        row_str = f"{i + 1}  "
        for j in range(size):
            if j % int(size ** 0.5) == 0 and j != 0:
                row_str += "| "

            cell = board[i][j]
            row_str += str(cell) if cell != 0 else "."
            row_str += " "

        print(row_str)

# Function to create a Sudoku puzzle by removing numbers from a solved board
def create_puzzle(full_board, blank):
    puzzle = [row[:] for row in full_board]
    size = len(puzzle)
    count = 0

    while count < blank:
        row = random.randint(0, size - 1)
        col = random.randint(0, size - 1)
        if puzzle[row][col] != 0:
            puzzle[row][col] = 0
            count += 1
    return puzzle

# Backtracking function to solve the Sudoku board
def Solve_Brd(board):
    size = len(board)

    for row in range(size):
        for col in range(size):
            if board[row][col] == 0:
                for num in range(1, size + 1):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if Solve_Brd(board):
                            return True
                        board[row][col] = 0
                return False
    return True

# Function to fill the board with the correct numbers using backtracking
def fill_board(board):
    Solve_Brd(board)

# Function to check if a move is valid
def is_valid(board, row, col, num):
    size = len(board)
    box = int(size ** 0.5)

    for i in range(size):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row = (row // box) * box
    start_col = (col // box) * box
    for i in range(box):
        for j in range(box):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

# Function to convert column letter to index
def column_letter_to_index(letter, size):
    labels = Column_lbl_4 if size == 4 else Column_lbl_9
    letter = letter.upper()
    if letter in labels:
        return labels.index(letter)
    return -1

# Function to check if the player has solved the puzzle
def is_solved(player_brd, solution):
    for i in range(len(player_brd)):
        for j in range(len(player_brd)):
            if player_brd[i][j] != solution[i][j]:
                return False
    return True

# Function to solve the Sudoku from user input
def solve_sudoku_input():
    try:
        size = int(input("Enter the board size (4 for Easy, 9 for Hard): "))
        if size not in [4, 9]:
            print("Only 4 or 9 are allowed.")
            return
        print("Enter the board row by row with 0 for blanks (e.g., 1030).")
        board = []
        for i in range(size):
            while True:
                row_input = input(f"Row {i + 1}: ")
                if len(row_input) != size or not row_input.isdigit():
                    print(f"Enter exactly {size} digits.")
                else:
                    board.append([int(c) for c in row_input])
                    break
        print_board(board)
        if Solve_Brd(board):
            print("\nSolved Board:")
            print_board(board)
        else:
            print("This Sudoku puzzle cannot be solved.")
    except:
        print("Error occurred. Please make sure your input is correct.")

# Start the game
if __name__ == "__main__":
    main()
