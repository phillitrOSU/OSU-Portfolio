# Author: Trevor Phillips
# GitHub username: phillitrOSU
# Date: 5/21/2022
# Description: Classes for running a real estate game.

import random

class Space:
    """A space on the game board."""
    def __init__(self, name, space_number, rent):
        """Initializes a space with name, space number and rent amount."""
        self._name = name
        self._rent = rent
        self._space_number = space_number
        self._value = rent*5
        self._players = {}
        self._owner = None

    def get_rent(self):
        """Returns rent amount of space.
        :return self._rent: amount of rent to be paid to owner (integer)."""
        return self._rent

    def get_name(self):
        """Returns name of space.
        :return self._name: name of the space (string)."""
        return self._name

    def get_value(self):
        """Returns value of space (rent*5).
        :return self._value: returns the purchasing price of space (integer)."""
        return self._value

    def get_owner(self):
        """Returns the player who owns the space.
        :return self._owner: the player who owns the space (player object)"""
        return self._owner

    def get_players(self):
        """A list of players currently on the space. Returns an empty list of no players on the space.
        :return players: a list of the names of players on the space (list).
        """
        return list(self._players.keys())

    def add_player(self, player):
        """Updates the space players dictionary with a player object.
        :param player: player object
        """
        self._players[player.get_name()] = player

    def clear_player(self, player):
        """Removes a player object from the space player dictionary.
        :param player: player object
        """
        del self._players[player.get_name()]

    def set_owner(self, player):
        """Sets the player as the owner of the space.
        :param player: player object
        """
        self._owner = player

    def clear_owner(self):
        """Removes the owner of a space by setting the owner attribute to None."""
        self._owner = None

class Player:
    """A player in the game."""
    def __init__(self, name, balance):
        """Initializes player with name, balance and starting position of 0 (GO space)
        The player has no owned spaces when first initialized. They are added during gameplay.
        """
        self._name = name
        self._balance = balance
        self._position = 0
        self._owned_spaces = {}

    def get_name(self):
        """Returns player name.
        :return self._name: name of the player (string)"""
        return self._name

    def get_balance(self):
        """Returns player balance.
        :return self._balance: current balance of player (integer)"""
        return self._balance

    def get_position(self):
        """Returns player position (an index).
        :return self._position: current space index of player (integer)"""
        return self._position

    def get_owned_spaces(self):
        """Returns the properties owned by the player.
        :return self._owned_spaces: spaces that are owned by the player."""
        return self._owned_spaces

    def add_space(self, space):
        """Adds a space to the player's owned spaces.
        :param space: a space object
        """
        self._owned_spaces[space.get_name()] = space

    def set_position(self, position):
        """Sets player position at index given."""
        self._position = position

    def add_space(self, space):
        """Adds a space to the player's owned spaces.
        :param space: a space object
        """
        self._owned_spaces[space.get_name()] = space

    def pay(self, amount):
        """Reduces player balance by the amount. If player balance is less than amount,
        an InsufficientBalance exception is raised.
        :param amount: amount player will pay (integer)
        """
        self._balance -= amount

    def clear_spaces(self):
        """Removes all spaces from the player's owned spaces (for when player has lost)."""
        self._owned_spaces = {}

    def receive(self, amount):
        """Increase player balance by the amount.
        :param amount: amount player will receive (integer)
        """
        self._balance += amount

    def clear_balance(self):
        """Clears player balance.
        """
        self._balance = 0

