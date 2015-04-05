#import numpy
import random, itertools
#import pylab

class Cards(object):#generates numDecks decks of cards. 
	def __init__(self, numDecks):
		self.numDecks = numDecks
		self.cards = list(itertools.product(range(1,14),['Clubs', 'Diamonds', 'Hearts', 'Spades'], range(numDecks)))
		self.count = 0

	def getCards(self): #Returns list of cards
		return self.cards
	
	def getCount(self): #indicates where in the deck we are
		return self.count

	def burn(self, num): #Moves to the next card in the deck
		self.count += num

	def nextCard(self): #returns top card from deck and moves to the next
		self.count += 1
		return self.cards[self.count-1]

	def shuffle(self): 
		random.shuffle(self.cards)
		self.count = 0

	def deal(self, players, numCards): #should have dealer as players[-1]
		for j in range(len(players)):
			players[j].setHand([self.cards[self.count+ j+(i * len(players))] for i in range(numCards)])
		self.count += len(players) * numCards

class Player(object): 
	#This class should probably be separated into standard player and blackjackplayer
	
	def __init__(self, bank):
		self.bank = float(bank)
		self.hand = []
		self.bust = False
		self.doubledhands = []
		self.wincount = 0	
	
	def getBank(self):
		return self.bank

	def getWinCount(self):
		return self.wincount

	def clearWinCount(self):
		self.wincount = 0

	def setHand(self,cards):
	#Sets the players first hand (does not incorperate the possibilioty of multiple hands)
		self.hand.append(Hand(cards))

	def getHand(self, num):
	#player can have multiple hands (for the purpose of splitting)
		return self.hand[num-1]

	def getHands(self):
	#Returns all of the players current hands
		return self.hand	

	def clearHand(self):
		self.hand = []

	def deposit(self, dep):
		self.bank += dep 

	def dealerHit(self):
	#This is a dealer's hit strategy
		if self.getHand(1).finalBJTotal() >= 17:
			return False
		else:
			return True	

	def optimalHit(self,hand, dealerCard):
	#This function determines how a player should act according to their cards and the one card that the dealer is showing.
		if hand.getBJTotal()>31:
		#Note the 31 here because this is how I have chosen to implement the "Ace Case"
			return 'Stand'
		if hand.hasAce() == False:
			if hand.hasPair() == False:
				if hand.getBJTotal() >= 17:
					return 'Stand'
				if dealerCard in {2,3,4,5,6}:
					if hand.getBJTotal()>11:						
						if dealerCard in {2,3} and hand.getBJTotal() == 12:							
							return 'Hit'
						else:
							return 'Stand'
					if hand.getBJTotal() >= 9:
						if dealerCard == 2 and hand.getBJTotal() == 9:
							return 'Hit'
						else:
							return 'Double'
					if hand.getBJTotal() >= 5:
						return 'Hit'

				if hand.getBJTotal() not in {10, 11}:
					return 'Hit'
				if hand.getBJTotal() == 10:
					if dealerCard in {7,8,9}:
						return 'Double'
					else:
						return 'Hit'  
				if dealerCard == 1:
					return 'Hit'
				else:
					return 'Double'
			else:
				if hand.getCards()[0][0] in {2, 3}:
					if dealerCard in {2,3,4,5,6,7}:
						return 'Split'
					else:
						return 'Hit'
				if hand.getCards()[0][0] == 4:
					if dealerCard in {5,6}:
						return 'Split'
					else:
						return 'Hit'
				if hand.getCards()[0][0] == 5:
					if 1<dealerCard<10:
						return 'Double'
					else:
						return 'Hit'
				if 5<hand.getCards()[0][0]<10:	
					if dealerCard in {2,3,4,5,6}:
						return 'Split'
					if hand.getCards()[0][0] == 6:
						return 'Hit'
					if hand.getCards()[0][0] == 7:
						if dealerCard == 7:
							print "how often"
							return 'Split'
						return 'Hit'
					if hand.getCards()[0][0] == 8:
						return 'Split'
					if hand.getCards()[0][0] == 9:
						if dealerCard in {2,3,4,5,6,8,9}:
							return 'Split'
						else:
							return 'Stand'
				if hand.getCards()[0][0] >= 10:
					return 'Stand'
		else:
			if hand.hasPair()==True:
				return 'Split'
			if hand.getBJTotal() in {19,20,21, 29,30,31}:
				return 'Stand'
			if hand.getBJTotal() in {18, 28}:
				if hand.getBJTotal() == 28:
					return 'Stand'
				if dealerCard in {2,7,8}:
					return 'Stand'
				if dealerCard in {3,4,5,6}:
					return 'Double'
				return 'Hit'
			if hand.getBJTotal() in {17, 27}:
				if hand.getBJTotal() == 27:
					return 'Stand'
				if dealerCard in {3,4,5,6}:
					return 'Double'
				return 'Hit'
			if hand.getBJTotal() in {15,16,25,26}:
				if hand.getBJTotal in {25,26}:
					if dealerCard in {2,3,4,5,6}:
						return 'Stand'
					else:
						return 'Hit'
				if dealerCard in {4,5,6}:
					return 'Double'
				return 'Hit'
			if hand.getBJTotal() in {13,14,23,24}:
				if hand.getBJTotal() in {23,24}:
					if dealerCard in {2,3,4,5,6}:
						return 'Stand'
					else:
						return 'Hit'
				if dealerCard in {5,6}:
					return 'Double'
				return 'Hit'
			if hand.getBJTotal() in {12, 22}:
				if dealerCard in {4,5,6}:
					return 'Stand'
				else:
					return 'Hit'	
		print "Oops you missed a case"

	def split(self,hand,deck):
		#Splits pairs into two hands and deals one more card to each
		self.hand.remove(hand)
		self.hand.append(Hand([hand.getCards()[0], deck.nextCard()]))
		self.hand.append(Hand([hand.getCards()[1], deck.nextCard()]))

	def turn(self,hand,dealerCard, deck):
		#This function simulates a players turn
		while self.optimalHit(hand, dealerCard) != 'Stand':
			if self.optimalHit(hand, dealerCard) == 'Hit':
				hand.newCard(deck)
				self.turn(hand, dealerCard, deck)
			if self.optimalHit(hand, dealerCard) == 'Double':
				hand.newCard(deck)
				self.doubledhands.append(self.hand.index(hand))
				break
			if self.optimalHit(hand, dealerCard) == 'Split':
				self.split(hand,deck)
				for hand in self.getHands():
					self.turn(hand, dealerCard, deck)

	def update(self, bet, dealer):
		#determines if a player wins agains the dealer and edits bank accounts accordingly
		for h in self.hand:
			x = 1
			if len(self.doubledhands) > 0:
				for i in self.doubledhands:
					if self.hand.index(h) == i:
						x = 2
			if h.bust() == False and dealer.getHand(1).bust() ==True:
					self.deposit(x * bet)
					dealer.deposit(-(x * bet))
					self.wincount+=1
			else:
				if h.bust() == True or h.underDealer(dealer) == True:
					self.deposit(- (x * bet))
					dealer.deposit(x * bet)
				else:
					if h.push(dealer) == True:
						pass
					else:
						self.deposit(x * bet)
						dealer.deposit(-(x * bet))
						self.wincount +=1

