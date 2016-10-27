class Bullet:
    MIZER_CONST = 10
    whistCosts = {6:2, 7:4, 8:6, 9:8, 10:10}
    needWhist = {6:4, 7:2, 8:1, 9:1, 10:0}
    def __init__(self, persons):
        self.persons = persons

    def Paste(self):
        for p in self.persons:
            print p.name, " BULLET:", p.bullet, "  MOUNTAIN:", p.mountain, "  Whists:", p.whist
        print

    def HalfAWhist(self, id, gamecost):
        self.persons[id].whist += self.needWhist[gamecost] / 2 * self.whistCosts[gamecost]

    def Update3Player(self, gameType, rezults, isWhist=(0, 0, 0), whistcnt=0, manager_id=0, pass_CONST=1, bribesNeed=6, is_out_of_three=False):
        if gameType == "Mizer":
            self.persons[manager_id].mountain += rezults[manager_id] * self.MIZER_CONST

        elif gameType == "Pass":
            for i in range(3):
                self.persons[i].mountain += rezults[i] * pass_CONST

        elif gameType == "Game":
            r = rezults[manager_id]
            # The shortfall in playing
            if r < bribesNeed:
                delta = bribesNeed - r # The shortfall in playing
                self.persons[manager_id].mountain += delta * self.whistCosts[bribesNeed]
                if whistcnt == 1:
                    # summ of whist - all for only whistmaker
                    for i in range(3):
                        if i != manager_id:
                            self.persons[i].whist += (sum(rezults) + delta) * isWhist[i] * self.whistCosts[bribesNeed]
                else:
                    # (each earn what he has + delta of shortfall) * whistCast
                    for i in range(3):
                        if i != manager_id:
                            self.persons[i].whist += (rezults[i] + delta) * isWhist[i] * self.whistCosts[bribesNeed]
            # now if no shortfall
            else:
                indeces = {0, 1, 2} - {manager_id}
                p1, p2 = list(indeces)
                penalities = [0, 0, 0]


                if whistcnt == 2:
                    need = int(self.needWhist[bribesNeed]*1.0 / 2 + 0.5001) # like a half -_-
                else:
                    need = self.needWhist[bribesNeed]
                for i in [p1, p2]:
                    self.persons[i].mountain += max(0, need - rezults[i]) * self.whistCosts[bribesNeed]
                    self.persons[i].whist += rezults[i] * self.whistCosts[bribesNeed]
                self.persons[manager_id].bullet += self.whistCosts[bribesNeed]





class Player:
    tricks_amount = 0
    deck = []
    name = ''
    id = 0

    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.bullet = 0
        self.mountain = 0
        self.whist = 0
class AnswerType:
    isPass = False
    isWhist = False
    isPlay = False
    isMiser = False
    PlayChoose = (-1, -1)

    class Action:
        @staticmethod
        def Mizer():
            return "Mizer"

        @staticmethod
        def Pass():
            return "Pass"

        @staticmethod
        def Vist():
            return "Vist"

        @staticmethod
        def Game():
            return "Game"

    def __init__(self, typeOfAction):
        if typeOfAction == AnswerType.Action.Mizer():
            self.isMizer = True
        elif type(typeOfAction) is tuple:
            self.isPlay = True
            self.PlayChoose = typeOfAction[1]
        elif typeOfAction == AnswerType.Action.Vist():
            self.isVist = True
        elif typeOfAction == AnswerType.Action.Pass():
            self.isPass = True

    def Tostr(self, y):
        x = AnswerType(y)
        if x.isPlay:
            return y[1][0] + y[1][1]
        else:
            return y
b = Bullet((Player("Misha", 0), Player("Sasha", 1), Player("Tolya", 2)))
b.Paste()
b.Update3Player("Mizer", (2, 2, 6), isWhist=(1, 1, 0), whistcnt=2, manager_id=2, bribesNeed=7)
b.Paste()