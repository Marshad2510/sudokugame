# Ask for the user's name
name = input("Enter your name: ")

# Ask user to press 'p' to play or 's' to solve
choice = input("Press 'p' to play or 's' to solve: ")

# Respond based on user input
if choice == 'p':
    print("You chose to play.")
elif choice == 's':
    print("You chose to solve.")
else:
    print("Invalid choice.")