class Hand(object):
	#A hand of cards is a list with some functionality
	def __init__(self,cards):
		self.cards = cards

	def getCards(self):
		return self.cards

	def newCard(self, deck): 
		self.cards.append(deck.nextCard())

	def hasAce(self):
		for i in range(len(self.cards)):
			if self.cards[i][0] == 1:
				return True
		return False

	def hasPair(self):
		if len(self.cards) == 2 and self.cards[0][0] == self.cards[1][0]:
			return True
		return False	

	def getBJTotal(self):
		tot = 0
		for i in range(len(self.cards)):
			if 1 < self.cards[i][0] < 11:
				tot += self.cards[i][0]
			else:
				if self.cards[i][0] > 10:
					tot += 10
				else:
					tot += 11
		return tot

	def finalBJTotal(self):
		if self.hasAce() == False:
			return self.getBJTotal()
		if self.getBJTotal() > 21:
			return self.getBJTotal() - 10
		else:
			return self.getBJTotal()
	
	def push(self,dealer):
		if self.finalBJTotal() == dealer.getHand(1).finalBJTotal():
			return True
		else:
			return False

	def underDealer(self, dealer):
		if self.finalBJTotal() < dealer.getHand(1).finalBJTotal():
			return True
		else:
			return False

	def bust(self):
		if self.finalBJTotal() > 21:
			return True
		else:
			return False