class RealEstateGame:
    """A real estate game class."""
    def __init__(self):
        """Initializes the game with no arguments and creates empty dictionaries
        for the spaces and players to be added when initialized."""
        self._spaces = {}
        self._players = {}
        self._go_money = 0

    def create_spaces(self, go_money, rent_amounts):
        """Adds board spaces to spaces dictionary using randomly generated names to create Space class objects.
        :param go_money: integer amount of money received for passing go
        :param rent_amounts: amount of rent owed for each property corresponding to property indexes 1-24.
        """
        self._go_money = go_money
        self._spaces["GO"] = Space("GO", 0, 0)
        first_names = ["Python", "Java", "C", "Recursion", "LinkedList", "Dynamic Programming", "Assembly",
                       "Programmer", "Object Oriented",]
        last_names = ["Lane", "Village", "Avenue", "Boulevard", "Street", "Tower", "Cafe",
                      "Diner", "Railroad", "Corner", "Place", "Walk", "Square"]
        for space_num in range(len(rent_amounts)):
            name = random.choice(first_names) + " " + random.choice(last_names)
            while name in self._spaces:         # Check to make sure there are no duplicate names
                name = random.choice(first_names) + " " + random.choice(last_names)
            # If name is unique, add space to dictionary.
            self._spaces[name] = Space(name, space_num + 1, rent_amounts[space_num])

    def create_player(self, name, balance):
        """Creates a player object with a name and starting balance.
        :param name: The name of the player (string)
        :param balance: The starting balance of the player (integer)
        """
        if name in self._players:
            print("That name is already chosen!")
            return
        new_player = Player(name, balance)
        self._players[name] = new_player
        self._spaces["GO"].add_player(new_player)       # Start player on "GO" space

    def get_player_account_balance(self, player_name):
        """Returns the balance of the player.
        :param player: the player whose balance is requested
        :return balance: the balance of the player (integer)
        """
        return self._players[player_name].get_balance()

    def get_player_current_position(self, player_name):
        """Returns the index of the player's current space on the board.
        :param player_name: the name of the player whose position is requested
        :return position: current player space index (integer)
        """
        return self._players[player_name].get_position()

    def get_player_current_space(self, player_name):
        """Returns the space name of the player's current space on the board.
        :param player_name: the name of the player whose space is being determined
        :return space_name: the name of the space the player is currently on.
        """
        position = self.get_player_current_position(player_name)
        space_name = list(self._spaces)[position]
        return self._spaces[space_name]

    def buy_space(self, player_name):
        """Adds a property to a player's owned properties and reduces player account balance
        by the value of the property. Returns True. If the property cannot be legally purchased
        (already owned, insufficient balance), returns false.
        :param player_name: name of player who is attempting to buy the space (string)
        :return True: True if property successfully purchased
        :return False: if property cannot be purchased
        """
        player = self._players[player_name]
        balance = player.get_balance()
        space = self.get_player_current_space(player_name)
        value = space.get_value()

        # Check player balance, and space ownership to see if space can be purchased.
        # No one can buy "GO" space.
        if balance < value or space.get_name() == "GO" or space.get_owner() != None:
            return False

        else:
            player.pay(value)
            space.set_owner(player)
            player.add_space(space)
            return True

    def move_player(self, player_name, roll):
        """If the player balance is 0, returns immediately.
        Otherwise, moves the player the number of spaces on the board as determined by the roll.
        The player position will reset to 0 after reaching space 24. If the player account balance is 0,
        the function will return immediately. If the player lands or passes go (space 0) they will receive
        the set amount of go money. If the player lands on a property owned by another player, they will
        pay the required rent and the rent is deposited into the other player's balance. If the paying player
        does not have enough money to pay the player they will pay their remaining balance until they have a
        balance of 0. They have lost the game and are removed as an owner from any space.
        :param player_name: name of the player who is moving places (string)
        :param roll: the number of spaces the player is moved
        """
        player = self._players[player_name]
        if player.get_balance() == 0:       # if player balance 0, they can't play anymore.
            return

        current_space = self.get_player_current_space(player_name)
        current_space.clear_player(player)      # remove player from the old space


        initial_pos = self.get_player_current_position(player_name)
        set_position = initial_pos + roll

        if set_position > 24:      # if player passes go, reset position and add go money to their balance
            set_position = set_position - 25
            player.receive(self._go_money)

        player.set_position(set_position) # new position = old position + roll
        new_space = self.get_player_current_space(player_name)
        new_space.add_player(player)            # Move player to the new space

        # if the space is owned pay rent or remaining balance
        if new_space.get_owner() != player and new_space.get_owner() != None:
            rent = new_space.get_rent()
            balance = player.get_balance()
            owner = new_space.get_owner()
            if rent > balance:      # Player has lost all their money and will retire all properties.
                player.pay(balance)
                owner.receive(balance)
                player.clear_spaces()
                for key, space in self._spaces.items():  # If space owned by player, remove player from ownership
                    if space.get_owner() == player:
                        space.clear_owner()
            else:   # otherwise the player pays the rent to the owning player
                print(f"paid ${rent} in rent to {owner.get_name()}")
                player.pay(rent)
                owner.receive(rent)

    def show_board(self):
        """Prints a representation of the board."""
        for key, value in self._players.items():
            print(f"{key} balance: {value.get_balance()}")
        for key, value in self._spaces.items():
            print(f"{key} {value.get_players()}")
            if value.get_owner() != None:
                print(f"Owned by: {value.get_owner().get_name()}")

    def check_game_over(self):
        """Checks to see if the game is over by checking to see if all players
        except one have a balance of 0. If the game is over, returns the winning players name (player
        who still has a balance remaining). Otherwise it returns an empty string.
        :return name: The name of the winning player
        :return "": Empty string--if there is no winner
        """
        balances = [(key, value.get_balance()) for key, value in self._players.items() if
                    value.get_balance() > 0]  # list of all player balances greater than 0
        # if only one player has a positive balance, return player (winner) name
        if len(balances) == 1:
            return balances[0][0]
        else:
            return ""     #otherwise return an empty string

#
#
#
# def main():
#     game = RealEstateGame()
#     rents = [10, 5, 10, 20, 100, 5, 5, 20, 15, 10, 10, 10, 5, 5, 5, 5, 5, 10, 20, 20, 20, 20, 20, 20]
#     game.create_spaces(50, rents)
#     game.create_player("Joe", 146)
#     game.create_player("Joe", 5000)
#     game.create_player("Sally", 1000)
#     game.create_player("Billy", 50)
#     game.move_player("Billy", 4)
#     game.get_player_current_position("Joe")
#     game.move_player("Joe", 4)
#     game.buy_space("Joe")
#     game.buy_space("Billy")
#     game.move_player("Sally", 23)
#     game.buy_space("Sally")
#     game.move_player("Joe", 10)
#     game.buy_space("Joe")
#     game.move_player("Joe", 9)
#     game.move_player("Sally", 10)
#     game.move_player("Billy", 19)
#     game.move_player("Billy", 5)
#     game.buy_space("Billy")
#     game.move_player("Joe", 5)
#     game.move_player("Joe", 20)
#     game.move_player("Joe", 5)
#     game.move_player("Sally", 22)
#     game.buy_space("Sally")
#     game.move_player("Joe", 2)
#     game.move_player("Joe", 2)
#     game.move_player("Billy", 2)
#     game.show_board()
#     print(game.check_game_over())
#     print(game._players["Billy"].get_owned_spaces())
#
#
# if __name__ == "__main__":
#     main()
