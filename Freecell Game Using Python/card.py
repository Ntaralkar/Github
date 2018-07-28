class Card:

    # Initialization of suit and face in card class
    def __init__(self, suit, face):
        self.suit = suit
        self.face = face

    def __str__(self):
        return str(self.face) + str(self.suit)

    def getSuit(self):
        return self.suit

    def getFace(self):
        return self.face


def main():
    c = Card('S', 1)


if __name__ == '__main__':
    main()

