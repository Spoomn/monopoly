import random
import sys
import pandas as pd

# This class is to initialize what a player is
# The player has a starting position and starting money, per monopoly rules
class Player:
    def __init__(self):
        self.position = 0
        self.money = 1500
        self.jail = False
        self.get_out_of_jail_free_cards = 0

    def move_to(self, position):
        self.position = position
        # print(f"Player moved to {self.position}")

    def move_by(self, spaces):
        self.position = (self.position + spaces) % 40
        # print(f"Player moved by {spaces} to {self.position}")

    def change_money(self, amount):
        self.money += amount
        # print(f"Player's money changed by {amount} to {self.money}")

    def go_to_jail(self):
        self.jail = True
        self.position = 10

    def get_out_of_jail_free_card(self):
        self.get_out_of_jail_free_cards += 1
        # print(f"Player received a Get Out of Jail Free card and now has {self.get_out_of_jail_free_cards} cards")

# This class is to initialize what a deck is
# The deck has cards and a discard pile, and can shuffle the deck, draw a card, and discard a card
# The ChanceDeck and CommunityChestDeck classes inherit from the Deck class
class Deck:
    def __init__(self, cards):
        self.cards = cards
        self.discard_pile = []
        self.shuffle_deck()

    def shuffle_deck(self):
        random.shuffle(self.cards)

    def draw(self):
        if self.cards == []:
            self.cards = self.discard_pile
            self.discard_pile = []
            self.shuffle_deck()
        return self.cards.pop(0)

    def discard(self, card):
        self.discard_pile.append(card)

# The ChanceDeck inherits from the Deck class and initializes the cards in the Chance deck
class ChanceDeck(Deck):
    def __init__(self):
        cards = [
            ("Advance to Boardwalk", lambda player: player.move_to(39)),
            ("Advance to Go (Collect $200)", lambda player: player.move_to(0) and player.change_money(200)),
            ("Advance to Illinois Avenue. If you pass Go, collect $200", lambda player: player.move_to(24) or player.change_money(200) if player.position > 24 else None),
            ("Advance to St. Charles Place. If you pass Go, collect $200", lambda player: player.move_to(11) or player.change_money(200) if player.position > 11 else None),
            ("Advance to the nearest Railroad. If unowned, you may buy it from the Bank. If owned, pay owner twice the rental to which they are otherwise entitled", lambda player: player.move_to(5) if player.position < 5 else player.move_to(15) if player.position < 15 else player.move_to(25) if player.position < 25 else player.move_to(35)),
            ("Advance token to nearest Utility. If unowned, you may buy it from the Bank. If owned, throw dice and pay owner a total ten times amount thrown.", lambda player: player.move_to(12) if player.position < 12 else player.move_to(28)),
            ("Bank pays you dividend of $50", lambda player: player.change_money(50)),
            ("Get Out of Jail Free", lambda player: player.get_out_of_jail_free_card()),
            ("Go Back 3 Spaces", lambda player: player.move_by(-3)),
            ("Go to Jail. Go directly to Jail, do not pass Go, do not collect $200", lambda player: player.go_to_jail()),
            ("Make general repairs on all your property. For each house pay $25. For each hotel pay $100", lambda player: player.change_money(-25)), 
            ("Speeding fine $15", lambda player: player.change_money(-15)),
            ("Take a trip to Reading Railroad. If you pass Go, collect $200", lambda player: player.move_to(5) or player.change_money(200) if player.position > 5 else None),
            ("You have been elected Chairman of the Board. Pay each player $50", lambda player: player.change_money(-50)),
            ("Your building loan matures. Collect $150", lambda player: player.change_money(150)),
        ]
        super().__init__(cards)

# The CommunityChestDeck inherits from the Deck class and initializes the cards in the Community Chest deck
class CommunityChestDeck(Deck):
    def __init__(self):
        cards = [
            ("Advance to Go (Collect $200)", lambda player: player.move_to(0) and player.change_money(200)),
            ("Bank error in your favor. Collect $200", lambda player: player.change_money(200)),
            ("Doctor’s fee. Pay $50", lambda player: player.change_money(-50)),
            ("From sale of stock you get $50", lambda player: player.change_money(50)),
            ("Get Out of Jail Free", lambda player: player.get_out_of_jail_free_card()),
            ("Go to Jail. Go directly to jail, do not pass Go, do not collect $200", lambda player: player.go_to_jail()),
            ("Holiday fund matures. Receive $100", lambda player: player.change_money(100)),
            ("Income tax refund. Collect $20", lambda player: player.change_money(20)),
            ("It is your birthday. Collect $10 from every player", lambda player: player.change_money(10)),
            ("Life insurance matures. Collect $100", lambda player: player.change_money(100)),
            ("Pay hospital fees of $100", lambda player: player.change_money(-100)),
            ("Pay school fees of $50", lambda player: player.change_money(-50)),
            ("Receive $25 consultancy fee", lambda player: player.change_money(25)),
            ("You are assessed for street repair. $40 per house. $115 per hotel", lambda player: player.change_money(-40)),
            ("You have won second prize in a beauty contest. Collect $10", lambda player: player.change_money(10)),
            ("You inherit $100", lambda player: player.change_money(100)),
        ]
        super().__init__(cards)


