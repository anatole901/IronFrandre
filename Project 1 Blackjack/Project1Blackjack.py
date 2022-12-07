#!/usr/bin/env python
# coding: utf-8

# Project 1 : Blackjack

# In this project, we are creating a game of blackjack. We are implementing it in Python.
# 
# Plan of the project
# 
# I Rules of the game
#     1_ Overview
#     2_ Value of the cards
#     3_ The process of a round
#     4_ Ending the round
#     5_ Process of the game
# 
# II Creating thee data structure
# III Creating and shuffling the deck
# IV Implementing the game
# 

# I Rules of the game
# 
# 1_ Overview
# 
# The rules of the game that we are about to implement are the following.
# We are playing with a standard deck of 52 playing cards. There are between 1 and 4 players. Their objective is to beat the dealer that will play automatically. Each player and the dealer (I will refer to a player or the dealer as an actor) receive cards. Cards have a value. Each actor decides to either get more cards or stop and lock their score. A player wins if his score is greater than the dealer's but not greater than 21. If an actor's score is greater than 21, we say that he is busted. A busted player automatically loses whatever the dealer does.
# 
# 2_ Value of the cards
# 
# There are 52 cards in the deck separated in 4 colors that have no meaning in this game. Each color has 13 cards, ten numbered cards that range from 1 to 10 and 3 faces which are the jack, the queen and the king. The value of each face is 10, the value of each card between 2 and 10 is its number. The 1 has a value that depends on the actor's score. It stands for 11 unless the actor's score is greater than 21, in which case it stands for 1.
# 
# 3_ The process of a round
# 
# At the start of the game, each player is given a stack of 500 chips. At the start of every round, each player has the choice to either leave the game and lock his score as final or continue the game. Then the round starts and each player bets any even non-zero amount of chips not greater than 100 chips that he can afford.
# 
# The dealer receives one card and each player receives two cards that are revealed to all players. Any player that has two cards with the same value and can afford may choose to separate those in two hands, putting an identical bet on the second hand that is freshly created. We say that he splits his hand. Till the end of the round, he will manage his two hands separately and each hand can win or lose him the round separately. Then the first player choose to hit or to stand. If he hits, he draws an additionnal card, adding it to his hand. If his score becomes greater than 21, he is busted. If he stands, he locks his score for the round. He repeats until he either stands or is busted. Then each player does the same in turns. The dealer does the same, but automatically hits if his score is less than 17. If his score is between 17 and 21, he stands.
# 
# 4_ Ending the round
# 
# Each busted player loses the round. Any player that has a score greater than the dealer's wins the round. Use 0 as the dealer's score if he is busted. Any other player loses the round. Any losing player loses his bet and the chips are taken from his stack. Any winning player wins an amount of chips equal to his bet unless his score is 21 (we say that he has a blackjack), in which case he wins 150% of his bet.
# 
# 5_ Process of the game
# 
# The players play rounds until everyone either leaves the game at the start of a round or lose all his stack of chips. The winning player is the one with the biggest final score. Try your best!

# II Creating the data structure

# In[18]:


class Card() :
    def __init__(self, value, color) :
        if value.lower() in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king'] :
            self.value = value.title()
        else :
            raise ValueError("The value of a card is a number between 1 and 10, Jack, Queen or King.")
        if color.lower() in ['heart', 'spade', 'diamond', 'club'] :
            self.color = color.title()
        else :
            raise ValueError("The color of a card is among Club, Heart, Spade or Diamond.")   
    
class Player() :
    def __init__(self, name) :
        self.name = name
        self.hand = []
        self.isclone = False
        self.bet = 0
        self.stack = 500

    def empty_hand(self) :
        self.hand = []

    def draw_card(self, deck) :
        self.hand.append(deck[-1])
        deck.pop()


# III Creating and shuffling the deck

# In[19]:


import random

