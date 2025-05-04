# import module random = generate random numbers for sudoku
import random

# column labels for 9x9 and 4x4 boards
COL_LABELS_9 = "A B C D E F G H I".split()  # Labels for 9x9 board
COL_LABELS_4 = "A B C D".split()  # Labels for 4x4 board

# Main function start the game
def main():
    

    print("Welcome to Sudoku")

    # ask for users name
    username = input("Please enter your name: ")
    print(f"Hello, {username}! Let the Sudoku games begin...\n")




    # main menu loop
    while True:
        print("---Main Menu---")
        print("Press 'p' to play")
        print("Press 'i' for instructions")
        print("Press 'q' to quit")




        # Get user choice
        choice = input("Enter your choice: ").lower()

    #TO PLAY
        if choice == 'p':

            # Ask for difficulty
            difficulty = input("Choose difficulty - 'e' for Easy (4x4), 'h' for Hard (9x9): ").lower()

            if difficulty == 'e':
                play_sudoku(size=4, name=username)  # Start easy game

            elif difficulty == 'h':
                play_sudoku(size=9, name=username)  # Start hard game

            else:
                print("Invalid choice. Please either choose 'e' for easy game or 'h'for a harder game.") 





    #INSTRUCTIONS 
        elif choice == 'i':  # If instructions selected

            
            print("\n---Instructions ---")
            print("- Enter (e) for Easy or (h) for Hard diffuclty level.")
            print("-  fill in the empty cells so that each row, column, and box contains all the numbers from 1 to 9 ")
            print("- (or 1 to 4 in Easy mode) without repeating any.")
            print("- A bigger box will either have 4(easy level) or 9(hard level) miniboxes, in these miniboxes numbers cant be repeated ")
            print("- Enter moves in format like e.g 'A1 2'. Therefore this will place the number 2 in the column A row 1 box .")
            print("- You can't change original puzzle numbers.")
            print("- You have 3 chances to make a wrong move.")           
            print("- Solve the puzzle to win. Good luck!\n")



    #QUIT GAME
        elif choice == 'q':
            print("Thank you for playing. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")





# Function to print the board
def print_board(board):
    size = len(board)

