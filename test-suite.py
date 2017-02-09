import unittest
import app

class BlackjackTestNewRound(unittest.TestCase):

# newRound - ensure that new round always starts with two empty hands
    def setUp(self):
        self.playerCards = [4,10,8]
        self.dealerCards = [10,6]
        
    def testClearHand(self):
        app.clearHand(self.playerCards)
        app.clearHand(self.dealerCards)
        self.assertEqual(len(self.playerCards), 0)
        self.assertEqual(len(self.dealerCards), 0)

class BlackjackTestDeals(unittest.TestCase):
    # ensure deal function only deals one card
    def setUp(self):
        self.playerCards = []
        self.dealerCards = []
    
    def testDeal(self):
        app.deal(self.playerCards, 2)
        app.deal(self.dealerCards, 1)

        self.assertEqual(len(self.playerCards), 2)
        self.assertEqual(len(self.dealerCards), 1)
        app.deal(self.playerCards, 1)
        self.assertEqual(len(self.playerCards), 3)


       
class BlackjackTestForBlackjack(unittest.TestCase):
    # check if a hand has blackjack.
    def setUp(self):
        self.playerCards = []
        self.dealerCards = []

    def testBlackjackTrue(self):
        # genuine Blackjack - 2 cards total 21
        self.playerCards.append(10)
        self.playerCards.append(11)
        self.assertTrue(app.checkBlackjack(self.playerCards))

        self.dealerCards.append(11)
        self.dealerCards.append(10)
        self.assertTrue(app.checkBlackjack(self.dealerCards))

    def testBlackjackFalse(self):
        # not Blackjack, more than 2 cards add up to 21
        self.playerCards.append(7)
        self.playerCards.append(8)
        self.playerCards.append(6)
        self.assertFalse(app.checkBlackjack(self.playerCards))

        self.dealerCards.append(9)
        self.dealerCards.append(4)
        self.dealerCards.append(8)
        self.assertFalse(app.checkBlackjack(self.dealerCards))

    def testBlackjackFalse2(self):
    # don't add up to 21
        self.playerCards.append(8)
        self.playerCards.append(10)
        self.assertFalse(app.checkBlackjack(self.playerCards))

        self.dealerCards.append(8)
        self.dealerCards.append(9)
        self.assertFalse(app.checkBlackjack(self.dealerCards))
        
class BlackjackHitAllowed(unittest.TestCase):
    # check if player or dealer allowed to hit
    def setUp(self):
        self.playerCards = []
        self.dealerCards = []

    # player max is 21, cannot hit if reached 21
    def testPlayerHitMax(self):
        self.playerCards.append(10)
        self.playerCards.append(11)
        self.assertFalse(app.canHit(self.playerCards, 'player'))

    def testPlayerHitBelowMax(self):
        self.playerCards.append(10)
        self.playerCards.append(10)
        self.assertTrue(app.canHit(self.playerCards, 'player'))

    # dealder max is 17, cannot hit if reached 17
    def testDealerHitMax(self):
        self.dealerCards.append(10)
        self.dealerCards.append(7)
        self.assertFalse(app.canHit(self.dealerCards, 'dealer'))

    def testDealderHitBelowMax(self):
        self.dealerCards.append(10)
        self.dealerCards.append(6)
        self.assertTrue(app.canHit(self.dealerCards, 'dealer'))
        
    def testBadTypeError(self):
        self.assertEqual(app.canHit(self.playerCards, 'badtype'), 'Error')

class BlackjackTableStatus(unittest.TestCase):
    # check valid returns based on round

    def setUp(self):
        self.playerCards = []
        self.dealerCards = []

    def testTableStatus(self):
        self.assertIsNone(app.tableStatus('player',
                self.playerCards, self.dealerCards))
        self.assertIsNone(app.tableStatus('dealer',
                self.playerCards, self.dealerCards))
        self.assertEqual(app.tableStatus('',
                self.playerCards, self.dealerCards), 'Error')

class BlackjackBust(unittest.TestCase):
    # check if hand has busted, over 21
    def setUp(self):
        self.playerCards = []
        self.dealerCards = []

    def testBustPlayerHand(self):
        self.playerCards.append(10)
        self.playerCards.append(11)
        self.assertFalse(app.bustHand(self.playerCards))

        self.playerCards.append(1)
        self.assertTrue(app.bustHand(self.playerCards))

    def testBustDealerHand(self):
        self.dealerCards.append(10)
        self.dealerCards.append(11)
        self.assertFalse(app.bustHand(self.dealerCards))

        self.dealerCards.append(1)
        self.assertTrue(app.bustHand(self.dealerCards))

class BlackjackHit(unittest.TestCase):
    def setUp(self):
        self.playerCards = []

    def testPlayerHit(self):
        # check Hit adds just one card
        self.playerCards.append(3)
        self.playerCards.append(9)
        app.playerHit(self.playerCards)
        self.assertEqual(len(self.playerCards), 3)
        app.playerHit(self.playerCards)
        self.assertEqual(len(self.playerCards), 4)

class BlackjackStick(unittest.TestCase):
    def setUp(self):
        self.playerCards = [10,7]

    def testStick(self):
        app.stick()
        self.assertEqual(app.round, 'dealer')

class BlackjackCheckHitOrStick(unittest.TestCase):
    # check user inputs correctly processed
    def setUp(self):
        self.playerCards = [10,4]

    # have to check results of the playerHit or stick functions, as checkHitOrStick doesn't return anything
    # TODO find out if better way of checking a function is called- Level 2 unittest studies
    def testPlayerHitLowerCase(self):
        app.checkHitOrStick(self.playerCards, 'h')
        self.assertEqual(len(self.playerCards), 3)
        
    def testPlayerHitUpperCase(self):
        app.checkHitOrStick(self.playerCards, 'H')
        self.assertEqual(len(self.playerCards),3)

    def testPlayerStickLowerCase(self):
        app.checkHitOrStick(self.playerCards, 's')
        self.assertEqual(len(self.playerCards), 2)
        self.assertEqual(app.round, 'dealer')

    def testPlayerStickUpperCase(self):
        app.checkHitOrStick(self.playerCards, 'S')
        self.assertEqual(len(self.playerCards), 2)
        self.assertEqual(app.round, 'dealer')

    def testPlayerInvalidInput(self):
        self.assertEqual(app.checkHitOrStick(self.playerCards, 'x'), 'Error')
        


if __name__ == '__main__':
    unittest.main()
    