def roundBJ(deck, players, bets):
	deck.deal(players, 2)
	for i in range(len(players[:-1])):
		if players[i].getHand(1).finalBJTotal() == 21:
			players[i].deposit(float(bets[i]) * 1.5)
			players[-1].deposit(-float(bets[i]) * 1.5)
			players[i].clearHand()
		else:
			players[i].turn(players[i].getHand(1),players[-1].getHand(1).getCards()[0][0], deck)

	while players[-1].dealerHit() == True:
		players[-1].getHand(1).newCard(deck)

	for i in range(len(players[:-1])):
		players[i].update(bets[i], players[-1])
		players[i].clearHand()
	players[-1].clearHand()
	




#Simulation
deck = Cards(15)
deck.shuffle()

joe = Player(0)
bob = Player(0)
doug = Player(0)
dealer = Player(0)
players = [joe,bob,doug,dealer]


# for turns in range(10000):
# 	if deck.getCount() > len(deck.getCards())- 6*len(players):
# 		deck.shuffle()
# 	roundBJ(deck, players,[1,1,1])




# for p in players[:-1]:
# 	print "Win percentage = ", p.getWinCount()/float(10000)*100
# 	print p.getBank()
# print dealer.getBank()

# print deck.getCount()
# joe.split(joe.getHands()[0], deck)
# print joe.getHand(1), joe.getHand(2)
# joe.split(joe.getHands()[1], deck)
# print joe.getHand(1), joe.getHand(2), joe.getHand(3)



#print joe.getHands()[0].getCards(), joe.getHands()[1].getCards()
# for i in range(5000):
# 	roundBJ(deck, players, [1, 2,0])
# print joe.getBank(), bob.getBank(), dealer.getBank()
# print (joe.getBank()+ bob.getBank() + dealer.getBank())


# x = Hand([deck.nextCard() for i in {1,2}])
# deck.burn(1)
# y = Hand([deck.nextCard() for i in {1,2}])
# z = Hand([deck.getCards()[2], deck.getCards()[-1]])
# w = Hand([deck.getCards()[1], deck.getCards()[-3]])
# u = Hand([deck.nextCard() for i in {1,2,3}])
#print w.finalBJTotal(), w.bust(),  u.finalBJTotal(), u.bust()

# dealer.setHand(z)
# print w.getCards()
# print w.push(dealer), x.underDealer(dealer)

#Testing Hand
#print x.hasAce(), y.hasAce(), x.hasPair(), y.hasPair()
#print x.finalBJTotal(), y.getBJTotal(), z.getBJTotal(), z.finalBJTotal()

# print joe.getHand(1).getCards(), dealer.getHand(1).getCards()
# print joe.optimalHit(joe.getHand(1), dealer.getHand(1).getCards()[0][0]), dealer.dealerHit()
# joe.turn(joe.getHand(1), dealer.getHand(1).getCards()[0][0], deck)
# print joe.getHand(1).getCards()


# for something in range(100):
# 	joe.clearHand()
# 	h = [(7, 'Diamonds', 0), (7, 'Hearts', 0)]
# 	joe.setHand(h)
# 	deck.shuffle()
# 	c = deck.nextCard()
# 	joe.turn(joe.getHand(1), c[0], deck)
# 	if len(joe.getHands())>2:
# 		print len(joe.getHands())


