#importing Card class in Deck class for geerating cards.
from card import Card
import random

class Deck:

    def __init__(self, start_value, end_value, no_of_suit):
        self.list1 = []
        self.start_value = start_value
        self.end_value = end_value
        self.no_of_suit = no_of_suit
        self.deck = []

        # Below code generates 52 cards with 4 suits and adds it into Deck.
        suits = ['C','D','H','S']
        ranks = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
        if start_value == 1 and end_value == 13 and no_of_suit ==4:
            for j in suits:
                for i in ranks:
                    self.deck.append(str(Card(i, j)))
        else:
            for j in range(self.no_of_suit):
                for i in range(self.start_value, self.end_value):
                    self.deck.append(str(Card(i, j)))


        self.shuffled_cards()
        self.draw_card()

    def __str__(self):
        string_name = ""
        for items in self.deck:
            string_name = string_name + " " + str(items)
        return string_name

    # Draw card method that returns a deck of 52 cards
    def shuffled_cards(self):
        random.shuffle(self.deck)


    # Draw card method that returns a deck of 52 cards
    def draw_card(self):
        return self.deck


def main():

    d = Deck(1, 13, 4)
    print(d.deck)

if __name__ == '__main__':
    main()