class MonopolyGame:
    def __init__(self):
        # Initialize the player
        self.player = Player()
        self.chance_deck = ChanceDeck()
        self.community_chest_deck = CommunityChestDeck()

        # The board is a list of tuples, where each tuple represents a square on the board.
        # The first element of the tuple is the name of the square, and the second element is the number of times the player has landed on that square.
        # The index in the board list represents the position of the square on the board.
        self.board = [('Go', 0), # 0
                      ('Mediterranean Avenue', 0), 
                      ('Community Chest1', 0), # 2 
                      ('Baltic Avenue', 0), 
                      ('Income Tax', 0), 
                      ('Reading Railroad', 0),
                      ('Oriental Avenue', 0), 
                      ('Chance1', 0), # 7
                      ('Vermont Avenue', 0), 
                      ('Connecticut Avenue', 0), 
                      ('Jail', 0), 
                      ('St. Charles Place', 0),
                      ('Electric Company', 0), 
                      ('States Avenue', 0), 
                      ('Virginia Avenue', 0), 
                      ('Pennsylvania Railroad', 0), 
                      ('St. James Place', 0),
                      ('Community Chest2', 0), # 17
                      ('Tennessee Avenue', 0), 
                      ('New York Avenue', 0), 
                      ('Free Parking', 0), 
                      ('Kentucky Avenue', 0),
                      ('Chance2', 0), # 22
                      ('Indiana Avenue', 0), 
                      ('Illinois Avenue', 0), 
                      ('B&O Railroad', 0), 
                      ('Atlantic Avenue', 0), 
                      ('Ventnor Avenue', 0),
                      ('Water Works', 0), 
                      ('Marvin Gardens', 0), 
                      ('Go To Jail', 0), 
                      ('Pacific Avenue', 0), 
                      ('North Carolina Avenue', 0),
                      ('Community Chest3', 0), # 33
                      ('Pennsylvania Avenue', 0), 
                      ('Short Line', 0), 
                      ('Chance3', 0), # 36
                      ('Park Place', 0), 
                      ('Luxury Tax', 0),
                      ('Boardwalk', 0),]

    # The play function executes the game loop n times
    def play(self, strategy, n):
        # Initialize the player
        self.player = Player()

        # initializes doubles count to 0
        moves = 0
        doubles_count = 0
        board_size = len(self.board)

        # The game loop
        while moves <= n:
            # Roll the dice to determine how many spaces the player moves
            dice_roll = roll_dice()
            # Increment the number of moves made
            moves += 1
            # Move the player according to the dice roll
            self.player.position += dice_roll[0]

            # Check if the player has passed Go
            if self.player.position >= 40:
                self.player.position -= 40
                self.player.money += 200
                # print("Player passed Go and collected $200")
                # print("Player now has $", self.player.money)
            self.player.position %= board_size
            # print(f"Player rolled {dice_roll[0]} and moved to {self.board[self.player.position][0]}")
            
            # Implements rule for going to jail if you roll three consecutive doubles on one turn 
            # as well as all of the other ways of being sent to jail (landing on Go to Jail or drawing Go to Jail cards)

            # Check for doubles 
            # if the player rolls doubles, increment the doubles count
            if dice_roll[1] == True:
                doubles_count += 1
            # if the player does not roll doubles, reset the doubles count
            else:
                doubles_count = 0
                
            # if the player rolls three doubles in a row, send them to jail
            if doubles_count == 3:
                self.player.position = 10
                self.player.jail = True
                # print("\nPlayer rolled three doubles in a row and is now in Jail\n")
                # reset the doubles count for the next turn
                doubles_count = 0



            ##########################################################################################################
        
            # After the move is made, we check the square the player landed on and implement the rules for that square
            # If the player lands on Community Chest or Chance, draw a card
            if self.player.position == 2 or self.player.position == 17 or self.player.position == 33:
                # print(f"Player landed on the {self.player.position}th square, {self.board[self.player.position][0]}")
                self.draw_card("Community Chest")
            if self.player.position == 7 or self.player.position == 22 or self.player.position == 36:
                # print(f"Player landed on the {self.player.position}th square, {self.board[self.player.position][0]}")
                self.draw_card("Chance")

            # Implement the rules for landing on go to jail
            if self.player.position == 30:
                self.board[self.player.position] = (self.board[self.player.position][0], self.board[self.player.position][1] + 1)
                self.player.position = 10
                self.player.jail = True

                # print("\nPlayer landed on Go To Jail and is now in Jail\n")

            # Check if the player is in Jail
            if self.player.jail == True:
                # Activate the strategy for getting out of Jail based on the argument passed

                if strategy == 1:
                    # Strategy A)  If you have a Get Out of Jail Free card, you must use it immediately.
                    # If you don’t have the card, then you should immediately assume you would have paid the $50 fine and gotten out of jail immediately.
                    # You should not try to roll doubles to get out of jail in this case.
                    if self.player.get_out_of_jail_free_cards >= 1:
                        self.player.get_out_of_jail_free_cards -= 1
                        self.player.jail = False
                        # print("Player used a Get Out of Jail Free card and is now out of Jail\n")
                    else:
                        # print("Player did not have a Get Out of Jail Free card and is now out of Jail by paying the fine\n")
                        self.player.money -= 50
                        self.player.jail = False

                elif strategy == 2:
                    # Strategy B) If you have a Get Out of Jail Free card, you must use it immediately.
                    # If you don’t have the card, then try to roll doubles for your next three iterations to see if you can get out of jail that way.
                    # If you have not gotten out of jail after three iterations, assume you would have paid the $50 fine on the fourth term and get out of jail on that turn.
                    if self.player.get_out_of_jail_free_cards >= 1:
                        self.player.get_out_of_jail_free_cards -= 1
                        # print("Player used a Get Out of Jail Free card and is now out of Jail\n")
                        self.player.jail = False
                    else:
                        # Try to roll doubles for the next three iterations
                        for i in range(3):
                            dice_roll = roll_dice()
                            if dice_roll[1] == True:
                                # print("Player rolled doubles and is now out of Jail\n")
                                self.player.jail = False
                                break
                            # else:
                                # print("Player did not roll doubles and is still in Jail\n")
                        # If the player has not rolled doubles after three iterations, pay the fine and get out of jail
                        if self.player.jail == True:
                            # print("Player did not roll doubles after three iterations and is now out of Jail by paying the fine\n")
                            self.player.money -= 50
                            self.player.jail = False

            # Keeps track of the number of times the player has landed on each square.
            self.board[self.player.position] = (self.board[self.player.position][0], self.board[self.player.position][1] + 1)

    # The draw_card function draws a card from the Chance or Community Chest deck and performs the action associated with the card
    def draw_card(self, deck_type):
        if deck_type == "Community Chest":
            card = self.community_chest_deck.draw()
        else:
            card = self.chance_deck.draw()
        
        # print(f"Drew {deck_type} card: {card[0]}")

        # Perform the action associated with the card
        card[1](self.player)

        # Discard the card
        if deck_type == "Community Chest":
            self.community_chest_deck.discard(card)
        else:
            self.chance_deck.discard(card)

    # The export_data function exports the data to an excel file
    def export_data(self, filename, n):
        data = {
            'Square': [square[0] for square in self.board],
            'Landed': [square[1] for square in self.board],
            'Percentage': [square[1] / sum([s[1] for s in self.board]) * 100 for square in self.board]
        }
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False) 

# The roll_dice function returns a random number between 1 and 6, twice
def roll_dice():
    # return a random number between 1 and 6, twice
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    sum = die1 + die2
    # doubles rule
    doubles = False
    if die1 == die2:
        doubles = True
    return sum, doubles


if __name__ == "__main__":
    # Create and start the game
    game = MonopolyGame()

    # Parse the cl arguments to choose strategy A or B and the number of moves
    args = sys.argv
    if len(args) < 3:
        print("Usage: python board.py <strategy> <moves>")
        sys.exit()
    strategy = int(args[1])
    n = int(args[2])
    game = MonopolyGame()
    game.play(strategy, n)
    game.export_data(f"TESTmonopoly_data_strategy_{strategy}_moves_{n}.xlsx", n)