def shuffled_deck() :
    deck = [Card(value, color) for value in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king'] for color in ['heart', 'spade', 'diamond', 'club']]
    random.shuffle(deck)
    return deck


# IV Implementing the game

# First, let's define who the players are.

# In[20]:


def init_players() :
    num_players = '0'
    list_players = []
    while num_players not in ['1', '2', '3', '4'] :
        num_players = input("Please choose the number of players. Enter a number between 1 and 4.")
    for i in range(int(num_players)) :
        next_player = ''
        while next_player in ['', 'Dealer'] or next_player in list_players :
            next_player = input(f"Enter the name of player {i+1} other than \"Dealer\" or the name of another player.")
        list_players.append(next_player)
    return [Player(name) for name in list_players]

dealer = Player("Dealer")


# Then let's code some useful functions.

# In[21]:


def enter_bets(players) :
    deck = shuffled_deck()
    dealer.draw_card(deck)
    input(f"The dealer has drawn a {dealer.hand[0].value.title()} of {dealer.hand[0].color.title()}. Press enter to continue")
    active_players = players
    for player in players :
        bet = '1'
        while bet not in [str(item) for item in range(0, 101, 2)] or int(bet) > player.stack if bet.isdigit() else True :
            bet = input(f"Player {player.name}, your current stack is {player.stack}. Please enter your bet. Choose any even number between 0 and 100 not greater than your stack. Please consider that a bet of 0 will make you leave the game and make your stack of chips final.")
        player.bet = int(bet)
        if bet == '0' :
            active_players.remove(player)
    return (active_players, deck)

def hand_value (hand) :
    there_is_an_ace = False
    h_v = 0
    for card in hand :
        if card.value in [str(item) for item in range(1, 11)] :
            h_v += int(card.value)
            if card.value == '1' :
                there_is_an_ace = True
        else :
            h_v += 10
    if there_is_an_ace and h_v <= 11 :
        return h_v + 10
    else :
        return h_v

def string_from_hand (hand) :
    s = 'nothing'
    if hand != [] :
        s = f'a {hand[0].value} of {hand[0].color}'
    for card in hand[1:len(hand)] :
        s = s+f' and a {card.value} of {card.color}'
    return s


# In[22]:


def clone(player):
    c = Player(player.name+', your second hand')
    c.isclone = True
    c.bet = player.bet
    return c
    
def split (index, players, deck) :
    active_players = []
    p = players[index]
    c = clone(p)
    for i in range(index-1) :
        active_players.append(players[i])
    cardclone = p.hand[1]
    c.hand = [cardclone]
    p.hand.pop()
    p.draw_card(deck)
    c.draw_card(deck)
    active_players.append(p)
    active_players.append(c)
    for i in range(index+1, len(players)) :
        active_players.append(players[i])
    return active_players




    


# Then let's code how a round works. The core function.

# In[23]:



def round(players, deck) :
if players == [] :
    return[]
else :
    active_players = [player for player in players]
    index = 0
    
    for pl in players :
        pl.draw_card(deck); pl.draw_card(deck)
        if pl.hand[0].value == pl.hand[1].value and pl.stack >= pl.bet * 2 :
            do_pl_split = ''
            while do_pl_split.lower() not in ['yes', 'no'] :
                do_pl_split = input(f"Player {pl.name}, you have a double as a starting hand. You have {string_from_hand(pl.hand)}. Do you want to split your hand and bet an extra {pl.bet} chips? Enter \"Yes\" or \"No\".")
            if do_pl_split.lower() == 'yes' :
                active_players = split(index, active_players, deck)
                index += 2
            else :
                index += 1
    
    for pl in active_players :
        do_pl_hit = ''
        while hand_value(pl.hand) <= 21 and do_pl_hit.lower() != 'stand':
            while do_pl_hit.lower() not in ['hit', 'stand'] :
                do_pl_hit = input(f'Player {pl.name}. You have {string_from_hand(pl.hand)} in your hand. Your score is {hand_value(pl.hand)}. Do you want to hit or stand? Please enter \"Hit\" if you want to hit and \"Stand\" if you want to stand')
            if do_pl_hit.lower() == 'hit' :
                pl.draw_card(deck)
                do_pl_hit = ''
        if hand_value(pl.hand) > 21 :
            input(f'Player {pl.name}. You drew {string_from_hand([pl.hand[-1]])}. Your score is {hand_value(pl.hand)}. You are busted! Press Enter to continue.')
        else :
            input(f'Player {pl.name}. Your final score for this round is {hand_value(pl.hand)}. Press Enter to continue.')
    
    while hand_value(dealer.hand) < 17 :
        dealer.draw_card(deck)
    score_dealer = hand_value(dealer.hand)
    input(f"The Dealer drew {string_from_hand(dealer.hand)}. The Dealer's final score for this round is {score_dealer}. Press Enter to continue.")
    if score_dealer > 21 :
        input("The Dealer is busted! Press Enter to continue.")
        score_dealer = 0

    for i in range(len(active_players)) :
        pl_i = active_players[i]
        score_i = hand_value(pl_i.hand)
        if not pl_i.isclone :
            if score_i > score_dealer and score_i < 21 :
                pl_i.stack += pl_i.bet
                input(f'Player {pl_i.name}. You won your bet! You earned {pl_i.bet} extra chips! Press Enter to continue.')
            elif score_i > score_dealer and score_i == 21 :
                pl_i.stack += pl_i.bet * 3 // 2
                input(f'Player {pl_i.name}. You won your bet with a blackjack! Amazing! You earned {pl_i.bet * 3 // 2} extra chips! Press Enter to continue.')
            else :
                pl_i.stack -= pl_i.bet
                input(f'Player {pl_i.name}. You lost your bet. You lost {pl_i.bet} chips. Press Enter to continue.')
        else :
            if score_i > score_dealer and score_i < 21 :
                active_players[i-1].stack += pl_i.bet
                input(f'Player {pl_i.name}. You won your bet! You earned {pl_i.bet} extra chips! Press Enter to continue.')
            elif score_i > score_dealer and score_i == 21 :
                active_players[i-1].stack += pl_i.bet * 3 // 2
                input(f'Player {pl_i.name}. You won your bet with a blackjack! Amazing! You earned {pl_i.bet * 3 // 2} extra chips! Press Enter to continue.')
            else :
                active_players[i-1].stack -= pl_i.bet
                input(f'Player {pl_i.name}. You lost your bet. You lost {pl_i.bet} chips. Press Enter to continue.')
    for player in active_players :
        player.empty_hand()
    dealer.empty_hand()
    return [player for player in active_players if not player.isclone]


# Now let's implement the full game.

# In[24]:


def blackjack() :
    players = init_players()
    winner = [players[0]]
    active_players = [player for player in players]
    while active_players != [] :
        e_b = enter_bets(active_players)
        active_players = round(e_b[0], e_b[1])
    
    for player in players :
        input(f'Player {player.name}. Your final stack has {player.stack} chips. Well played! Press Enter to continue.')
        if player.stack > winner[0].stack :
            winner = [player]
        elif player.stack == winner[0].stack and player != winner[0] :
            winner.append(player)
    for player in winner :
        if player.stack > 500 :
            input(f'Player {player.name}. Well played! You won this game with a high score of {player.stack}!')


# Example

# In[25]:


blackjack()

