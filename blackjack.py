import random

# Set Up Cards
suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

# Global Playing Variable
playing = True

# CLASSES

class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
    
    def __str__(self):
        deck_str = ''
        for card in self.deck:
            deck_str += '\n' + card.__str__()
        return deck_str

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        card = self.deck.pop()
        return card

class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        
        if(card.rank == "Ace"):
            self.aces += 1
    
    def adjust_for_ace(self):
        if(self.value > 21 and self.aces > 0):
            self.value -= 10
            self.aces -= 1

class Chips:
    
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
        self.bet = 0
    
    def lose_bet(self):
        self.total -= self.bet
        self.bet = 0



# FUNCTIONS
def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("\nEnter number of chips you would like to bet: "))
        except:
            print("Bet must be a valid integer")
        else:
            if (chips.bet > chips.total):
                print("You only have ", chips.total, " chips available" )
            else:
                break
 

def hit(deck,hand):
    new_card = deck.deal()
    hand.add_card(new_card)
    hand.adjust_for_ace()
 

def hit_or_stand(deck,hand):
    global playing

    while True:
        try:
            # Player input for hit or stand
            player_move = input("\nHit or Stand: ").lower()
        except:
            # If input was not hit or stand
            print("\nPlease enter 'Hit' or 'Stand'")
        else:
            # Hit
            if (player_move == "hit"):
                hit(deck,hand)

            # Stand
            if (player_move == 'stand'):
                print("\nPlayer stands. Dealer's turn")
                playing = False
        break


def show_some(player,dealer):
    print("\nPlayer Hand:")
    print(*player.cards, sep = "\n")
    print("\nDealer Hand:\nHidden Card")
    print(*dealer.cards[1:], sep = "\n")
    
def show_all(player,dealer):
    
    print("\nPlayer Hand:")
    print(*player.cards, sep = "\n")
    print("\nDealer Hand:")
    print(*dealer.cards, sep = "\n")

def player_busts(player, dealer, chips):
    print("\nPlayer Busts!")
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print("\nPlayer Wins!")
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print("\nDealer Busts!")
    chips.win_bet()
    
def dealer_wins(player, dealer, chips):
    print("\nDealer Wins!")
    chips.lose_bet()
    
def push(player, dealer):
    print("\nIt's a push (tie)!")

def play_game():
    global playing

    while True:
        # Print an opening statement
        print("\nHello and welcome to the Python Casino Black Jack table")
        
        # Create & shuffle the deck, deal two cards to each player
        game_deck = Deck()
        game_deck.shuffle()
        
        player = Hand()
        dealer = Hand()
        
        player.add_card(game_deck.deal())
        player.add_card(game_deck.deal())
        dealer.add_card(game_deck.deal())
        dealer.add_card(game_deck.deal())
            
        # Set up the Player's chips
        chips = Chips()
        
        # Prompt the Player for their bet
        take_bet(chips)
        
        # Show cards (but keep one dealer card hidden)
        show_some(player, dealer)
        
        while playing:  # recall this variable from our hit_or_stand function
            
            # Prompt for Player to Hit or Stand
            hit_or_stand(game_deck, player)
            
            # Show cards (but keep one dealer card hidden)
            show_some(player, dealer)
            
            # If player's hand exceeds 21, run player_busts() and break out of loop
            if(player.value > 21):
                player_busts(player, dealer, chips)
                break

        # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
        if(player.value <= 21):
            while(dealer.value < 17):
                hit(game_deck, dealer)
        
            # Show all cards
            show_all(player, dealer)
            
            # Run different winning scenarios
            
            # Dealer Bust
            if (dealer.value > 21):
                dealer_busts(player, dealer, chips)
            # Player Win
            elif(player.value > dealer.value):
                player_wins(player, dealer, chips)
            # Dealer Win
            elif(player.value < dealer.value):
                dealer_wins(player, dealer, chips)
            #Push
            else:
                push(player, dealer)
        
        # Inform Player of their chips total 
        print("\nPlayer's winnings total:", chips.total, "chips")
        
        # Ask to play again
        play_again = input("\nWould you like to play again? Yes or No: ").lower()
        # Yes
        if(play_again == "yes"):
            playing = True
            continue
        # No
        else:
            print("\nThanks for playing. Come again soon.\n")
            break

play_game()