# This is udpserver.py file
# Player 2

# Import socket and random modules
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

# create a UDP socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

# Get local machine address
ip = "10.228.227.90"                          

# Set port number for this server
port = 15000                                          

# Bind to the port
serversocket.bind((ip, port))                                  

while (True):  
    print("\nWaiting to receive message on port " + str(port) + '\n')

    # Receive player 1 hand value
    data, addr = serversocket.recvfrom(1024)
    player1_hand = int(data.decode())

    # Starting hand for player 2
    player2_hand = [deal_card(), deal_card()]

    # Print player 2 starting hand
    print("\nPlayer 2's Hand:", ', '.join(player2_hand))
    print("Player 2's Hand Value:", calculateValue(player2_hand))

    # Player 2's turn
    while True:
        # Player 2 chooses actions
        action = input("\nPlayer 2's turn. Hit or Stand? (h/s): ")
        if action.lower() == 'h':
            player2_hand.append(deal_card())
            print(f"Player 2's Hand:", ', '.join(player2_hand))
            print("Player 2's Hand Value:", calculateValue(player2_hand))
            if calculateValue(player2_hand) > 21:
                print("Player 2 busts!")
                break
        elif action.lower() == 's':
            break
        else:
            # Handle player inputs
            print("Invalid input. Please enter 'h' for Hit or 's' for Stand.")

    # Determine winner
    if (player1_hand) <= 21 and (calculateValue(player2_hand) > 21 or (player1_hand) > calculateValue(player2_hand)):
        print("\nPlayer 1 wins!")
        # Send win status 
        win = "\nPlayer 1 wins!"
        sent = serversocket.sendto(win.encode(), addr)

    elif calculateValue(player2_hand) <= 21 and ((player1_hand) > 21 or calculateValue(player2_hand) > (player1_hand)):
        print("\nPlayer 2 wins!")
        # Send win status 
        win = "\nPlayer 2 wins!"
        sent = serversocket.sendto(win.encode(), addr)

    else:
        print("\nIt's a tie!")
        # Send win status 
        win = "\nIt's a tie!"
        sent = serversocket.sendto(win.encode(), addr)

    # Receive player 1 vote 
    data, addr = serversocket.recvfrom(1024)
    player1_vote = str(data.decode())
    
    if player1_vote.lower() == 'n':
        break   

    # Check if players want to continue playing
    while(True):
        player2_vote = input("\nPlayer 2, do you want to continue playing? (y/n): ")
        if player2_vote != 'y' and player2_vote != 'n':
            # Handle player vote to continue
            print("\nInvalid input, please try again.")
        else:
            break

    sent = serversocket.sendto(player2_vote.encode(), addr)
   
    if player2_vote.lower() == 'n':
        break 

print("\nThanks for playing!")