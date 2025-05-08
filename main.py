# Import random module = generate random numbers for the sudoku puzzle
import random

# Labels for columns
column_lable_h = ["A", "B", "C", "D", "E", "F", "G", "H", "I"] # colomn for the hard 9x9 board
column_lable_e = ["A", "B", "C", "D"] # colomn label for easier 4x4 board



# main function to start the game
def main():
    print("Welcome to Sudoku!")


    # Ask for players name
    user_name = input("Please enter your name: ")
    print(f"Hello, {user_name}! let the Sudoku games begin...\n")


###

    
    # Main Menu
    while True:
        print("~~~~~Main Menu~~~~~")
        
        print("please choose from the following options:")
        print("Press 'p' to play sudoku ")
        print("Press 's' to solve your own sudoku puzzle")
        print("Press 'i' for instructions and how to play sudoku")
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

    # Number of blanks/remove depends on each difficulty
    #an easy game 4x4 will have 8 blanks and  a hard game 9x9 will have 40
    
    if size == 4: #easy game 
        blank = 8 # 8 blanks
    
    else: 
        blank = 40 #hard game = 40 blanks

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
        move = input("Please enter your move (e.g A1 2, where A is the colomn, 1 is the row and 2 is the value): ").strip().upper()

        
        # have this at the top if user wants to quit
        if move.lower() == 'q': 
            print("You have quit the game.")
            return

        try:
            parts = move.split()
            # Ensure the input has the correct format
            if len(parts) != 2:  
                raise ValueError ("enter your move (e.g A1 2, where A is the colomn, 1 is the row and 2 is the value")

            column_letter = parts[0][0] #colum letter 
            row_number = int(parts[0][1]) # row number
            num = int(parts[1]) #number/value to be in sudoku

            row = row_number - 1  # Convert row number to index as it starts at 0
            col = column_letter_to_index(column_letter, size)  # Convert column letter to index

            # Check if input is valid
                
            #check if row is within the range
            if row not in range(size):
                print("please double check your row number. It should be between 1 and", size)
                continue
            
            #check if that the colomn is within the range 
            if col == -1:
                print("Please check your column letter. It should be one of the valid labels at the top.")
                continue
            
            #Check if number is valid 
            if num not in range(1, size + 1):
                print("sorry thats a incorrect number, try again.")
                continue 

            if puzzle[row][col] != 0:  # Can't change original numbers
                print("You can't change original numbers.")
                continue #skip to next

            # Vaalidate and update
            if is_valid(board, row, col, num):
                board[row][col] = num
                print_board(board)

                # Check if puzzle is solved
                if is_solved(board, solution):
                    print(f"Well done {name}! You have successfully solved the puzzle.Taking you back to the main menu...")
                    return
            
            
            else:
                print("Sorry, that's incorrect. Please try again.")
                wrong_atmpts += 1 #add 1 to wrong attempts
                print(f"lives left: {wrong_atmpts}/3") #show the gamer how many attempts hes got left

                
                # end the game after 3 wrong attempts
                if wrong_atmpts == 3:  
                    print("game over! You've have lost all your lives. Rome wasnt built in a day, keep trying ...")
                    return
        except ValueError:
            print("Sorry thats a invalid input. Please try again.")


# function = prints the sudoku board
def print_board(board):
    size = len(board)
    lables = column_lable_e if size == 4 else column_lable_h

############################################################################
    
    # Print column headers
    print("\n   " + "  ".join(lables))

    # print rows
    for i in range(size):
        if i % int(size ** 0.5) == 0 and i != 0:
            print("   " + "-" * (size * 2 + (size // int(size ** 0.5)) - 1))  # box separation line

        #row number
        row_str = f"{i + 1}  "
        for j in range(size):
            if j % int(size ** 0.5) == 0 and j != 0:
                
                
                #make miniboxes within bigger box
                row_str += "| "

            cell = board[i][j]
            row_str += str(cell) if cell != 0 else "."
            row_str += " "

        print(row_str)

# function = to create a sudoku puzzle - randomly remove numbers from a solved board
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

# backtracking function = solves the board
def solve_board(board):
    size = len(board)

    for row in range(size):
        for col in range(size):
            if board[row][col] == 0: #if that cell is blank
                for num in range(1, size + 1):# try the numbers in range
                    if is_valid(board, row, col, num): #double check by validating if its the right number
                        board[row][col] = num #then place the number in board
                        if solve_board(board): #repeat to solve the full sudkou board  
                            return True
                        board[row][col] = 0 #if it doesn't work, then go back and remove that number
                #if no valid numbers found then return false
                return False
    #puzzle is successfullt solved when all the blanks are filled
    return True

# function = fills  board with  correct numbers via backtracking
def fill_board(board):
    #use backtracking to solve
    solve_board(board)

# function = checks if move is valid
def is_valid(board, row, col, num):
    size = len(board)
    box = int(size ** 0.5)

    #check if the number is already in the roe or the colomun
    for i in range(size):
        if board[row][i] == num or board[i][col] == num:
            return False

    
    #check if that number is already within the minibox
    start_row = (row // box) * box
    start_col = (col // box) * box
    for i in range(box):
        for j in range(box):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

# function = converts column letter to index
def column_letter_to_index(letter, size):
    labels = column_lable_e if size == 4 else column_lable_h
    letter = letter.upper()
    if letter in labels:
        return labels.index(letter)
    return -1

# ffunction = checks if player has successfully solved their puzzle
def is_solved(player_brd, solution):
    for i in range(len(player_brd)):
        for j in range(len(player_brd)):
            if player_brd[i][j] != solution[i][j]:
                return False
    return True





#Solve
# function = solves a sudoku from a users input

def solve_sudoku_input():
    #ask user if they want so solve a 4x4 board or a 9x9 board
    try:
        choice = input("Please enter 'e' if u want to solve a easy board 4x4 or enter 'h' to solve a hard 9x9 board: ").lower()

        #if statmnt for e or h board
        if choice == 'e':
            size = 4 
        
        elif choice == 'h':
            size = 9
        
        else:
            print("Sorry that isn't right please either enter e for a 4x4 board or h for a 9x9 board.")
            return
        print("Perfecr now enter your sudoky row by row, and use 0 for the blanks (e.g 1001)")

        board = []
        for i in range(size):
            while True:
                row_input = input(f"row {i+1}: ")
                if len(row_input) != size or not row_input.isdigit():
                    print(f"sorry ensure that its exactly {size} digits.")
                else:
                    row = [int(n) for n in row_input]
                    board.append(row)
                    break

        print_board(board)

        if solve_board(board):
            print("\n this is the solved board:")
            print_board(board)
        else:
            print("sorry, can't solve. Please check your input and try again")
    except ValueError:
        print("sorry somethings not right, please double check and try again.")



# main to start the game 
if __name__ == "__main__":
    main()