# d = [i for i in range(2,14)]
# d.append(1)
# joe = Player(0)
#Tests optimal Hit Strategy for pairs. 
# h = [[(i,'clubs',0), (i,'clubs',0)] for i in range (2,14)]
# h.append([(1,'clubs',0), (1,'clubs',0)])
# for l in range(len(h)):
# 	joe.setHand(h[l])
# 	print [joe.optimalHit(joe.getHand(1),k) for k in d]
# 	joe.clearHand()

#Test soft hand with 2 cards
# h = [[(1,'clubs',0), (i,'clubs',0)] for i in range (2,10)]
# for l in range(len(h)):
# 	joe.setHand(h[l])
# 	print [joe.optimalHit(joe.getHand(1),k) for k in d]
# 	joe.clearHand()

#Test hand without pairs or aces and 2 cards up to
# h = [[(12,'clubs',0), (i,'clubs',0)] for i in range (2,14)]
# for l in range(len(h)):
# 	joe.setHand(h[l])
# 	print [joe.optimalHit(joe.getHand(1),k) for k in d]
# 	joe.clearHand()

#Test with 3 cards
# h = [[(12,'clubs',0), (i,'clubs',0)] for i in range (2,14)]
# for l in range(len(h)):
# 	joe.setHand(h[l])
# 	print [joe.optimalHit(joe.getHand(1),k) for k in d]
# 	joe.clearHand()



def userRoundBJ(deck, players):
	print "Place your bet"
	x = raw_input()
	bets = [int(x) for i in range(len(players[:-1]))]
	deck.shuffle()
	deck.deal(players, 2)
	def askTurn(playa, hand):
		command = ""
		if hand.finalBJTotal() == 21 and len(hand.getCards()) == 2:
			print "Player", str(i+1), " Blackjack with", hand.getCards() 
			playa.deposit(float(bets[i]) * 1.5)
			players[-1].deposit(-float(bets[i]) * 1.5)
			playa.getHands().remove(hand)
		else:
			while command != 2:
				if hand.finalBJTotal() > 21:
					print "BUST with", hand.finalBJTotal()
					break
				if hand.hasAce() == True and hand.hasPair() == True:
					print "You have a pair of aces"
				if hand.hasAce() == True and hand.hasPair() == False:
					print "You have;", hand.getBJTotal(), "(with Ace)"
				if hand.hasAce() == False and hand.hasPair() == True:
					print "You have ", players[i].getHand(1).getBJTotal(), "a pair of", int(players[i].getHand(1).getBJTotal()/float(2))
				if hand.hasAce() == False and hand.hasPair() == False:
					print "You have ", hand.getBJTotal(), "(hard)"
				if players[-1].getHand(1).getCards()[0][0] >= 10:
					print "dealer showing", 10
				else:
					print "dealer showing", players[-1].getHand(1).getCards()[0][0]

				print "You should ", playa.optimalHit(hand, players[-1].getHand(1).getCards()[0][0])
				print "Press; 1-Hit, 2-Stand, 3-Split, 4-DoubleDown"
				command = raw_input()
				if command == str(1):
					hand.newCard(deck)					
				if command == str(2):
					break
				if command == str(3):
					playa.split(hand,deck)
					for h in playa.getHands():
						askTurn(playa, h)

				if command == str(4):
					hand.newCard(deck)
					print "Your now have", hand.finalBJTotal(), "with ", hand.getCards()
					break

	for i in range(len(players[:-1])):
		askTurn(players[i], players[i].getHand(1))	

	while players[-1].dealerHit() == True:
		players[-1].getHand(1).newCard(deck)

	print "Dealer has; ", players[-1].getHand(1).finalBJTotal()

	for i in range(len(players[:-1])):
		players[i].update(bets[i], players[-1])
		players[i].clearHand()
	players[-1].clearHand()





def oneplayer():
#This allows you to play a one player game and tells you what to do (This is for testing optimalHit strategy)
	d = Cards(1)
	usr = Player(0)
	dealer = Player(0)
	p = [usr, dealer]	
	playagain = ""
	while playagain != "n":
		userRoundBJ(d,p)
		print "You have $",usr.getBank()
		print "Again? y or n"
		playagain = raw_input()

oneplayer()
