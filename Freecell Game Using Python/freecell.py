# importing deck class to add functionalities in order to play the game.
from deckk import Deck

"""  ****************** RULES *************************************

1.1 The Rules
The game follows the following rules:
 Only one card may be moved at a time.
 The four foundations must be built starting from the Ace of the appropriate suit, followed by the 2, then the 3 etc. until the King is placed.
 If a card is placed on a cascade, it must be placed of a card of the opposite colour, and of a suit that is one higher than itself. E.g. a red 2 can be placed on a black 3, but not a black 4.
 Any card may be placed in an empty cascade.
 Cards from the foundations may be placed back onto a cascade, or an empty cascade slot.
 Only one card at a time can occupy a cell slot.
Victory is achieved when all four foundations are lled with their respective suits from Ace to King.

"""






class Freecell:

    def __init__(self):
        self.cascade1 = []
        self.cascade2 = []
        self.cascade3 = []
        self.cascade4 = []
        self.cascade5 = []
        self.cascade6 = []
        self.cascade7 = []
        self.cascade8 = []
        self.openCellList = [[], [], [], []]
        self.num = 0
        self.count = 0
        self.foundation_cell = [[], [], [], []]
        d = Deck(1, 13, 4)
        self.stackOfStack = [[]] * 8
        x = d.draw_card()


        # populate 4 list with 6 cards in each and 4 list with 7 cards in each to form a complete cascade.
        for i in range(6):
            y = x.pop(-1)
            self.cascade1.append(y)

        for i in range(6):
            y = x.pop(-1)
            self.cascade2.append(y)

        for i in range(6):
            y = x.pop(-1)
            self.cascade3.append(y)

        for i in range(6):
            y = x.pop(-1)
            self.cascade4.append(y)

        for i in range(7):
            y = x.pop(-1)
            self.cascade5.append(y)

        for i in range(7):
            y = x.pop(-1)
            self.cascade6.append(y)


        for i in range(7):
            y = x.pop(-1)
            self.cascade7.append(y)


        for i in range(7):
            y = x.pop(-1)
            self.cascade8.append(y)

        # Generating a List of List

        self.stackOfStack[0] = self.cascade1
        self.stackOfStack[1] = self.cascade2
        self.stackOfStack[2] = self.cascade3
        self.stackOfStack[3] = self.cascade4
        self.stackOfStack[4] = self.cascade5
        self.stackOfStack[5] = self.cascade6
        self.stackOfStack[6] = self.cascade7
        self.stackOfStack[7] = self.cascade8


        self.gameFreecell()

    # A Function to move a card from one list to another list in a cascade.

    def moveTostack(self, source, target):
        self.source_stack = ''


        if self.num == 1:
            self.source_stack = self.stackOfStack[source]

        if self.num == 4:
            self.source_stack = self.stackOfStack[source]

        if self.num == 5:
            self.source_stack = self.openCellList[source]

        if self.num == 6:
            self.source_stack = self.foundation_cell[source]

        target_stack = self.stackOfStack[target]

        # This part of the code takes last card into  s variable and convert it into string
        s = str(self.source_stack[-1])
        t = str(target_stack[-1])

        # slicing of string to get rank and suit value of a card for comparison
        a = int(s[1:3])
        c = int(t[1:3])


        if s.__contains__('S') or s.__contains__('C'):
            if t.__contains__('H') or t.__contains__('D'):
                if c - 1 == a:
                    x = self.source_stack.pop()
                    print(x)
                    target_stack.append(x)
                else:
                    print("cannot move the Card, Please check face value of card 1")  # opposite suit color card but rank doesnt match
            else:
                print("Invalid move ! , cannot move a card on same suit")  # same suit  different rank


        elif s.__contains__('H') or s.__contains__('D'):
            if t.__contains__('S') or t.__contains__('C'):
                if c - 1 == a:
                    x = self.source_stack.pop()
                    target_stack.append(x)
                else:
                    print("cannot move the Card, Please check face value of card")
            else:
                print("Invalid move !! , cannot move a card on same suit")

        elif len(target_stack) == 0:
            x = self.source_stack.pop()
            target_stack.append(x)
        else:
            print("Cannot move a card on same suit")

    # Below Function is to move a Card to Open Cell from Cascade

    def moveToOpenCell(self, source, target):

        # gets the cascade list from where cards needs to be moved to Open cell
        s1 = self.stackOfStack[source]
        x = s1.pop()

        if len(self.openCellList[target]) == 0:
            self.openCellList[target].append(x)
            return self.openCellList
        else:
            print("Opencell is not empty")

    # Below Function is to move a card from Open cell Foundation and Cascade.

    def moveFromOpenCell(self, source, target):

        # This part of the code calls another function to move a card to Cascade and to move a card to Foundation

        if self.num == 4:
            self.moveToFoundation(source, target)
        if self.num == 5:
            self.moveTostack(source, target)

    # Beow Function is to move a card to Foundation from Cascade and Open Cell.

    def moveToFoundation(self, source, target):

        source_last_card = ''
        source_stack = []

        if self.num == 3:
            source_stack = self.stackOfStack[source]
            source_last_card = str(source_stack[-1])

        if self.num == 4:
            self.moveToOpenCell(source, target)
            source_stack = self.openCellList[source]
            source_last_card = str(source_stack[-1])

        source_int_value = int(source_last_card[1:3])

        if source_last_card.__contains__('S') and target == 0:
            if len(self.foundation_cell[target]) == 0:
                if source_int_value == 1:
                    x = source_stack.pop()
                    self.foundation_cell[target].append(x)
                else:
                    print("Invalid move, Card can only move on top of Ace of Spade")
            else:
                # Card validation for all Spade cards except Ace of Spade
                target_stack = self.foundation_cell[target]
                target_last_card = str(target_stack[-1])
                target_int_value = int(target_last_card[1:3])
                print(target_int_value)
                if source_int_value - 1 == target_int_value:
                    x = source_stack.pop()
                    self.foundation_cell[target].append(x)
                else:
                    print("Invalid move, Please check the face value of card")

        # Card Validation for Ace of Heart Card.
        elif source_last_card.__contains__('H') and target == 1:
            if len(self.foundation_cell[target]) == 0:
                if source_int_value == 1:
                    x = source_stack.pop()
                    self.foundation_cell[target].append(x)
                else:
                    print("Invalid move, Card can only move on top of Ace of Heart")
            else:
                # Card validation for all Heart cards except Ace of Heart card.
                target_stack = self.foundation_cell[target]
                target_last_card = str(target_stack[-1])
                target_int_value = int(target_last_card[1:3])
                if source_int_value - 1 == target_int_value:
                    x = source_stack.pop()
                    self.foundation_cell[target].append(x)
                else:
                    print("Invalid move, Please check the face value of card")

        # Card validation for Ace of club card

        elif source_last_card.__contains__('C') and target == 2:
            if len(self.foundation_cell[target]) == 0:
                if source_int_value == 1:
                    x = source_stack.pop()
                    self.foundation_cell[target].append(x)
                else:
                    print("Invalid move, Card can only move on top of Ace of Club")
            else:
                # Card validation for all club cards except Ace of club
                target_stack = self.foundation_cell[target]
                target_last_card = str(target_stack[-1])
                target_int_value = int(target_last_card[1:3])
                if source_int_value - 1 == target_int_value:
                    x = source_stack.pop()
                    self.foundation_cell[target].append(x)
                else:
                    print("Invalid move, Please check the face value of card")

        # Card validation for Ace of Diamond
        elif source_last_card.__contains__('D') and target == 3:
            if len(self.foundation_cell[target]) == 0:
                if source_int_value == 1:
                    x = source_stack.pop()
                    self.foundation_cell[target].append(x)
                else:
                    print("Invalid move, Card can only move on top of Ace of Diamond")
            else:
                # Card validation for all Daimond cards except Ace of Diamond card.
                target_stack = self.foundation_cell[target]
                target_last_card = str(target_stack[-1])
                target_int_value = int(target_last_card[1:3])
                if source_int_value - 1 == target_int_value:
                    x = source_stack.pop()
                    self.foundation_cell[target].append(x)
                else:
                    print("Invalid move, Please check the face value of card")

        else:
            print(
                "Spade can move to 1st cell,\n Heart can move to 2nd cell,\n Club can move to 3rd cell \n and Diamond can move to 4th cell ")

        # Winning condition, if Foundation cell has 52 cards than the player wins.
        if len(self.foundation_cell) == 52:
            print("Congratulations, You WIN !!!")
            print("Number of moves : ", count)
        return self.foundation_cell

    # Below function is used to call all other functions in a while loop to play the FreeCell game.
    def gameFreecell(self):

        i = 0

        while i < 5:

            self.count = self.count + 1
            options = "1 : Move from one Cascade to another Cascade \n2 : Move from Cascade to OpenCell\n3 : Move from Cascade to Foundation\n"
            options = options + "" + "4 : Move from Opencell to Foundation\n"
            options = options + "" + "5 : Move from OpenCell to Cascade\n6 : Move from foundation to Cascade\n7 : Exit"

            self.FaceCheck(self.stackOfStack[0])
            self.FaceCheck(self.stackOfStack[1])
            self.FaceCheck(self.stackOfStack[2])
            self.FaceCheck(self.stackOfStack[3])
            self.FaceCheck(self.stackOfStack[4])
            self.FaceCheck(self.stackOfStack[5])
            self.FaceCheck(self.stackOfStack[6])
            self.FaceCheck(self.stackOfStack[7])
            print()
            print("Foundation cell : ")
            self.FaceCheck(self.foundation_cell[0])
            self.FaceCheck(self.foundation_cell[1])
            self.FaceCheck(self.foundation_cell[2])
            self.FaceCheck(self.foundation_cell[3])
            print()
            print("Open Cell : ")
            self.FaceCheck(self.openCellList[0])
            self.FaceCheck(self.openCellList[1])
            self.FaceCheck(self.openCellList[2])
            self.FaceCheck(self.openCellList[3])

            print(options)

            # Get the input from user for playing FreeCell game

            self.num = int(input("Enter your choice"))
            # source = int(input("Enter the source cascade number from where you want to move the card"))

            if self.num == 1:
                source = int(input("Enter the source cascade number from where you want to move the card : "))
                target = int(input("Enter the target location where you want to move the card : "))
                self.moveTostack(source, target)


            elif self.num == 2:
                source = int(input("Enter the source cascade number from where you want to move the card : "))
                target = int(input("Enter the Opencell location where you want to move the card : "))
                self.moveToOpenCell(source, target)

            elif self.num == 3:
                source = int(input("Enter the source cascade number from where you want to move the card : "))
                target = int(input("Enter the Foundation location where you want to move the card : "))
                self.moveToFoundation(source, target)



            elif self.num == 4:
                source = int(input("Enter the OpenCell location from where you want to move the card : "))
                target = int(input("Enter the target location where you want to move the card : "))
                self.moveFromOpenCell(source, target)



            elif self.num == 5:
                source = int(input("Enter the OpenCell location from where you want to move the card : "))
                target = int(input("Enter the Cascade location where you want to move the card : "))
                self.moveFromOpenCell(source, target)

            elif self.num == 6:
                source = int(input("Enter the Foundation cell location from where you want to move the card : "))
                target = int(input("Enter the Cascade location where you want to move the card : "))
                self.moveTostack(source, target)

            elif self.num == 7:
                print("Thank You for playing FREECELL game !!")
                print("Number of moves : ", count)
                break

            else:
                print("Invalid choice")


    # The function is used to display card face values in their original format
    # For eg. for S11 = SJ , S12 = SQ and S13 = SK


    def FaceCheck(self, list2):
        n = len(list2)
        self.list1 = []
        for i in range(0, n):
            x = list2[i]
            first_digit = x[0:1]
            last_digits = x[1:3]
            if last_digits == '1':
                x = first_digit + 'A'
            if last_digits == '11':
                x = first_digit + 'J'
            if last_digits == '12':
                x = first_digit + 'Q'
            if last_digits == '13':
                x = first_digit + 'K'
            self.list1.append(x)
        print(self.list1)


def main():
    f = Freecell()

if __name__ == '__main__':
    main()