#if easy game is chosen then label will be COL_LABELS_4, orelse its hard game therefore itll be 
    labels = COL_LABELS_4 if size == 4 else COL_LABELS_9 
    
    #column header
    print("\n   " + "  ".join(labels)) 


    #loop thru each row to print
    for i in range(size):
        if i % int(size ** 0.5) == 0 and i != 0:
            # box seperation line (2x2 in easy and 3x3 in hard)
            print("   " + "-" * (size * 2 + (size // int(size ** 0.5)) - 1))  # Box separation line

        #Print row numbers
        row_str = f"{i+1}  "  #index

        #loop thru each colum of row
        for j in range(size):

        #vertical seperator to make the box divised 
            if j % int(size ** 0.5) == 0 and j != 0:

                row_str += "| "  
            
            #get the cell value then show . for blank
            cell = board[i][j]
            row_str += str(cell) if cell != 0 else "."  #
            row_str += " " #SPACE BETWEEN NUMBERS

        #print the row
        print(row_str)

# function - convert column letter to index
def col_letter_to_index(letter, size):
    #first find the column depends on size
    labels = COL_LABELS_4 if size == 4 else COL_LABELS_9

    letter = letter.upper()#convert lowercase to uppercase

    #makes sure letter is in the column and then return the index
    if letter in labels:
        return labels.index(letter)
    #if incorrect returns -1
    return -1 

#SUDOKU GAME FACTORS

# function - check if the number is valid
def is_valid(board, row, col, num):
    size = len(board)
    #size of the minibox within bigger box
    box = int(size ** 0.5)

    #check if entered number is in that row and column
    for i in range(size):
        if board[row][i] == num or board[i][col] == num:
            
            #if its present then return false. CANNOT HAVE SAME NUMBER IN ROW+COLUMN
            return False 

    # Check if entered number exists in the minibox
    #find the start of row and column
    start_row = (row // box) * box
    start_col = (col // box) * box
    for i in range(box):
        for j in range(box):
            if board[start_row + i][start_col + j] == num:

                #if its present then return false. CANNOT HAVE SAME NUMBER IN THE MINIBOX
                return False  
            
    #ONLY IF ITS RIGHT THEN RETURN TRUE
    return True  # Valid placement

#BACKTRACKING - solve board
def solve_board(board):
    #get size of board
    size = len(board)

    #go thru board to find empty cell =0
    for row in range(size):
        for col in range(size):
            if board[row][col] == 0:
                #place every number from 1 in empty cell
                for num in range(1, size + 1):
                    if is_valid(board, row, col, num): #check if that numbers valid
                        board[row][col] = num #PLACE THAT CORRECT NUMBER
                        if solve_board(board): 
                        #if it is solveable = true
                            return True  
                        
                        board[row][col] = 0  # go back if not working
                        #return false = no valid numbers cant be placed
                return False
#if board is solved successfully return = true
    return True

# fill out the board with correct numbers using backtracking
def fill_board(board):
    solve_board(board) 


# CREATE SUDOKU by removing numbers from a full working board
def create_puzzle(full_board, blanks):
    
    # Make a copy of board
    puzzle = [row[:] for row in full_board]  
    size = len(puzzle) #size of board
    count = 0 #for removed numbers
    while count < blanks:
        row = random.randint(0, size - 1)
        col = random.randint(0, size - 1)
        if puzzle[row][col] != 0:
            puzzle[row][col] = 0  # Remove number
            count += 1
    return puzzle

# Check if player's board matches the solution
def is_solved(player_board, solution):
    for i in range(len(player_board)):
        for j in range(len(player_board)):
            if player_board[i][j] != solution[i][j]:
                return False  # Mismatch found
    return True

# Function to handle the full game flow
def play_sudoku(size, name):
    solution = [[0]*size for _ in range(size)]  # Create empty solution board
    fill_board(solution)  # Fill it with valid solution

    blanks = 8 if size == 4 else 40  # Number of blanks based on difficulty
    puzzle = create_puzzle(solution, blanks)  # Generate puzzle
    board = [row[:] for row in puzzle]  # Create player board

    print(f"\n{name}, here is your Sudoku puzzle!")
    print("Enter moves like 'A1 2'. Enter 'q' to quit.")
    print_board(board)  # Show initial board

    wrong_attempts = 0  # Track mistakes

    while True:
        move = input("Enter your move: ").strip().upper()  # Get player move

        if move.lower() == 'q':
            print("You quit the game.")
            return

        try:
            parts = move.split()
            if len(parts) != 2:
                raise ValueError  # Invalid input format

            col_letter = parts[0][0]  # Extract column letter
            row_num = int(parts[0][1])  # Extract row number
            num = int(parts[1])  # Extract number to place

            row = row_num - 1
            col = col_letter_to_index(col_letter, size)  # Get column index

            if row not in range(size) or col == -1 or num not in range(1, size + 1):
                print("Invalid move. Use format like A1 3.")
                continue

            if puzzle[row][col] != 0:
                print("You can't change original numbers.")
                continue

            if is_valid(board, row, col, num):
                board[row][col] = num  # Place the number
                print_board(board)  # Show updated board

                if is_solved(board, solution):
                    print(f"\n Congratulations {name}! You solved the puzzle!")
                    return
            else:
                print("\u274C Wrong move!")
                wrong_attempts += 1
                print(f"Wrong attempts: {wrong_attempts}/3")
                if wrong_attempts == 3:
                    print("Game over! Too many mistakes.")
                    return
        except:
            print("Invalid input. Try again.")

# Run the main function to start the game
if __name__ == "__main__":
    main()
