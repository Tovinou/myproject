import random

# Options for the game
choices = ['rock', 'paper', 'scissors']

# Function to determine the winner
def determine_winner(player, computer):
    if player == computer:
        return "It's a tie!"
    elif (player == 'rock' and computer == 'scissors') or \
         (player == 'scissors' and computer == 'paper') or \
         (player == 'paper' and computer == 'rock'):
        return "player wins!"
    else:
        return "computer wins!"

# Main game loop
def play_game():
    # Ask for player's input
    player = input("rock, paper or scissors? ").lower()
    
    # Validate player input
    if player not in choices:
        print("Invalid input, game over!")
        return
    
    # Computer randomly chooses
    computer = random.choice(choices)

    # Display choices
    print(f"player: {player}")
    print(f"computer: {computer}")

    # Determine the winner
    result = determine_winner(player, computer)
    print(result)
    print("game over!")

# Run the game
if __name__ == "__main__":
    play_game()
