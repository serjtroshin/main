# -*- coding: utf-8 -*-

import numpy as np

class Modulo3Incrementer:
    def __init__(self, x):
        self.x = x
    def __add__(self, a):
        return (self.x + a) % 3
    def __dir__(self, a):
        return (self.x + 333 - a) % 3

class Card:
    @classmethod
    def CardsAmount(arg):
        return 32

    def __init__(self, id, istrump=False):
        self.suit = id % 4
        self.rating = id / 4

    def __lt__(self, other):
        return (self.suit + 1) * 100 + self.rating < (other.suit + 1) * 100 + other.rating

    def __str__(self):
        val = ''
        if self.rating == 0:
            val = '7'
        elif self.rating == 1:
            val = '8'
        elif self.rating == 2:
            val = '9'
        elif self.rating == 3:
            val = '10'
        elif self.rating == 4:
            val = 'J'
        elif self.rating == 5:
            val = 'Q'
        elif self.rating == 6:
            val = 'K'
        elif self.rating == 7:
            val = 'A'
        suit = 0
        if self.suit == 0:
            suit = '♠'
        elif self.suit == 1:
            suit = '♣'
        elif self.suit == 2:
            suit = '♦'
        elif self.suit == 3:
            suit = '♥'
        return val + suit


class Hand:
    def __init__(self, hand):
        self.deck = map(lambda x: Card(x), hand)

    def __str__(self):
        return ' '.join(map(str, sorted(self.deck)))


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

    def IncTricksAmount(self):
        self.tricks_amount += 1

    def updateDeck(self, deck):
        self.deck = deck

    def __str__(self):
        return 'name=' + str(self.name) + ' id=' + str(self.id) + ' deck:' + str(self.deck)

    def GetDeccisionOnBarg(self, leftDeccision, rightDeccision, sheduleFreeList):
        return sheduleFreeList[0]



class AnswerType: # данный класс - это ответ игрока при торгах
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

    def __init__(self, typeOfAction, card=(-1, -1)): #define ПАС/ ВИСТ
        if typeOfAction == AnswerType.Action.Mizer:
            self.isMizer = True
        elif typeOfAction == AnswerType.Action.Game:
            self.isPlay = True
            self.PlayChoose = card
        elif typeOfAction == AnswerType.Action.Vist:
            self.isVist = True
        elif typeOfAction == AnswerType.Action.Pass:
            self.isPass = True


# class Rate(Card):


class Shedule:
    def __init__(self):
        masks = ['7', '8', '9', '10']
        masks1 = ['♠', '♣', '♦', '♥', 'БК']
        self.alls = [(i, j) for i in masks for j in masks1]
        self.used = {i: False for i in self.alls}

    def SetUsed(self, cnt, typeX):
        card = (cnt, typeX)
        for i in range(len(self.alls)):
            if self.alls[i] == card:
                print("YES")
                for j in range(i + 1):
                    self.used[self.alls[j]] = True

    def IsUsed(self, cnt, typeX):
        return self.used[(cnt, typeX)]

    def GetFreeList(self):
        return list(filter(lambda x: self.used[x] == False, self.used.keys()))

    def __str__(self):
        return "Locked: " + ' '.join(map(str, filter(lambda x: self.used[x] == True, self.used.keys())))



class Round:
    typeOfRound = -1
    table = []
    players = -1
    manager_id = -1
    allCards = np.arange(32)  # crea

    def MakeOneCircle(self, manager_id, players, trump):
        tripleset = []
        for manager in range(3):
            id_man = (manager + manager_id) % 3
            player = players[id_man]
            playerleft = players[(id_man + 3 - 1) % 3]
            playerright = players[(id_man + 3 + 1) % 3]
            card = player.get_card(self.table, playerleft.get_hand(), playerright.get_hand())  # самое главное - сделать ход
            tripleset.append((card, id_man))
            self.table = tripleset
        tripleset = list(sorted(tripleset, key=lambda x: x[0], reverse=True))
        winner_id = tripleset[0][1]
        players[winner_id].IncTricksAmount()
        return winner_id

    def __init__(self, players, manager_id):
        self.table = []
        self.players = players
        self.manager_id = manager_id
        self.allCards = np.arange(32)  # creating a deck
        np.random.shuffle(self.allCards)
        xDecks = (Hand(self.allCards[:10]), Hand(self.allCards[10:20]), Hand(self.allCards[20:30]))
        self.talon = Hand(self.allCards[30:])
        for P, D in zip(self.players, xDecks):
            P.updateDeck(D)

    def MakeBargs(self, players, manager_id):
        manager_id = Modulo3Incrementer(manager_id)
        shedule = Shedule()
        freeList = shedule.GetFreeList()
        answers = [-1, -1, -1]
        # первый круг голосов - возможны распасы


        while any(shedule.GetFreeList()): # пока есть свободные ячейки в таблице
            if all(filter(lambda x: isinstance(x, AnswerType) == True, answers)):
                if len(list(filter(lambda x: x.isPass == True, answers))) == 2: # если хотя бы два не играют
                    break

            manager_id += 1 # modulo 3
            player



    def __str__(self):
        return 'Player {0}: {1}, \nPlayer {2}: {3}, \nPlayer {4}: {5}, TALON: {6}'.format(self.players[0].name,
                                                                                          self.players[0].deck,
                                                                                          self.players[1].name,
                                                                                          self.players[1].deck,
                                                                                          self.players[2].name,
                                                                                          self.players[2].deck,
                                                                                          self.talon)


class Game:
    players = []
    maxBullet = 20

    def __init__(self, name1="Trus", name2="Balbes", name3="Bivaliy"):
        self.players.append(Player(name1, 0))
        self.players.append(Player(name2, 1))
        self.players.append(Player(name3, 2))
        self.manager = 0
        #while any(filter(lambda x: x.bullet < self.maxBullet, self.players)):
        #    r = Round(self.players, self.manager)
        #    print(r)
        #    print


d = Shedule()
print(d)
d.SetUsed('8', '♠')
print(d)