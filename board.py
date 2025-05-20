import random

# Define column labels for 9x9 and 4x4 boards
COL_LABELS_9 = "A B C D E F G H I".split()
COL_LABELS_4 = "A B C D".split()

# Main function of the game
def main():
    print("===== Welcome to Sudoku Game =====")
    username = input("Enter your username: ")  # Ask for username once
    print(f"Hello, {username}! Let's begin.\n")

    while True:
        # Show the main menu
        print("===== Main Menu =====")
        print("Press 'p' to play the game")
        print("Press 'i' for instructions")
        print("Press 'q' to quit")
        
        choice = input("Enter your choice: ").lower()  # Get menu choice

        if choice == 'p':
            # Ask difficulty
            difficulty = input("Choose difficulty - 'e' for Easy (4x4), 'h' for Hard (9x9): ").lower()
            if difficulty == 'e':
                play_sudoku(size=4, name=username)
            elif difficulty == 'h':
                play_sudoku(size=9, name=username)
            else:
                print("Invalid choice. Choose 'e' or 'h'.")

        elif choice == 'i':
            # Show instructions
            print("\n===== Instructions =====")
            print("- Choose Easy or Hard mode.")
            print("- Enter moves in format like 'A1 2' to place number.")
            print("- You can't change original puzzle numbers.")
            print("- You have 3 chances to make a wrong move.")
            print("- Solve the puzzle to win. Good luck!\n")

        elif choice == 'q':
            print("Thank you for playing. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

# Function to print the current board
def print_board(board):
    size = len(board)
    labels = COL_LABELS_4 if size == 4 else COL_LABELS_9
    print("\n   " + "  ".join(labels))  # Column headers

    for i in range(size):
        # Add a line to separate boxes
        if i % int(size ** 0.5) == 0 and i != 0:
            print("   " + "-" * (size * 2 + (size // int(size ** 0.5)) - 1))
        row_str = f"{i+1}  "
        for j in range(size):
            if j % int(size ** 0.5) == 0 and j != 0:
                row_str += "| "
            cell = board[i][j]
            row_str += str(cell) if cell != 0 else "."
            row_str += " "
        print(row_str)

# Convert column letter to column index
def col_letter_to_index(letter, size):
    labels = COL_LABELS_4 if size == 4 else COL_LABELS_9
    letter = letter.upper()
    if letter in labels:
        return labels.index(letter)
    return -1

# Check if placing a number is valid
def is_valid(board, row, col, num):
    size = len(board)
    box = int(size ** 0.5)

    # Check row and column
    for i in range(size):
        if board[row][i] == num or board[i][col] == num:
            return False

    # Check square box
    start_row = (row // box) * box
    start_col = (col // box) * box
    for i in range(box):
        for j in range(box):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

# Solve board using backtracking
def solve_board(board):
    size = len(board)
    for row in range(size):
        for col in range(size):
            if board[row][col] == 0:
                for num in range(1, size + 1):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_board(board):
                            return True
                        board[row][col] = 0
                return False
    return True

# Fill a board with a valid Sudoku solution
def fill_board(board):
    solve_board(board)

# Create a puzzle by removing numbers from a full board
def create_puzzle(full_board, blanks):
    puzzle = [row[:] for row in full_board]  # Make a copy
    size = len(puzzle)
    count = 0
    while count < blanks:
        row = random.randint(0, size - 1)
        col = random.randint(0, size - 1)
        if puzzle[row][col] != 0:
            puzzle[row][col] = 0
            count += 1
    return puzzle

# Check if player solved the board correctly
def is_solved(player_board, solution):
    for i in range(len(player_board)):
        for j in range(len(player_board)):
            if player_board[i][j] != solution[i][j]:
                return False
    return True

# Function to play the game
def play_sudoku(size, name):
    # Generate solution board
    solution = [[0]*size for _ in range(size)]
    fill_board(solution)

    # Decide blanks: 8 for 4x4, 40 for 9x9
    blanks = 8 if size == 4 else 40

    # Create puzzle
    puzzle = create_puzzle(solution, blanks)
    board = [row[:] for row in puzzle]  # Player board

    print(f"\n{name}, here is your Sudoku puzzle!")
    print("Enter moves like 'A1 2'. Enter 'q' to quit.")
    print_board(board)

    wrong_attempts = 0  # Track wrong moves

    while True:
        move = input("Enter your move: ").strip().upper()

        if move.lower() == 'q':
            print("You quit the game.")
            return  # Go back to main menu

        try:
            parts = move.split()
            if len(parts) != 2:
                raise ValueError

            col_letter = parts[0][0]
            row_num = int(parts[0][1])
            num = int(parts[1])

            row = row_num - 1
            col = col_letter_to_index(col_letter, size)

            if row not in range(size) or col == -1 or num not in range(1, size + 1):
                print("Invalid move. Use format like A1 3.")
                continue

            if puzzle[row][col] != 0:
                print("You can't change original numbers.")
                continue

            if is_valid(board, row, col, num):
                board[row][col] = num
                print_board(board)

                if is_solved(board, solution):
                    print(f"\n🎉 Congratulations {name}! You solved the puzzle!")
                    return  # Return to menu
            else:
                print("❌ Wrong move!")
                wrong_attempts += 1
                print(f"Wrong attempts: {wrong_attempts}/3")
                if wrong_attempts == 3:
                    print("Game over! Too many mistakes.")
                    return
        except:
            print("Invalid input. Try again.")

# Start the program
if __name__ == "__main__":
    main()
