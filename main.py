# Importing random module to generate random numbers for the puzzle
import random

# Define column labels for 9x9 and 4x4 boards
COL_LABELS_9 = "A B C D E F G H I".split()  # Labels for 9x9 board
COL_LABELS_4 = "A B C D".split()  # Labels for 4x4 board

# Main function to start the game
def main():
    # Welcome message
    print("===== Welcome to Sudoku Game =====")

    # Ask for username
    username = input("Enter your username: ")
    print(f"Hello, {username}! Let's begin.\n")

    # Loop for main menu
    while True:
        print("===== Main Menu =====")
        print("Press 'p' to play the game")
        print("Press 'i' for instructions")
        print("Press 'q' to quit")

        # Get user choice
        choice = input("Enter your choice: ").lower()

        if choice == 'p':  # If play selected
            # Ask for difficulty
            difficulty = input("Choose difficulty - 'e' for Easy (4x4), 'h' for Hard (9x9): ").lower()
            if difficulty == 'e':
                play_sudoku(size=4, name=username)  # Start easy game
            elif difficulty == 'h':
                play_sudoku(size=9, name=username)  # Start hard game
            else:
                print("Invalid choice. Choose 'e' or 'h'.")

        elif choice == 'i':  # If instructions selected
            # Print game instructions
            print("\n===== Instructions =====")
            print("- Choose Easy or Hard mode.")
            print("- Enter moves in format like 'A1 2' to place number.")
            print("- You can't change original puzzle numbers.")
            print("- You have 3 chances to make a wrong move.")
            print("- Solve the puzzle to win. Good luck!\n")

        elif choice == 'q':  # If quit selected
            print("Thank you for playing. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

# Function to print the current Sudoku board
def print_board(board):
    size = len(board)
    labels = COL_LABELS_4 if size == 4 else COL_LABELS_9  # Choose label based on board size
    print("\n   " + "  ".join(labels))  # Print column headers

    for i in range(size):
        if i % int(size ** 0.5) == 0 and i != 0:
            print("   " + "-" * (size * 2 + (size // int(size ** 0.5)) - 1))  # Box separation line
        row_str = f"{i+1}  "  # Row label
        for j in range(size):
            if j % int(size ** 0.5) == 0 and j != 0:
                row_str += "| "  # Vertical box separator
            cell = board[i][j]
            row_str += str(cell) if cell != 0 else "."  # Show number or dot for empty
            row_str += " "
        print(row_str)

# Function to convert column letter to index
def col_letter_to_index(letter, size):
    labels = COL_LABELS_4 if size == 4 else COL_LABELS_9
    letter = letter.upper()
    if letter in labels:
        return labels.index(letter)
    return -1

# Function to check if placing a number is valid
def is_valid(board, row, col, num):
    size = len(board)
    box = int(size ** 0.5)

    for i in range(size):
        if board[row][i] == num or board[i][col] == num:
            return False  # Number exists in row or column

    # Check the box
    start_row = (row // box) * box
    start_col = (col // box) * box
    for i in range(box):
        for j in range(box):
            if board[start_row + i][start_col + j] == num:
                return False  # Number exists in box

    return True  # Valid placement

# Backtracking function to solve the board
def solve_board(board):
    size = len(board)
    for row in range(size):
        for col in range(size):
            if board[row][col] == 0:
                for num in range(1, size + 1):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_board(board):
                            return True  # Continue solving
                        board[row][col] = 0  # Backtrack
                return False
    return True

# Fill board with valid solution
def fill_board(board):
    solve_board(board)  # Use backtracking to fill the board

# Create puzzle by removing numbers from a full board
def create_puzzle(full_board, blanks):
    puzzle = [row[:] for row in full_board]  # Make a copy of board
    size = len(puzzle)
    count = 0
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
                    print(f"\n\U0001F389 Congratulations {name}! You solved the puzzle!")
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
