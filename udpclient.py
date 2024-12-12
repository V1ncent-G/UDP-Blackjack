# This is udpclient.py file
# Player 1

#Import socket programming module and random module
import socket
import random

# Function to deal a random card
def deal_card(): 
    suits = ['Hearts','Diamonds','Clubs','Spades'] # Available suits
    values = ['Ace','2','3','4','5','6','7','8','9','10','Jack','Queen','King'] # Values of cards
    return random.choice(values) + ' of ' + random.choice(suits) # Return random combination of value and suits

# Function to calculate player hand
def calculateValue(player_hand): 
    values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
        'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11} # Dictionary for values
    player_value = 0
    aces = 0
    
    # Check for aces in hand
    for card in player_hand:
        value = values[card.split()[0]]
        player_value += value
        if card.startswith('Ace'):
            aces += 1
   
    while player_value > 21 and aces > 0: 
        # Ace has value of 11. If there is an ace and value is bigger than 21, then ace has a value of 1
        player_value -= 10
        aces -= 1
    
    return player_value

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

# Set destination port
port = 21012

# Include the server Address 
serverAddr = ('10.230.221.6', port)

# Send message (input from the keyboard).
#The string needs to be converted to bytes (encode()).
# To send more than one message, please create a loop

while (True):
    # Starting hands for player 1
    player1_hand = [deal_card(), deal_card()]

    # Print starting hand for player 1
    print("\nPlayer 1's Hand:", ', '.join(player1_hand))
    print("Player 1's Hand Value:", calculateValue(player1_hand))
    
    # Player 1's turn
    while True:
        # Player 1 chooses action
        action = input("\nPlayer 1's turn. Hit or Stand? (h/s): ")
        if action.lower() == 'h':
            player1_hand.append(deal_card())
            print(f"\nPlayer 1's Hand:", ', '.join(player1_hand))
            print("Player 1's Hand Value:", calculateValue(player1_hand))
            if calculateValue(player1_hand) > 21:
                print("\nPlayer 1 busts!")
                break
        elif action.lower() == 's':
            break
        else:
            # Handle player inputs
            print("\nInvalid input. Please enter 'h' for Hit or 's' for Stand.")
    
    # Send client hand value to server
    msg = str(calculateValue(player1_hand))
    print("\nSending...")
    s.sendto(msg.encode(), serverAddr)

    # Receive win status from server
    msg, addr = s.recvfrom(1024)
    msg = msg.decode()
    print("\nReceived: " + msg)

    # Check if players want to continue playing
    while(True):
        player1_continue = input("\nPlayer 1, do you want to continue playing? (y/n): ")
        msg = player1_continue
        if player1_continue != 'y' and player1_continue != 'n':
            # Handle player vote to continue
            print("\nInvalid input, please try again.")
        else:
            break

    # Send server player 1's vote on continuing the game
    print("\nSending vote...")
    s.sendto(msg.encode(), serverAddr)

    # If player 1 wants to end the game, break the loop
    if msg == 'n':
        break

    # Receive vote from server to continue playing
    msg, addr = s.recvfrom(1024)
    msg = msg.decode()

    # If server chooses not to continue, end the game
    if msg == 'n':
        break

# Close connection
print("\nThanks for playing!")
s.close()