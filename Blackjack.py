
import  random

#Create a Class card 
class Card (object):
  RANKS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)
  SUITS = ('S', 'D', 'H', 'C')

  
  def __init__ (self, rank = 12, suit = 'S'):
    if (rank in Card.RANKS):
      self.rank = rank
    else:
      self.rank = 12

    if (suit in Card.SUITS):
      self.suit = suit
    else:
      self.suit = 'S'
  #the rank of the card for J Q K A
  #return a suit and a number
  def __str__ (self):
    if self.rank == 1:
      rank = 'A'
    elif self.rank == 13:
      rank = 'K'
    elif self.rank == 12:
      rank = 'Q'
    elif self.rank == 11:
      rank = 'J'
    else:
      rank = self.rank
    return str(rank) + self.suit

  def __eq__ (self, other):
    return (self.rank == other.rank)

  def __ne__ (self, other):
    return (self.rank != other.rank)

  def __lt__ (self, other):
    return (self.rank < other.rank)

  def __le__ (self, other):
    return (self.rank <= other.rank)

  def __gt__ (self, other):
    return (self.rank > other.rank)

  def __ge__ (self, other):
    return (self.rank >= other.rank)

#Create a Deck Class
class Deck (object):
  #this will include all 52 cards in the deck
  def __init__ (self):
    self.deck = []
    for suit in Card.SUITS:
      for rank in Card.RANKS:
        card = Card (rank, suit)
        self.deck.append(card)
  #shuffle the deck, so its all random.
  def shuffle (self):
    random.shuffle (self.deck)
  #when deal the card, take the first card from the desk and return it.
  #if no more card is in the deck, return None
  def deal (self):
    if len(self.deck) == 0:
      return None
    else:
      return self.deck.pop(0)

#Create a class for Player
class Player (object):
  # cards is a list of card objects
  def __init__ (self, cards):
    self.cards = cards
  #append 1 card to the player
  def hit (self, card):
    self.cards.append(card)

  #getPoints return the point each player has 
  def getPoints (self):
    count = 0
    for card in self.cards:
      if card.rank > 9:
        count += 10
      elif card.rank == 1:
        count += 11
      else:
        count += card.rank

    # deduct 10 if Ace is there and needed as 1
    for card in self.cards:
      if count <= 21:
        break
      elif card.rank == 1:
        count = count - 10
    
    return count

  # does the player have 21 points or not
  def hasBlackjack (self):
    return len (self.cards) == 2 and self.getPoints() == 21

  # complete the code so that the cards and points are printed 
  def __str__ (self):
    result=""
    for c in self.cards:
      result = result +str(c)+" "
    result = result + "- "+str(self.getPoints())+ " points"
    return result

    

# Dealer class inherits from the Player class

#dealer only show 1 card (players show both cards)
class Dealer (Player):
  def __init__ (self, cards):
    Player.__init__ (self, cards)
    self.show_one_card = True

  # over-ride the hit() function in the parent class
  # add cards while points < 17, then allow all to be shown
  def hit (self, deck):
    self.show_one_card = False
    while self.getPoints() < 17:
      self.cards.append (deck.deal())

  # return just one card if not hit yet by over-riding the str function
  def __str__ (self):
    if self.show_one_card:
      return str(self.cards[0])
    else:
      return Player.__str__(self)

#Create a Class Blackjack
class Blackjack (object):

  #first we need to have a shuffled deck, and need to know how many people are playing(receive from main().
  def __init__ (self, numPlayers = 1):
    self.deck = Deck()
    self.deck.shuffle()

    self.numPlayers = numPlayers
    self.Players = []

    # create the number of players specified
    # each player gets two cards
    for i in range (self.numPlayers):
      self.Players.append (Player([self.deck.deal(), self.deck.deal()]))

    # create the dealer
    # dealer gets two cards
    self.dealer = Dealer ([self.deck.deal(), self.deck.deal()])

  def play (self):
    # Print the cards that each player has
    for i in range (self.numPlayers):
      print ('Player ' + str(i + 1) + ': ' ,(self.Players[i]))

    # Print the cards that the dealer has
    print ('Dealer: ' ,self.dealer ,'\n')

    # Each player hits until he says no
    #if the players have Blackjack, we skip its input and go on to the next player
    playerPoints = []
    for i in range (self.numPlayers):
      while True:
        if self.Players[i].getPoints() == 21:
          break
        else:
          choice = input ('Player '+str(i+1)+', do you want to hit? [y / n]: ')
          if choice in ('y', 'Y'):
            (self.Players[i]).hit (self.deck.deal())
            points = (self.Players[i]).getPoints()
            print ('Player ' + str(i + 1) + ': ' , self.Players[i])
            if points >= 21:
              break
          else:
            break
        
      print ("")
      playerPoints.append ((self.Players[i]).getPoints())

    # Dealer's turn to hit if dealer point is below 17, continue to hit until dealer point >= 17
    self.dealer.hit (self.deck)
    dealerPoints = self.dealer.getPoints()
    print ("Dealer:",self.dealer)

    #display each player's result and compare it with dealer.
    #and print out the result
    player=1
    for i in self.Players:
      if(i.getPoints()<=21 and i.getPoints()>dealerPoints) or ((i.getPoints()<=21 and dealerPoints > 21)):
        print ("Player",player,"wins")
        player+=1
      elif(i.getPoints()>21) or (i.getPoints()<=21 and i.getPoints()<dealerPoints):
        print ("Player",player,"loses")
        player+=1
      elif(i.getPoints()<=21 and dealerPoints <= 21 and i.getPoints()==dealerPoints):

        #if player and dealer has the same points (below 21), see if dealer or player got a blackjack
        if(i.hasBlackjack() and not self.dealer.hasBlackjack()):
          print ("Player",player,"wins")
        elif(not i.hasBlackjack() and self.dealer.hasBlackjack()):
          print ("Player",player,"loses")
        else:
          print ("Player",player,"Tie")
        player+=1
    

     

def main ():
  #Ask for the number of players in the game at the beginning.
  numPlayers = eval (input ('Enter number of players: '))
  print ("")
  while (numPlayers < 1 or numPlayers > 6):
    numPlayers = eval (input ('Enter number of players: '))
  game = Blackjack (numPlayers)
  game.play()
  print("")
  Again= input("do you want to play again? yes/ press any key to exit ")
  if Again == "yes":
    main()
  else:
    print
    

    
main()
