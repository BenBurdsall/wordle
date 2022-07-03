import logging


class slot:

    def __init__(self, position):
        self.logger = logging.getLogger(__name__)
        self.currentLetter = None
        self.fixed = False
        self.cannotContainer = []
        self.position = position

    def clone(self):
        cl = slot()
        cl.currentLetter = self.currentLetter
        cl.fixed  =self.fixed
        cl.cannotContainer = self.cannotContainer.copy()
        cl.position = self.position
        return cl

    def assignLetter(self,letter):
        if self.fixed and not letter == self.currentLetter:
            raise Exception(f"You are trying to assign a DIFFERENT letter {letter} to a slot {self.position} that is already fixed to {self.currentLetter} ")

        if letter in self.cannotContainer:
            raise Exception

        self.currentLetter = letter

     # used to indicate that the current letter cannot be in this slot position. It may or may not be in another position
    def wrongLetter(self):

        if self.fixed:
            raise Exception(
                f"The letter for slot {self.position} has already been fixed as {self.currentLetter}- cannot set it as being wrong")

        if self.currentLetter not in self.cannotContainer:
            self.cannotContainer.append(self.currentLetter)
    # used to fix the current letter as being correct for this slot.
    def correctLetter(self):
        if self.currentLetter is None:
            raise Exception("You cannot say a letter is correct when it has not yet been assigned")

        if self.currentLetter in self.cannotContainer:
            raise Exception(f"Slot {self.position} cannot be set as being correct with letter {self.currentLetter} as this letter has already been declared as incorrect")



        self.fixed = True
        self.logger.info(f" fixing slot {self.position} as the letter {self.currentLetter}")
