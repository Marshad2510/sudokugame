print("Hello welcome to sudoku")

#ask for the users name
name = input("Enter your name: ")

#ask user to choose 'p' to play the game or 's' to solve the game
choice = input("Press 'p' to play or 's' to solve: ")

#IF statment 
if choice == 'p':
    print("You chose to play.")
elif choice == 's':
    print("You chose to solve.")
else:
    print("Please choose p to play or s to solved.")
