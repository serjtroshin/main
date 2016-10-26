# -*- coding: utf-8 -*-

import numpy as np

class Modulo3Incrementer:
    x = 0

    def __init__(self, x):
        self.x = x

    def __add__(self, a):
        return int((self.x + a) % 3)

    def __sub__(self, a):
        return int((self.x + 333 - a) % 3)

    def __iadd__(self, other):
        self.x = (self.x + other) % 3
        return self.x

    def __isub__(self, other):
        self.x = (self.x + 333 - other) % 3

    def __int__(self):
        return self.x

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
        self.deck = list(map(lambda x: Card(x), hand))

    def __str__(self):
        return ' '.join(map(str, sorted(self.deck)))

    def __getitem__(self, key):
        return self.deck[key]


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

    def GetBarg(self, shedule, leftDeccision, rightDeccision):
        xx = shedule.GetFreeList()
        # print(''.join(xx[0]))
        if any(xx):
            return ("Game", xx[0])
        else:
            return "Pass"

    def Get(self, id):
        card = self.deck[id]
        self.deck = self.deck[:id] + self.deck[id+1:]
        return card

    # self.table, playerleft.get_hand(), playerright.get_hand()
    def get_card(self, table, lefthand, righthand):
        return self.Get(0)

    def get_hand(self):
        return self.deck




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

    def __init__(self, typeOfAction): #define ПАС/ ВИСТ
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

# class Rate(Card):


class Shedule:
    def __init__(self):
        self.masks = ['6', '7', '8', '9', '10']
        self.masks1 = ['♠', '♣', '♦', '♥', 'БК']
        self.alls = [(i, j) for i in self.masks for j in self.masks1]
        self.used = {i: False for i in self.alls}


    def GetIdMask1(self, c):
        for i in enumerate(self.masks1):
            if i[1] == c:
                return i[0]
        return False

    @staticmethod
    def cmp(a, b):
        x1 = Shedule.GetIdMask1(Shedule(), a[1])
        x2 = Shedule.GetIdMask1(Shedule(), b[1])
        return int(a[0]) * 100 + x1 - int(b[0]) * 100 - x2

    def SetUsed(self, cnt, typeX):
        card = (cnt, typeX)
        ans = list(filter(lambda x: self.used[x] == False, self.used.keys()))
        ans = list(sorted(ans, cmp=self.cmp))
        for i in range(len(ans)):
            if ans[i] == card:
                for j in range(i + 1):
                    self.used[ans[j]] = True

    def IsUsed(self, cnt, typeX):
        return self.used[(cnt, typeX)]

    def GetFreeList(self):
        ans = list(filter(lambda x: self.used[x] == False, self.used.keys()))
        ans = list(sorted(ans, cmp=self.cmp))
        # print(' '.join(map(lambda x: str(x[0])+str(x[1]), ans)))
        return ans

    def __str__(self):
        return "Locked: " + ' '.join(map(str, filter(lambda x: self.used[x] == True, self.used.keys())))



class Round:
    typeOfRound = -1
    table = []
    players = -1
    manager_id = -1
    allCards = np.arange(32)  # crea

    def MakeOneCircle(self, manager_id, players, trump='♠', amount_cnt=6):
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
        for i in range(3):
            ans = players[(manager_id + 0) % 3].GetBarg(shedule, answers[(manager_id + 3 - 1) % 3], answers[(manager_id + 1) % 3])
            answers[(manager_id + 0) % 3] = ans
            if AnswerType(ans).isPlay:
                shedule.SetUsed(ans[1][0], ans[1][1])
            elif AnswerType(ans).isMiser:
                shedule.SetUsed('8', 'БК')
            manager_id += 1
        # print(' '.join(map(lambda x: str(x[0])+str(x[1]), answers)))
        # первый круг голосов пройден
        while True: # пока есть свободные ячейки в таблице
            if len(list(filter(lambda x: AnswerType(x).isPass is True, answers))) == 2: # если хотя бы два не играют
                break

            ans = players[(manager_id + 0) % 3].GetBarg(shedule, answers[(manager_id + 3 - 1) % 3],
                                                        answers[(manager_id + 1) % 3])
            answers[(manager_id + 0) % 3] = ans
            print(ans)
            if AnswerType(ans).isPlay:
                shedule.SetUsed(ans[1][0], ans[1][1])
            elif AnswerType(ans).isMiser:
                shedule.SetUsed('8', 'БК')
            manager_id += 1 # modulo 3

        return answers


    def __str__(self):
        return 'Player {0}: {1}, \nPlayer {2}: {3}, \nPlayer {4}: {5}, TALON: {6}\n'.format(self.players[0].name,
                                                                                          ' '.join(map(str, self.players[0].deck)),
                                                                                          self.players[1].name,
                                                                                          ' '.join(map(str,
                                                                                                       self.players[
                                                                                                           1].deck)),
                                                                                          self.players[2].name,
                                                                                          ' '.join(map(str,
                                                                                                       self.players[
                                                                                                           2].deck)),
                                                                                          self.talon)


class Game:
    players = []
    maxBullet = 20

    def __init__(self, name1="Trus", name2="Balbes", name3="Bivaliy"):
        self.players.append(Player(name1, 0))
        self.players.append(Player(name2, 1))
        self.players.append(Player(name3, 2))
        self.manager = 0
        r = Round(self.players, self.manager)
        self.answers = r.MakeBargs(self.players, self.manager)
        print(self.answers)
        print(' '.join(map(lambda x: AnswerType(x).Tostr(x), self.answers)))
        notPass = ()
        for i in self.answers:
            if not AnswerType(i).isPass:
                notPass = i
        if notPass == '':
            print("RASPASI!!!)!)!)!)!)!)!))!)!)!)!)!)!)!)!)")
        elif AnswerType(notPass).isMiser:
            print("MIZER TIMEEEOJOJOSNDVOJDNVIOJSNFOEJFNEOJN")
        else:
            while any(self.players[0].deck):
                self.manager = r.MakeOneCircle(self.manager, self.players, notPass[1][1], int(notPass[1][0]))
                print(r)

        #while any(filter(lambda x: x.bullet < self.maxBullet, self.players)):
        #    r = Round(self.players, self.manager)
        #    print(r)
        #    print


g = Game()
