import random

# User selects if they want to play or solve the game
def main():
    print("Welcome to Sudoku!")

    # get user name
    name = input("Enter your name: ")
    print(f"Hello, {name}!\n")

    #if player = p then play game, if player = s then solve game 
    choice = input("Press 'p' to play or 's' to solve: ").lower()
    if choice == 'p':
        print("Alright get ready to play.")
        play_sudoku()
    elif choice == 's':
        print("You chose to solve")
        solve_sudoku()
    else:
        print("Invalid choice! Please either choose 'p' to play or 's' to solve.")

# Code for the board

COL_LABELS = "A B C D E F G H I".split()

def print_board(board):
    print("\n   " + "  ".join(COL_LABELS))
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("   " + "-" * 21)
        row_str = f"{i+1}  "
        for j in range(9):
            if j % 3 == 0 and j != 0:
                row_str += "| "
            row_str += str(board[i][j]) if board[i][j] != 0 else "."
            row_str += " "
        print(row_str)

def col_letter_to_index(letter):
    letter = letter.upper()
    if letter in COL_LABELS:
        return COL_LABELS.index(letter)
    return -1

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def is_solved(player_board, solution):
    for i in range(9):
        for j in range(9):
            if player_board[i][j] != solution[i][j]:
                return False
    return True

def fill_board(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if fill_board(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def create_puzzle(full_board, blanks=40):
    puzzle = [row[:] for row in full_board]
    count = 0
    while count < blanks:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if puzzle[row][col] != 0:
            puzzle[row][col] = 0
            count += 1
    return puzzle


# cdoe to play sudoku

def play_sudoku():
    while True:
        solution = [[0] * 9 for _ in range(9)]
        fill_board(solution)
        puzzle = create_puzzle(solution, blanks=40)
        board = [row[:] for row in puzzle]

        print("\n New Sudoku Puzzle!")
        print("Input moves in the format 'A1 5' to place 5 at Row 1, Column A.")
        print_board(board)

        while True:
            move = input("Enter move (e.g., A1 5) or 'q' to quit: ").strip()
            if move.lower() == 'q':
                print("Thanks for playing!")
                return

            try:
                parts = move.upper().split()
                if len(parts) != 2 or len(parts[0]) < 2:
                    raise ValueError
                col_letter = parts[0][0]
                row_num = int(parts[0][1])
                num = int(parts[1])
                row = row_num - 1
                col = col_letter_to_index(col_letter)

                if row not in range(9) or col == -1 or not (1 <= num <= 9):
                    print("Invalid input format. Use format like 'B3 9'")
                    continue

                if puzzle[row][col] != 0:
                    print("You can't change the original puzzle values.")
                    continue

                if is_valid(board, row, col, num):
                    board[row][col] = num
                    print_board(board)
                    if is_solved(board, solution):
                        print("\n Congratulations! You solved the puzzle! 🎉")
                        break
                else:
                    print(" Invalid move! That number conflicts with Sudoku rules.")
            except:
                print("Invalid format. Example: 'C4 7' means put 7 at Column C, Row 4.")

        again = input("Do you want to play again? (y/n): ").lower()
        if again != 'y':
            print("Goodbye!")
            break


# code to solve a sudoku 

def solve_sudoku():
    print("\nYou chose to solve a Sudoku puzzle!")
    board = [[0 for _ in range(9)] for _ in range(9)]
    print("\nEmpty Sudoku Board:")
    print_board(board)

    print("\nNow enter your puzzle row by row. Use 9 digits per row (use 0 for blanks).")
    for i in range(9):
        while True:
            row_input = input(f"Row {i+1}: ").strip()
            if len(row_input) == 9 and row_input.isdigit():
                board[i] = [int(d) for d in row_input]
                break
            else:
                print("Invalid input. Please enter exactly 9 digits (use 0 for blanks).")
    print("\nYour puzzle:")
    print_board(board)

    print("\nSolving the puzzle...\n")
    if solve_board(board):
        print("Solved Sudoku:")
        print_board(board)
    else:
        print("This puzzle cannot be solved. Please check your input.")


# Solving function (backtracking) 
def solve_board(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_board(board):
                            return True
                        board[row][col] = 0
                return False
    return True


# Run program
if __name__ == "__main__":
    main()
