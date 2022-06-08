# contains a frequency counter for how many times a letter in a specified position [1..5] appears
class tupleCount:

   # intiates the counter at 1 for a given letter and position
   def __init__(self, letter,position,count=1):
      self.letter=letter
      self.position = position
      self.count = count

   def __str__(self):
      return f"{self.letter},slot={self.position},freq={self.count}"