# Building new Blackjack game alongside tests.

#for random deal generation
import random

# declare variable for player and dealer cards
# canHit function needs way of determining whether player or dealer
# so dealer starts with 0 and player starts with 1 always
playerCards = []
dealerCards = []
round = 'player'

def clearHand(hand):
    """Clears all cards from the hand, i.e. new game, and resets round to player"""
    global round
    hand.clear()
    round = 'player'
    return

def deal(hand, numberOfCards):
    """Deals that number of cards to the specified hand"""
    cardValues = [2,3,4,5,6,7,8,9,10,10,10,10,11]

    i = 0
    while i < numberOfCards:
        dealtCard = cardValues[random.randrange(0,13)]
        hand.append(dealtCard)
        i = i + 1
    return

def checkBlackjack(hand):
    """Checks if the hand has a valid Blackjack (2 cards only totalling 21)"""
    if len(hand) == 2 and sum(hand) == 21:
        return True
    else:
        return False

def canHit(hand, type):
    """Checks if the hand is allowed to hit based on whether player or dealer"""

    global round
    
    # if player, check under 21
    if type == 'player' and sum(hand) < 21:
        return True

    # if player and exactly 21, then dealer's turn
    if type == 'player' and sum(hand) == 21:
        round = 'dealer'
        return False

    # if dealer, check under 17
    elif type == 'dealer' and sum(hand) < 17:
        return True

    # if player/dealer and previous checks failed, then cannot hit
    elif type == 'player' or type == 'dealer':
        return False

    # if none of the above triggered, then error state, e.g. wrong type passed
    else:
        return 'Error'

def tableStatus(round, playerCards, dealerCards):
    """ Display the cards and their totals. Format depends on if still player's round
    or dealer's"""
    if round == 'player':
        print("You have been dealt: ", playerCards, "your total is: ", sum(playerCards))
        print("The dealer is showing: ", dealerCards)
        return
    elif round == 'dealer':
        print("Your total is: ", sum(playerCards))
        print("The dealer has been dealt: ", dealerCards, "which totals: ", sum(dealerCards))
        return
    elif round == 'draw':
        print("Your total is: ", sum(playerCards))
        print("The dealer has been dealt: ", dealerCards, "which totals: ", sum(dealerCards))
        print("Push! You get your money back.")
        newGame()
    elif round == 'playerwin':
        print("Your total is: ", sum(playerCards))
        print("The dealer has been dealt: ", dealerCards, "which totals: ", sum(dealerCards))
        print("You win!")
        newGame()
    elif round == 'playerbust':
        print("Your total is: ", sum(playerCards))
        print("You busted out. Sorry!")
        newGame()
    elif round == 'dealerbust':
        print("The dealer busted out! You win!")
        newGame()
    elif round == 'dealerwin':
        print("The dealer beat you this time. Never mind!")
        newGame()
    else:
        return 'Error'

def bustHand(hand):
    """ Check if hand over 21, if so busted """
    if sum(hand) > 21:
        return True
    else:
        return False

def playerHit(hand):
    """ if player hits, deal one more card"""
    deal(hand, 1)
    return

def stick():
    """ if player sticks, switch to dealer's round"""
    global round
    round = 'dealer'
    return

def checkHitOrStick(hand, action):
    """ checks user's input to see if valid and triggers function or error """
    if action.upper() == 'H' and canHit(hand, 'player'):
        playerHit(hand)

    elif action.upper() == 'S':
        stick()
    else:
        return 'Error'
        
def dealerAfterPlayerBlackjack(hand):
    """ if player has blackjack, dealer must have blackjack to draw, else player wins """
    print ("You have Blackjack, let's see how the dealer does...")
    global round
    deal(hand, 1)
    if checkBlackjack(hand):
        round = 'draw'
    else:
        round = 'playerwin'
    tableStatus(round, playerCards, dealerCards)
    

def newGame():
    newGame = input("Do you want to play again? y/n")
    if newGame == 'y':
        clearHand(playerCards)
        clearHand(dealerCards)
        main()
    else:
        exit()
        


def main():
    """ the script for the game, in main() so unittests don't
    accidentally run it on import"""

    # TO DO script errored if didn't declare global round in main()
    # but why are playerCards and dealerCards okay outside of main()?
    # Added to Level 2 variable studies
    
    global round
    
    # start new game
    clearHand(playerCards)
    clearHand(dealerCards)

    # deal initial cards
    deal(playerCards, 2)
    deal(dealerCards, 1)

    # show table Status
    tableStatus(round, playerCards, dealerCards)

    # check if player has blackjack and if so, check if dealer does, then game ends
    if checkBlackjack(playerCards):
        dealerAfterPlayerBlackjack(dealerCards)

    # otherwise option to hit or stick
    # TODO bug if [11,11] dealt, will just stop as cannot hit - postpone to OOO
    else:
        while round == 'player' and canHit(playerCards, 'player') and not bustHand(playerCards):
            action = input("Do you want to Hit (h) or Stick (s)?")
            checkHitOrStick(playerCards, action)
            tableStatus(round, playerCards, dealerCards)

        if bustHand(playerCards):
            round = 'playerbust'
            tableStatus(round, playerCards, dealerCards)

        while round == 'dealer' and canHit(dealerCards, 'dealer'):
            deal(dealerCards, 1)
            tableStatus(round, playerCards, dealerCards)

        if bustHand(dealerCards):
            round = 'dealerbust'
            tableStatus(round, playerCards, dealerCards)

        else:
            if sum(playerCards) > sum(dealerCards):
                round = 'playerwin'
                tableStatus(round, playerCards, dealerCards)
            elif sum(playerCards) == sum(dealerCards):
                round = 'draw'
                tableStatus(round, playerCards, dealerCards)
            else:
                round = 'dealerwin'
                tableStatus(round, playerCards, dealerCards)


if __name__ == "__main__":
    main()
