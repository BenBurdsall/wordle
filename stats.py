class stats:

    def __init__(self):
        self.stratScores = {}

    def registerStrategy(self,label):
        # tripple is [games-played, solved in guessses, not solved within 5]
        self.stratScores[label]=(0,0,0)

    # Records a single game result for a given strategy. Solved is a boolean, guesses is the number of guesses if it was solved within 5
    def addGameResult(self,strategy, solved, guesses):
        played, totalguess, failedcount = self.stratScores[strategy]
        if guesses > 5:
            raise Exception(f"Too many guesses enteredd {guesses}")

        played +=1
        if not solved:
            failedcount +=1
        else:
            totalguess += guesses
        self.stratScores[strategy] = (played,totalguess,failedcount)

    # Returns the [average amount of guesses, percentage games won]
    def getStatFor(self,strategy):
        played, totalguess, failedcount = self.stratScores[strategy]

        solved = played-failedcount
        averageGuess = totalguess / solved
        percentagePass = 100 * solved / played
        return averageGuess,percentagePass


    def __str__(self):
        message = "---------Scores on the doors--------------\n"
        for strat in self.stratScores:
            avg , pp = self.getStatFor(strat)
            message += f"strategy {strat}......... Average Guess Count {avg}, Percentage of games won {pp} \n"

        return message