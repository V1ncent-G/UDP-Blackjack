Please do not copy this code and pass it off as your own. 
Additionally please don't reuse this code for another project.
This project is intentionally shared as a demonstration.

Additional features I've considered are implementing a UI, expanding multiplayer to be compatible with more than two players, and using cards from a deck instead of using the random function.

A video demonstration of this project can be shared on YouTube if requested. 
Reach out to me via LinkedIn if you would like to see a video demonstration. 
https://www.linkedin.com/in/vincentguo3/

Breakdown of the code:
A card dealing function is created to deal the player with a random card.
The card randomly dealt is associated with a value and a suit.
The values of the cards in the player's hand are calculated with a value.
An ace has a value of 1 or 11. If a player has an ace and the value of the hand is less than 21 then the ace will have a value of 11, otherwise the ace will be 1 if the hand is 21 or greater.

UDP socket is created and the IP of the machine needs to be binded.
The main loop is initiated on the udpserver.py and waits for a response from the client player. 
When the server receives a response it initiates player 2's (server) turn and gives the option to hit or stand.
When the player stands the program will calculate the values of the cards in each player's hands and determine the winner. 
Both players will be prompted to continue playing if both players have matching responses to continue playing, or end the game if one player does not want to continue.
