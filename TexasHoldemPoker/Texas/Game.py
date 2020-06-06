from tkinter import *
from tkinter import font
from winsound import *
from Card import *
from Player import *
import random

class MainGame:
    def setupButton(self):
        self.Check = Button(self.window, text = "Check", width = 6, height = 1, font = self.fontstyle2, command = self.pressedCheck)
        self.Check.place(x = 50, y= 500)
        self.Betx1 = Button(self.window, text = "Bet x1", width = 6, height = 1, font = self.fontstyle2, command = self.pressedBetx1)
        self.Betx1.place(x = 150, y = 500)
        self.Betx2 = Button(self.window, text="Bet x2", width=6, height=1, font=self.fontstyle2,command=self.pressedBetx2)
        self.Betx2.place(x=250, y=500)

        self.Deal = Button(self.window, text="Deal", width=6, height=1, font=self.fontstyle2,command=self.pressedDeal)
        self.Deal.place(x=600, y=500)
        self.Again = Button(self.window, text="Again", width=6, height=1, font=self.fontstyle2, command=self.pressedAgain)
        self.Again.place(x=700, y=500)

        self.Deal['state'] = 'disabled'
        self.Deal['bg'] = 'gray'

        self.Again['state'] = 'disabled'
        self.Again['bg'] = 'gray'

    def setupLabel(self):
        self.LbetMoney = Label(text = "&10", width=4, height = 1, font = self.fontstyle,bg = "dark green", fg = "cyan")
        self.LbetMoney.place(x=250, y=450)
        self.LPlayertMoney = Label(text="You have &990", width=15, height=1, font=self.fontstyle, bg="dark green", fg="cyan")
        self.LPlayertMoney.place(x=500, y=450)

        self.LstatusPlayer=Label(text= "", width = 15, height = 1, font = self.fontstyle, bg = "dark green", fg = "yellow")
        self.LstatusPlayer.place(x = 250, y = 380)
        self.LstatusDealer=Label(text="", width = 15, height = 1, font = self.fontstyle, bg = "dark green", fg = "yellow")
        self.LstatusDealer.place(x= 250, y= 80)
        self.Lwinner = Label(text = "", width=6, height = 1, font = self.fontstyle,bg = "dark green", fg = "red")
        self.Lwinner.place(x = 500, y = 380)

    def pressedCheck(self):
        PlaySound('sounds/ding.wav', SND_FILENAME)

        #뒤집힌 카드 다시그리기
        p = PhotoImage(file = "cards/" + self.dealer.cards[0].filename())
        self.LcardsDealer[0].configure(image = p)
        self.LcardsDealer[0].image = p

        p = PhotoImage(file = "cards/" + self.dealer.cards[1].filename())
        self.LcardsDealer[1].configure(image = p)
        self.LcardsDealer[1].image = p

        #비교
        for i in self.mastercards:
            self.player.addCard(i)
            self.dealer.addCard(i)

        self.playerscore = -1
        self.dealerscore = -1

        #원페어 - 같은 숫자 2장 최대 7
        self.checkOnepairPlayer()
        self.checkOnepairDealer()

        #투페어 - 같은 숫자 2장 + 같은 숫자 2장 최대 14
        self.checkTwopairPlayer()
        self.checkTwopairDealer()

        #트리플 - 같은 숫자가 3장 점수 15
        self.checkTriplePlayer()
        self.checkTripleDealer()

        #스트레이트 - 카드 5장 숫자가 연달아 20점
        self.checkStraightPlayer()
        self.checkStraightDealer()

        #백스트레이트 - A2345 30점
        self.checkBackStraightPlayer()
        self.checkBackStraightDealer()

        #마운틴 - 10 J Q K A  10 11 12 13 1  40점
        self.checkMountainPlayer()
        self.checkMountainDealer()

        #플러쉬 - 같은 무늬 5장 50점
        self.checkFlushPlayer()
        self.checkFlushDealer()

        #풀하우스 - 같은 숫자 3장 같은 숫자 2장 60점
        self.checkFullhousePlayer()
        self.checkFullhouseDealer()

        #포카드 - 같은 숫자 4장 70점
        self.checkFourcardPlayer()
        self.checkFourcardDealer()

        #스트레이트플러쉬 - 같은무늬 + 숫자 연달아 80점
        self.checkStraightFlushPlayer()
        self.checkStraightFlushDealer()

        #백 스트레이트 플러쉬 - 같은무늬 + A 2 3 4 5  90점
        self.checkBackStraightFlushPlayer()
        self.checkBackStraightFlushDealer()

        #로얄 스트레이트 플러쉬 - 같은무늬  10 J K Q K A 10 11 12 13 1 100점
        self.checkRoyalStraightFlushPlayer()
        self.checkRoyalStraightFlushDealer()

        #점수 계산후 글자 띄우기, 배팅된금액 * 2한것을 내 돈에 더하기
        self.LstatusPlayer.configure(text = str(self.statusPlayer))
        self.LstatusDealer.configure(text = str(self.statusDealer))

        if self.playerscore > self.dealerscore:#플레이어 승
            self.Lwinner.configure(text = "WIN")
            self.Lwinner.place(x = 500, y = 380)
            self.playerMoney += self.betMoney*2
            PlaySound('sounds/win.wav', SND_FILENAME)

        elif self.playerscore < self.dealerscore:#딜러승
            self.Lwinner.configure(text="WIN")
            self.Lwinner.place(x=500, y=80)
            PlaySound('sounds/wrong.wav', SND_FILENAME)

        else: #비김
            self.Lwinner.configure(text="DRAW")
            self.Lwinner.place(x=500, y=80)
            self.playerMoney += self.betMoney
            PlaySound('sounds/ding.wav', SND_FILENAME)

        self.betMoney = 0
        self.LbetMoney.configure(text="$" + str(self.betMoney))
        self.LPlayertMoney.configure(text = "You have &" + str(self.playerMoney))

        self.Deal['state'] = 'disabled'
        self.Deal['bg'] = 'gray'
        self.Again['state'] = 'active'
        self.Again['bg'] = 'white'

        self.Betx1['state'] = 'disabled'
        self.Betx1["bg"] = "gray"
        self.Betx2['state'] = 'disabled'
        self.Betx2["bg"] = "gray"
        self.Check['state'] = 'disabled'
        self.Check["bg"] = "gray"

    def checkOnepairPlayer(self):
        self.playerscore = 0
        tlist = []
        plist = []

        for i in range(self.player.inHand()):
            tlist.append(self.player.cards[i].getValue())
            plist.append(self.player.cards[i].getsuit())

        for j in range(self.player.inHand()):
            if tlist.count(tlist[j]) == 2:
               self.statusPlayer = "One Pair"
               value = tlist[j]
               for k in range(self.player.inHand()):
                   if value == tlist[k]:
                       if plist[k] == "Clubs":
                           self.playerscore += 1
                       elif plist[k] == "Spades":
                           self.playerscore += 4
                       elif plist[k] == "Hearts":
                           self.playerscore += 2
                       elif plist[k] == "Diamonds":
                           self.playerscore += 3
               return

    def checkOnepairDealer(self):
        self.dealerscore = 0
        tlist = []
        plist = []
        for i in range(self.dealer.inHand()):
            tlist.append(self.dealer.cards[i].getValue())
            plist.append(self.dealer.cards[i].getsuit())

        for j in range(self.dealer.inHand()):
            if tlist.count(tlist[j]) == 2:
                self.statusDealer = "One Pair"
                value = tlist[j]
                for k in range(self.dealer.inHand()):
                    if value == tlist[k]:
                        if plist[k] == "Clubs":
                            self.dealerscore += 1
                        elif plist[k] == "Spades":
                            self.dealerscore += 4
                        elif plist[k] == "Hearts":
                            self.dealerscore += 2
                        elif plist[k] == "Diamonds":
                            self.dealerscore += 3
                return

    def checkTwopairPlayer(self):
        tlist = []
        plist = []

        for i in range(self.player.inHand()):
            tlist.append(self.player.cards[i].getValue())
            plist.append(self.player.cards[i].getsuit())

        pair = 0
        playerscore = 0
        beforevalue = 0

        for j in range(self.player.inHand()):
            if pair == 2:
                self.playerscore = playerscore + 5
                self.statusPlayer = "Two Pair"
                return

            if tlist.count(tlist[j]) == 2:
                if beforevalue == tlist[j]:
                    continue

                pair += 1
                beforevalue = tlist[j]
                value = tlist[j]
                for k in range(self.player.inHand()):
                    if value == tlist[k]:
                        if plist[k] == "Clubs":
                            playerscore += 1
                        elif plist[k] == "Spades":
                            playerscore += 4
                        elif plist[k] == "Hearts":
                            playerscore += 2
                        elif plist[k] == "Diamonds":
                            playerscore += 3

    def checkTwopairDealer(self):
        tlist = []
        plist = []

        for i in range(self.dealer.inHand()):
            tlist.append(self.dealer.cards[i].getValue())
            plist.append(self.dealer.cards[i].getsuit())

        pair = 0
        dealerscore = 0
        beforevalue = 0

        for j in range(self.dealer.inHand()):
            if pair == 2:
                self.dealerscore = dealerscore + 5
                self.statusDealer = "Two Pair"
                return

            if tlist.count(tlist[j]) == 2:
                if beforevalue == tlist[j]:
                    continue

                pair += 1
                beforevalue = tlist[j]
                value = tlist[j]
                for k in range(self.dealer.inHand()):
                    if value == tlist[k]:
                        if plist[k] == "Clubs":
                            dealerscore += 1
                        elif plist[k] == "Spades":
                            dealerscore += 4
                        elif plist[k] == "Hearts":
                            dealerscore += 2
                        elif plist[k] == "Diamonds":
                            dealerscore += 3

    def checkTriplePlayer(self):
        tlist = []

        for i in range(self.player.inHand()):
            tlist.append(self.player.cards[i].getValue())

        for j in range(self.player.inHand()):
            if tlist.count(tlist[j]) == 3:
                self.playerscore = 20
                self.statusPlayer = "Triple"
                return

    def checkTripleDealer(self):
        tlist = []

        for i in range(self.dealer.inHand()):
            tlist.append(self.dealer.cards[i].getValue())

        for j in range(self.dealer.inHand()):
            if tlist.count(tlist[j]) == 3:
                self.dealerscore = 20
                self.statusDealer = "Triple"
                return

    def checkStraightPlayer(self):
        tlist = []

        for i in range(self.player.inHand()):
            tlist.append(self.player.cards[i].getValue())

        setlist = list(set(tlist))
        setlist.sort()

        if len(setlist) < 5:
            return
        else:
            if len(setlist) == 5:
                for i in range(4):
                    if(setlist[i+1] - setlist[i]) != 1:
                        return
                self.playerscore = 30
                self.statusPlayer = "Straight"
            elif len(setlist) == 6:
                straight = True
                for i in range(4):#01 12 23 34
                    if (setlist[i + 1] - setlist[i]) != 1:
                        straight = False
                        break
                if straight:
                    self.playerscore = 30
                    self.statusPlayer = "Straight"
                    return

                straight = True
                for i in range(4):  # 12 23 34 45
                    if (setlist[i + 2] - setlist[i+1]) != 1:
                        straight = False
                        break
                if straight:
                    self.playerscore = 30
                    self.statusPlayer = "Straight"
                    return
            else:
                straight = True
                for i in range(4):  # 01 12 23 34
                    if (setlist[i + 1] - setlist[i]) != 1:
                        straight = False
                        break
                if straight:
                    self.playerscore = 30
                    self.statusPlayer = "Straight"
                    return

                straight = True
                for i in range(4):  # 12 23 34 45
                    if (setlist[i + 2] - setlist[i + 1]) != 1:
                        straight = False
                        break
                if straight:
                    self.playerscore = 30
                    self.statusPlayer = "Straight"
                    return

                straight = True
                for i in range(4):  # 23 34 45 56
                    if (setlist[i + 3] - setlist[i + 2]) != 1:
                        straight = False
                        break
                if straight:
                    self.playerscore = 30
                    self.statusPlayer = "Straight"
                    return

    def checkStraightDealer(self):
        tlist = []

        for i in range(self.dealer.inHand()):
            tlist.append(self.dealer.cards[i].getValue())

        setlist = list(set(tlist))
        setlist.sort()

        if len(setlist) < 5:
            return
        else:
            if len(setlist) == 5:
                for i in range(4):
                    if (setlist[i + 1] - setlist[i]) != 1:
                        return
                self.dealerscore = 30
                self.statusDealer = "Straight"
            elif len(setlist) == 6:
                straight = True
                for i in range(4):  # 01 12 23 34
                    if (setlist[i + 1] - setlist[i]) != 1:
                        straight = False
                        break
                if straight:
                    self.dealerscore = 30
                    self.statusDealer = "Straight"
                    return

                straight = True
                for i in range(4):  # 12 23 34 45
                    if (setlist[i + 2] - setlist[i + 1]) != 1:
                        straight = False
                        break
                if straight:
                    self.dealerscore = 30
                    self.statusDealer = "Straight"
                    return
            else:
                straight = True
                for i in range(4):  # 01 12 23 34
                    if (setlist[i + 1] - setlist[i]) != 1:
                        straight = False
                        break
                if straight:
                    self.dealerscore = 30
                    self.statusDealer = "Straight"
                    return

                straight = True
                for i in range(4):  # 12 23 34 45
                    if (setlist[i + 2] - setlist[i + 1]) != 1:
                        straight = False
                        break
                if straight:
                    self.dealerscore = 30
                    self.statusDealer = "Straight"
                    return

                straight = True
                for i in range(4):  # 23 34 45 56
                    if (setlist[i + 3] - setlist[i + 2]) != 1:
                        straight = False
                        break
                if straight:
                    self.dealerscore = 30
                    self.statusDealer = "Straight"
                    return

    def checkBackStraightPlayer(self):
        tlist = []

        for i in range(self.player.inHand()):
            tlist.append(self.player.cards[i].getValue())

        setlist = list(set(tlist))
        setlist.sort()

        if len(setlist) < 5:
            return
        else:
            if len(setlist) == 5:
                if setlist == [1,2,3,4,5]:
                    self.playerscore = 40
                    self.statusPlayer = "BackStraight"
            else:
                list5 = []
                for i in range(5):
                    list5.append(setlist[i])
                if list5 == [1,2,3,4,5]:
                    self.playerscore = 40
                    self.statusPlayer = "BackStraight"

    def checkBackStraightDealer(self):
        tlist = []

        for i in range(self.dealer.inHand()):
            tlist.append(self.dealer.cards[i].getValue())

        setlist = list(set(tlist))
        setlist.sort()

        if len(setlist) < 5:
            return
        else:
            if len(setlist) == 5:
                if setlist == [1, 2, 3, 4, 5]:
                    self.dealerscore = 40
                    self.statusDealer = "BackStraight"
            else:
                list5 = []
                for i in range(5):
                    list5.append(setlist[i])
                if list5 == [1, 2, 3, 4, 5]:
                    self.dealerscore = 40
                    self.statusDealer = "BackStraight"

    def checkMountainPlayer(self):
        tlist = []

        for i in range(self.player.inHand()):
            tlist.append(self.player.cards[i].getValue())

        if len(tlist) < 5:
            return

        if tlist.count(1):
            if tlist.count(10):
                if tlist.count(11):
                    if tlist.count(12):
                        if tlist.count(13):
                            self.playerscore = 50
                            self.statusPlayer = "Mountain"

    def checkMountainDealer(self):
        tlist = []

        for i in range(self.dealer.inHand()):
            tlist.append(self.dealer.cards[i].getValue())

        if len(tlist) < 5:
            return

        if tlist.count(1):
            if tlist.count(10):
                if tlist.count(11):
                    if tlist.count(12):
                        if tlist.count(13):
                            self.dealerscore = 50
                            self.statusDealer = "Mountain"

    def checkFlushPlayer(self):
        plist = []

        for i in range(self.player.inHand()):
            plist.append(self.player.cards[i].getsuit())

        if plist.count("Clubs") == 5:
            self.playerscore = 60
            self.statusPlayer = "Flush"
        elif plist.count("Spades") == 5:
            self.playerscore = 60
            self.statusPlayer = "Flush"
        elif plist.count("Hearts") == 5:
            self.playerscore = 60
            self.statusPlayer = "Flush"
        elif plist.count("Diamonds") == 5:
            self.playerscore = 60
            self.statusPlayer = "Flush"

    def checkFlushDealer(self):
        plist = []

        for i in range(self.dealer.inHand()):
            plist.append(self.dealer.cards[i].getsuit())

        if plist.count("Clubs") == 5:
            self.dealerscore = 60
            self.statusDealer = "Flush"
        elif plist.count("Spades") == 5:
            self.dealerscore = 60
            self.statusDealer = "Flush"
        elif plist.count("Hearts") == 5:
            self.dealerscore = 60
            self.statusDealer = "Flush"
        elif plist.count("Diamonds") == 5:
            self.dealerscore = 60
            self.statusDealer = "Flush"

    def checkFullhousePlayer(self):
        tlist = []

        for i in range(self.player.inHand()):
            tlist.append(self.player.cards[i].getValue())

        two = False
        three = False

        for i in range(self.player.inHand()):
            if tlist.count(tlist[i]) == 2:
                two = True
            elif tlist.count(tlist[i]) == 3:
                three = True

        if two and three:
            self.playerscore = 70
            self.statusPlayer = "Fullhouse"

    def checkFullhouseDealer(self):
        tlist = []

        for i in range(self.dealer.inHand()):
            tlist.append(self.dealer.cards[i].getValue())

        two = False
        three = False

        for i in range(self.dealer.inHand()):
            if tlist.count(tlist[i]) == 2:
                two = True
            elif tlist.count(tlist[i]) == 3:
                three = True

        if two and three:
            self.dealerscore = 70
            self.statusDealer = "Fullhouse"

    def checkFourcardPlayer(self):
        tlist = []

        for i in range(self.player.inHand()):
            tlist.append(self.player.cards[i].getValue())

        for i in range(self.player.inHand()):
            if tlist.count(tlist[i])  == 4:
                self.playerscore = 80
                self.statusPlayer = "Four Card"
                return

    def checkFourcardDealer(self):
        tlist = []

        for i in range(self.dealer.inHand()):
            tlist.append(self.dealer.cards[i].getValue())

        for i in range(self.dealer.inHand()):
            if tlist.count(tlist[i])  == 4:
                self.dealerscore = 80
                self.statusDealer = "Four Card"
                return

    def checkStraightFlushPlayer(self):
        plist = []

        for i in range(self.player.inHand()):
            plist.append(self.player.cards[i].getsuit())

        if plist.count("Clubs") >= 5:
            index = [i for i, value in enumerate(plist) if value == "Clubs"]
            tlist = [self.player.cards[i].getValue() for i in index]
            tlist.sort()

            if len(tlist) == 5:
                for i in range(4):
                    if(tlist[i+1] - tlist[i]) != 1:
                        return
                self.playerscore = 90
                self.statusPlayer = "Straight Flush"

            elif len(tlist) == 6:
                straight = True
                for i in range(4):  # 01 12 23 34
                    if (tlist[i + 1] - tlist[i]) != 1:
                        straight = False
                        break
                if straight:
                    self.playerscore = 90
                    self.statusPlayer = "Straight Flush"
                    return

                straight = True
                for i in range(4):  # 12 23 34 45
                    if (tlist[i + 2] - tlist[i + 1]) != 1:
                        straight = False
                        break
                if straight:
                    self.playerscore = 90
                    self.statusPlayer = "Straight Flush"
                    return
            else:
                straight = True
                for i in range(4):  # 01 12 23 34
                    if (tlist[i + 1] - tlist[i]) != 1:
                        straight = False
                        break
                if straight:
                    self.playerscore = 90
                    self.statusPlayer = "Straight Flush"
                    return

                straight = True
                for i in range(4):  # 12 23 34 45
                    if (tlist[i + 2] - tlist[i + 1]) != 1:
                        straight = False
                        break
                if straight:
                    self.playerscore = 90
                    self.statusPlayer = "Straight Flush"
                    return

                straight = True
                for i in range(4):  # 23 34 45 56
                    if (tlist[i + 3] - tlist[i + 2]) != 1:
                        straight = False
                        break
                if straight:
                    self.playerscore = 90
                    self.statusPlayer = "Straight Flush"
                    return
        elif plist.count("Spades") >= 5:
            index = [i for i, value in enumerate(plist) if value == "Spades"]
            tlist = [self.player.cards[i].getValue() for i in index]
            tlist.sort()

            if len(tlist) == 5:
                for i in range(4):
                    if (tlist[i + 1] - tlist[i]) != 1:
                        return
                self.playerscore = 90
                self.statusPlayer = "Straight Flush"

            elif len(tlist) == 6:
                straight = True
                for i in range(4):  # 01 12 23 34
                    if (tlist[i + 1] - tlist[i]) != 1:
                        straight = False
                        break
                if straight:
                    self.playerscore = 90
                    self.statusPlayer = "Straight Flush"
                    return

                straight = True
                for i in range(4):  # 12 23 34 45
                    if (tlist[i + 2] - tlist[i + 1]) != 1:
                        straight = False
                        break
                if straight:
                    self.playerscore = 90
                    self.statusPlayer = "Straight Flush"
                    return
            else:
                straight = True
                for i in range(4):  # 01 12 23 34
                    if (tlist[i + 1] - tlist[i]) != 1:
                        straight = False
                        break
                if straight:
                    self.playerscore = 90
                    self.statusPlayer = "Straight Flush"
                    return

                straight = True
                for i in range(4):  # 12 23 34 45
                    if (tlist[i + 2] - tlist[i + 1]) != 1:
                        straight = False
                        break
                if straight:
                    self.playerscore = 90
                    self.statusPlayer = "Straight Flush"
                    return

                straight = True
                for i in range(4):  # 23 34 45 56
                    if (tlist[i + 3] - tlist[i + 2]) != 1:
                        straight = False
                        break
                if straight:
                    self.playerscore = 90
                    self.statusPlayer = "Straight Flush"
                    return
        elif plist.count("Hearts") >= 5:
            index = [i for i, value in enumerate(plist) if value == "Hearts"]
            tlist = [self.player.cards[i].getValue() for i in index]
            tlist.sort()

            if len(tlist) == 5:
                for i in range(4):
                    if (tlist[i + 1] - tlist[i]) != 1:
                        return
                self.playerscore = 90
                self.statusPlayer = "Straight Flush"

            elif len(tlist) == 6:
                straight = True
                for i in range(4):  # 01 12 23 34
                    if (tlist[i + 1] - tlist[i]) != 1:
                        straight = False
                        break
                if straight:
                    self.playerscore = 90
                    self.statusPlayer = "Straight Flush"
                    return

                straight = True
                for i in range(4):  # 12 23 34 45
                    if (tlist[i + 2] - tlist[i + 1]) != 1:
                        straight = False
                        break
                if straight:
                    self.playerscore = 90
                    self.statusPlayer = "Straight Flush"
                    return
            else:
                straight = True
                for i in range(4):  # 01 12 23 34
                    if (tlist[i + 1] - tlist[i]) != 1:
                        straight = False
                        break
                if straight:
                    self.playerscore = 90
                    self.statusPlayer = "Straight Flush"
                    return

                straight = True
                for i in range(4):  # 12 23 34 45
                    if (tlist[i + 2] - tlist[i + 1]) != 1:
                        straight = False
                        break
                if straight:
                    self.playerscore = 90
                    self.statusPlayer = "Straight Flush"
                    return

                straight = True
                for i in range(4):  # 23 34 45 56
                    if (tlist[i + 3] - tlist[i + 2]) != 1:
                        straight = False
                        break
                if straight:
                    self.playerscore = 90
                    self.statusPlayer = "Straight Flush"
                    return
        elif plist.count("Diamonds") >= 5:
            index = [i for i, value in enumerate(plist) if value == "Diamonds"]
            tlist = [self.player.cards[i].getValue() for i in index]
            tlist.sort()

            if len(tlist) == 5:
                for i in range(4):
                    if (tlist[i + 1] - tlist[i]) != 1:
                        return
                self.playerscore = 90
                self.statusPlayer = "Straight Flush"

            elif len(tlist) == 6:
                straight = True
                for i in range(4):  # 01 12 23 34
                    if (tlist[i + 1] - tlist[i]) != 1:
                        straight = False
                        break
                if straight:
                    self.playerscore = 90
                    self.statusPlayer = "Straight Flush"
                    return

                straight = True
                for i in range(4):  # 12 23 34 45
                    if (tlist[i + 2] - tlist[i + 1]) != 1:
                        straight = False
                        break
                if straight:
                    self.playerscore = 90
                    self.statusPlayer = "Straight Flush"
                    return
            else:
                straight = True
                for i in range(4):  # 01 12 23 34
                    if (tlist[i + 1] - tlist[i]) != 1:
                        straight = False
                        break
                if straight:
                    self.playerscore = 90
                    self.statusPlayer = "Straight Flush"
                    return

                straight = True
                for i in range(4):  # 12 23 34 45
                    if (tlist[i + 2] - tlist[i + 1]) != 1:
                        straight = False
                        break
                if straight:
                    self.playerscore = 90
                    self.statusPlayer = "Straight Flush"
                    return

                straight = True
                for i in range(4):  # 23 34 45 56
                    if (tlist[i + 3] - tlist[i + 2]) != 1:
                        straight = False
                        break
                if straight:
                    self.playerscore = 90
                    self.statusPlayer = "Straight Flush"
                    return

    def checkStraightFlushDealer(self):
        plist = []

        for i in range(self.dealer.inHand()):
            plist.append(self.dealer.cards[i].getsuit())

        if plist.count("Clubs") >= 5:
            index = [i for i, value in enumerate(plist) if value == "Clubs"]
            tlist = [self.dealer.cards[i].getValue() for i in index]
            tlist.sort()

            if len(tlist) == 5:
                for i in range(4):
                    if (tlist[i + 1] - tlist[i]) != 1:
                        return
                self.dealerscore = 80
                self.statusDealer = "Straight Flush"

            elif len(tlist) == 6:
                straight = True
                for i in range(4):  # 01 12 23 34
                    if (tlist[i + 1] - tlist[i]) != 1:
                        straight = False
                        break
                if straight:
                    self.dealerscore = 80
                    self.statusDealer = "Straight Flush"
                    return

                straight = True
                for i in range(4):  # 12 23 34 45
                    if (tlist[i + 2] - tlist[i + 1]) != 1:
                        straight = False
                        break
                if straight:
                    self.dealerscore = 80
                    self.statusDealer = "Straight Flush"
                    return
            else:
                straight = True
                for i in range(4):  # 01 12 23 34
                    if (tlist[i + 1] - tlist[i]) != 1:
                        straight = False
                        break
                if straight:
                    self.dealerscore = 80
                    self.statusDealer = "Straight Flush"
                    return

                straight = True
                for i in range(4):  # 12 23 34 45
                    if (tlist[i + 2] - tlist[i + 1]) != 1:
                        straight = False
                        break
                if straight:
                    self.dealerscore = 80
                    self.statusDealer = "Straight Flush"
                    return

                straight = True
                for i in range(4):  # 23 34 45 56
                    if (tlist[i + 3] - tlist[i + 2]) != 1:
                        straight = False
                        break
                if straight:
                    self.dealerscore = 80
                    self.statusDealer = "Straight Flush"
                    return
        elif plist.count("Spades") >= 5:
            index = [i for i, value in enumerate(plist) if value == "Spades"]
            tlist = [self.dealer.cards[i].getValue() for i in index]
            tlist.sort()

            if len(tlist) == 5:
                for i in range(4):
                    if (tlist[i + 1] - tlist[i]) != 1:
                        return
                self.dealerscore = 90
                self.statusDealer = "Straight Flush"

            elif len(tlist) == 6:
                straight = True
                for i in range(4):  # 01 12 23 34
                    if (tlist[i + 1] - tlist[i]) != 1:
                        straight = False
                        break
                if straight:
                    self.dealerscore = 90
                    self.statusDealer = "Straight Flush"
                    return

                straight = True
                for i in range(4):  # 12 23 34 45
                    if (tlist[i + 2] - tlist[i + 1]) != 1:
                        straight = False
                        break
                if straight:
                    self.dealerscore = 90
                    self.statusDealer = "Straight Flush"
                    return
            else:
                straight = True
                for i in range(4):  # 01 12 23 34
                    if (tlist[i + 1] - tlist[i]) != 1:
                        straight = False
                        break
                if straight:
                    self.dealerscore = 90
                    self.statusDealer = "Straight Flush"
                    return

                straight = True
                for i in range(4):  # 12 23 34 45
                    if (tlist[i + 2] - tlist[i + 1]) != 1:
                        straight = False
                        break
                if straight:
                    self.dealerscore = 90
                    self.statusDealer = "Straight Flush"
                    return

                straight = True
                for i in range(4):  # 23 34 45 56
                    if (tlist[i + 3] - tlist[i + 2]) != 1:
                        straight = False
                        break
                if straight:
                    self.dealerscore = 90
                    self.statusDealer = "Straight Flush"
                    return
        elif plist.count("Hearts") >= 5:
            index = [i for i, value in enumerate(plist) if value == "Hearts"]
            tlist = [self.dealer.cards[i].getValue() for i in index]
            tlist.sort()

            if len(tlist) == 5:
                for i in range(4):
                    if (tlist[i + 1] - tlist[i]) != 1:
                        return
                self.dealerscore = 90
                self.statusDealer = "Straight Flush"

            elif len(tlist) == 6:
                straight = True
                for i in range(4):  # 01 12 23 34
                    if (tlist[i + 1] - tlist[i]) != 1:
                        straight = False
                        break
                if straight:
                    self.dealerscore = 90
                    self.statusDealer = "Straight Flush"
                    return

                straight = True
                for i in range(4):  # 12 23 34 45
                    if (tlist[i + 2] - tlist[i + 1]) != 1:
                        straight = False
                        break
                if straight:
                    self.dealerscore = 90
                    self.statusDealer = "Straight Flush"
                    return
            else:
                straight = True
                for i in range(4):  # 01 12 23 34
                    if (tlist[i + 1] - tlist[i]) != 1:
                        straight = False
                        break
                if straight:
                    self.dealerscore = 90
                    self.statusDealer = "Straight Flush"
                    return

                straight = True
                for i in range(4):  # 12 23 34 45
                    if (tlist[i + 2] - tlist[i + 1]) != 1:
                        straight = False
                        break
                if straight:
                    self.dealerscore = 90
                    self.statusDealer = "Straight Flush"
                    return

                straight = True
                for i in range(4):  # 23 34 45 56
                    if (tlist[i + 3] - tlist[i + 2]) != 1:
                        straight = False
                        break
                if straight:
                    self.dealerscore = 90
                    self.statusDealer = "Straight Flush"
                    return
        elif plist.count("Diamonds") >= 5:
            index = [i for i, value in enumerate(plist) if value == "Diamonds"]
            tlist = [self.dealer.cards[i].getValue() for i in index]
            tlist.sort()

            if len(tlist) == 5:
                for i in range(4):
                    if (tlist[i + 1] - tlist[i]) != 1:
                        return
                self.dealerscore = 90
                self.statusDealer = "Straight Flush"

            elif len(tlist) == 6:
                straight = True
                for i in range(4):  # 01 12 23 34
                    if (tlist[i + 1] - tlist[i]) != 1:
                        straight = False
                        break
                if straight:
                    self.dealerscore = 90
                    self.statusDealer = "Straight Flush"
                    return

                straight = True
                for i in range(4):  # 12 23 34 45
                    if (tlist[i + 2] - tlist[i + 1]) != 1:
                        straight = False
                        break
                if straight:
                    self.dealerscore = 90
                    self.statusDealer = "Straight Flush"
                    return
            else:
                straight = True
                for i in range(4):  # 01 12 23 34
                    if (tlist[i + 1] - tlist[i]) != 1:
                        straight = False
                        break
                if straight:
                    self.dealerscore = 90
                    self.statusDealer = "Straight Flush"
                    return

                straight = True
                for i in range(4):  # 12 23 34 45
                    if (tlist[i + 2] - tlist[i + 1]) != 1:
                        straight = False
                        break
                if straight:
                    self.dealerscore = 90
                    self.statusDealer = "Straight Flush"
                    return

                straight = True
                for i in range(4):  # 23 34 45 56
                    if (tlist[i + 3] - tlist[i + 2]) != 1:
                        straight = False
                        break
                if straight:
                    self.dealerscore = 90
                    self.statusDealer = "Straight Flush"
                    return

    def checkBackStraightFlushPlayer(self):
        plist = []

        for i in range(self.player.inHand()):
            plist.append(self.player.cards[i].getsuit())

        if plist.count("Clubs") >= 5:
            index = [i for i, value in enumerate(plist) if value == "Clubs"]
            tlist = [self.player.cards[i].getValue() for i in index]
            tlist.sort()

            if len(tlist) == 5:
                if plist == [1,2,3,4,5]:
                    self.playerscore = 100
                    self.statusPlayer = "BackStraight Flush"
            else:
                list5 = []
                for i in range(5):
                    list5.append(tlist[i])
                if list5 == [1,2,3,4,5]:
                    self.playerscore = 100
                    self.statusPlayer = "BackStraight Flush"

        elif plist.count("Spades") >= 5:
            index = [i for i, value in enumerate(plist) if value == "Spades"]
            tlist = [self.player.cards[i].getValue() for i in index]
            tlist.sort()

            if len(tlist) == 5:
                if plist == [1, 2, 3, 4, 5]:
                    self.playerscore = 100
                    self.statusPlayer = "BackStraight Flush"
            else:
                list5 = []
                for i in range(5):
                    list5.append(tlist[i])
                if list5 == [1, 2, 3, 4, 5]:
                    self.playerscore = 100
                    self.statusPlayer = "BackStraight Flush"

        elif plist.count("Hearts") >= 5:
            index = [i for i, value in enumerate(plist) if value == "Hearts"]
            tlist = [self.player.cards[i].getValue() for i in index]
            tlist.sort()

            if len(tlist) == 5:
                if plist == [1, 2, 3, 4, 5]:
                    self.playerscore = 100
                    self.statusPlayer = "BackStraight Flush"
            else:
                list5 = []
                for i in range(5):
                    list5.append(tlist[i])
                if list5 == [1, 2, 3, 4, 5]:
                    self.playerscore = 100
                    self.statusPlayer = "BackStraight Flush"

        elif plist.count("Diamonds") >= 5:
            index = [i for i, value in enumerate(plist) if value == "Diamonds"]
            tlist = [self.player.cards[i].getValue() for i in index]
            tlist.sort()

            if len(tlist) == 5:
                if plist == [1, 2, 3, 4, 5]:
                    self.playerscore = 100
                    self.statusPlayer = "BackStraight Flush"
            else:
                list5 = []
                for i in range(5):
                    list5.append(tlist[i])
                if list5 == [1, 2, 3, 4, 5]:
                    self.playerscore = 100
                    self.statusPlayer = "BackStraight Flush"

    def checkBackStraightFlushDealer(self):
        plist = []

        for i in range(self.dealer.inHand()):
            plist.append(self.dealer.cards[i].getsuit())

        if plist.count("Clubs") >= 5:
            index = [i for i, value in enumerate(plist) if value == "Clubs"]
            tlist = [self.dealer.cards[i].getValue() for i in index]
            tlist.sort()

            if len(tlist) == 5:
                if plist == [1, 2, 3, 4, 5]:
                    self.dealerscore = 100
                    self.statusDealer = "BackStraight Flush"
            else:
                list5 = []
                for i in range(5):
                    list5.append(tlist[i])
                if list5 == [1, 2, 3, 4, 5]:
                    self.dealerscore = 100
                    self.statusDealer = "BackStraight Flush"

        elif plist.count("Spades") >= 5:
            index = [i for i, value in enumerate(plist) if value == "Spades"]
            tlist = [self.dealer.cards[i].getValue() for i in index]
            tlist.sort()

            if len(tlist) == 5:
                if plist == [1, 2, 3, 4, 5]:
                    self.dealerscore = 100
                    self.statusDealer = "BackStraight Flush"
            else:
                list5 = []
                for i in range(5):
                    list5.append(tlist[i])
                if list5 == [1, 2, 3, 4, 5]:
                    self.dealerscore = 100
                    self.statusDealer = "BackStraight Flush"

        elif plist.count("Hearts") >= 5:
            index = [i for i, value in enumerate(plist) if value == "Hearts"]
            tlist = [self.dealer.cards[i].getValue() for i in index]
            tlist.sort()

            if len(tlist) == 5:
                if plist == [1, 2, 3, 4, 5]:
                    self.dealerscore = 100
                    self.statusDealer = "BackStraight Flush"
            else:
                list5 = []
                for i in range(5):
                    list5.append(tlist[i])
                if list5 == [1, 2, 3, 4, 5]:
                    self.dealerscore = 100
                    self.statusDealer = "BackStraight Flush"

        elif plist.count("Diamonds") >= 5:
            index = [i for i, value in enumerate(plist) if value == "Diamonds"]
            tlist = [self.dealer.cards[i].getValue() for i in index]
            tlist.sort()

            if len(tlist) == 5:
                if plist == [1, 2, 3, 4, 5]:
                    self.dealerscore = 100
                    self.statusDealer = "BackStraight Flush"
            else:
                list5 = []
                for i in range(5):
                    list5.append(tlist[i])
                if list5 == [1, 2, 3, 4, 5]:
                    self.dealerscore = 100
                    self.statusDealer = "BackStraight Flush"

    def checkRoyalStraightFlushPlayer(self):
        plist = []

        for i in range(self.player.inHand()):
            plist.append(self.player.cards[i].getsuit())

        if plist.count("Clubs") >= 5:
            index = [i for i, value in enumerate(plist) if value == "Clubs"]
            tlist = [self.player.cards[i].getValue() for i in index]

            if tlist.count(1):
                if tlist.count(10):
                    if tlist.count(11):
                        if tlist.count(12):
                            if tlist.count(13):
                                self.playerscore = 110
                                self.statusPlayer = "Royal Straight Flush"

        elif plist.count("Spades") >= 5:
            index = [i for i, value in enumerate(plist) if value == "Spades"]
            tlist = [self.player.cards[i].getValue() for i in index]

            if tlist.count(1):
                if tlist.count(10):
                    if tlist.count(11):
                        if tlist.count(12):
                            if tlist.count(13):
                                self.playerscore = 110
                                self.statusPlayer = "Royal Straight Flush"
        elif plist.count("Hearts") >= 5:
            index = [i for i, value in enumerate(plist) if value == "Hearts"]
            tlist = [self.player.cards[i].getValue() for i in index]

            if tlist.count(1):
                if tlist.count(10):
                    if tlist.count(11):
                        if tlist.count(12):
                            if tlist.count(13):
                                self.playerscore = 110
                                self.statusPlayer = "Royal Straight Flush"

        elif plist.count("Diamonds") >= 5:
            index = [i for i, value in enumerate(plist) if value == "Diamonds"]
            tlist = [self.player.cards[i].getValue() for i in index]

            if tlist.count(1):
                if tlist.count(10):
                    if tlist.count(11):
                        if tlist.count(12):
                            if tlist.count(13):
                                self.playerscore = 110
                                self.statusPlayer = "Royal Straight Flush"

    def checkRoyalStraightFlushDealer(self):
        plist = []

        for i in range(self.dealer.inHand()):
            plist.append(self.dealer.cards[i].getsuit())

        if plist.count("Clubs") >= 5:
            index = [i for i, value in enumerate(plist) if value == "Clubs"]
            tlist = [self.dealer.cards[i].getValue() for i in index]

            if tlist.count(1):
                if tlist.count(10):
                    if tlist.count(11):
                        if tlist.count(12):
                            if tlist.count(13):
                                self.dealerscore = 110
                                self.statusDealer = "Royal Straight Flush"

        elif plist.count("Spades") >= 5:
            index = [i for i, value in enumerate(plist) if value == "Spades"]
            tlist = [self.dealer.cards[i].getValue() for i in index]

            if tlist.count(1):
                if tlist.count(10):
                    if tlist.count(11):
                        if tlist.count(12):
                            if tlist.count(13):
                                self.dealerscore = 110
                                self.statusDealer = "Royal Straight Flush"
        elif plist.count("Hearts") >= 5:
            index = [i for i, value in enumerate(plist) if value == "Hearts"]
            tlist = [self.dealer.cards[i].getValue() for i in index]

            if tlist.count(1):
                if tlist.count(10):
                    if tlist.count(11):
                        if tlist.count(12):
                            if tlist.count(13):
                                self.dealerscore = 110
                                self.statusDealer = "Royal Straight Flush"

        elif plist.count("Diamonds") >= 5:
            index = [i for i, value in enumerate(plist) if value == "Diamonds"]
            tlist = [self.dealer.cards[i].getValue() for i in index]

            if tlist.count(1):
                if tlist.count(10):
                    if tlist.count(11):
                        if tlist.count(12):
                            if tlist.count(13):
                                self.dealerscore = 110
                                self.statusDealer = "Royal Straight Flush"

    def pressedBetx1(self):
        if self.playerMoney < self.betMoney:
            return

        if self.betMoney *2  <= self.playerMoney:
            self.playerMoney -= self.betMoney
            self.betMoney += self.betMoney
            self.LbetMoney.configure(text = "$" + str(self.betMoney))
            self.LPlayertMoney.configure(text = "You have $" + str(self.playerMoney))
            self.Deal["state"] = "active"
            self.Deal["bg"] = "white"
            self.Betx1['state'] = 'disabled'
            self.Betx1["bg"] = "gray"
            self.Betx2['state'] = 'disabled'
            self.Betx2["bg"] = "gray"
            self.Check['state'] = 'disabled'
            self.Check["bg"] = "gray"
            PlaySound('sounds/chip.wav', SND_FILENAME)

    def pressedBetx2(self):
        if self.playerMoney < self.betMoney:
            return

        if self.betMoney + self.betMoney*2 <= self.playerMoney:
            self.playerMoney -= self.betMoney*2
            self.betMoney += self.betMoney*2
            self.LbetMoney.configure(text = "$" + str(self.betMoney))
            self.LPlayertMoney.configure(text = "You have $" + str(self.playerMoney))
            self.Deal["state"] = "active"
            self.Deal["bg"] = "white"
            self.Betx1['state'] = 'disabled'
            self.Betx1["bg"] = "gray"
            self.Betx2['state'] = 'disabled'
            self.Betx2["bg"] = "gray"
            self.Check['state'] = 'disabled'
            self.Check["bg"] = "gray"
            PlaySound('sounds/chip.wav', SND_FILENAME)

    def getCardPlayer(self, n):
        newCard = Card(self.cardDeck[self.deckN])
        self.deckN += 1
        self.player.addCard(newCard)
        p = PhotoImage(file="cards/"+ newCard.filename())
        self.LcardsPlayer.append(Label(self.window, image=p))

        self.LcardsPlayer[self.player.inHand() - 1].image = p
        self.LcardsPlayer[self.player.inHand() - 1].place(x=50 + n*80, y= 350)

    def getCardDealer(self, n):
        newCard = Card(self.cardDeck[self.deckN])
        self.deckN += 1
        self.dealer.addCard(newCard)
        p = PhotoImage(file="cards/b2fv.png")
        self.LcardsDealer.append(Label(self.window, image=p))

        self.LcardsDealer[self.dealer.inHand() - 1].image = p
        self.LcardsDealer[self.dealer.inHand() - 1].place(x=50 + n*80, y= 50)

    def getCardMaster(self,n):
        newCard = Card(self.cardDeck[self.deckN])
        self.deckN += 1
        self.mastercards.append(newCard)
        p = PhotoImage(file="cards/"+ newCard.filename())
        self.Lmatercards.append(Label(self.window, image=p))

        self.Lmatercards[n].image = p
        self.Lmatercards[n].place(x=100 + n*80, y = 200)

    def pressedDeal(self):
        if self.player.inHand() == 0:#카드를 한장도 안 갖고 있음
            self.cardDeck = [i for i in range(52)]
            random.shuffle(self.cardDeck)
            self.deckN = 0
            self.getCardPlayer(0)
            self.getCardPlayer(1)
            self.getCardDealer(0)
            self.getCardDealer(1)
            PlaySound('sounds/cardFlip1.wav', SND_FILENAME)

        elif self.player.inHand() == 2:#카드를 가짐
            if len(self.mastercards) <3:
                for i in range(3):
                    self.getCardMaster(i)

            elif len(self.mastercards) == 3:
                self.getCardMaster(3)

            elif len(self.mastercards) == 4:
                self.getCardMaster(4)

            elif len(self.mastercards) == 5:
                print(self.player.inHand())
                self.pressedCheck()
            PlaySound('sounds/cardFlip1.wav', SND_FILENAME)


        self.Deal["state"] = "disabled"
        self.Deal["bg"] = "gray"
        self.Betx1['state'] = 'active'
        self.Betx1["bg"] = "white"
        self.Betx2['state'] = 'active'
        self.Betx2["bg"] = "white"
        self.Check['state'] = 'active'
        self.Check["bg"] = "white"

    def pressedAgain(self):
        self.player.reset()
        self.dealer.reset()
        self.mastercards.clear()
        self.betMoney = 10
        self.LbetMoney.configure(text="$" + str(self.betMoney))
        self.playerMoney -= self.betMoney
        self.LPlayertMoney.configure(text = "You have &" + str(self.playerMoney))

        self.nCardsDealer = 0
        self.nCardsPlayer = 0

        for i in self.LcardsPlayer:
            i.destroy()

        for i in self.LcardsDealer:
            i.destroy()

        for i in self.Lmatercards:
            i.destroy()

        self.LcardsPlayer.clear()
        self.LcardsDealer.clear()
        self.Lmatercards.clear()
        self.playerscore=0
        self.dealerscore=0

        self.statusDealer = ""
        self.statusPlayer = ""
        self.LstatusPlayer.configure(text = "")
        self.LstatusDealer.configure(text = "")
        self.Lwinner.configure(text = "")

        self.deckN = 0

        self.Deal['state'] = 'disabled'
        self.Deal['bg'] = 'gray'
        self.Again['state'] = 'disabled'
        self.Again['bg'] = 'gray'

        self.Betx1['state'] = 'active'
        self.Betx1["bg"] = "white"
        self.Betx2['state'] = 'active'
        self.Betx2["bg"] = "white"
        self.Check['state'] = 'active'
        self.Check["bg"] = "white"

        PlaySound('sounds/ding.wav', SND_FILENAME)

    def __init__(self):
        self.window = Tk()
        self.window.title("Texas Holdem Pocker")
        self.window.geometry("800x600")
        self.window.configure(bg = "dark green")
        self.fontstyle = font.Font(self.window, size = 24, weight = 'bold',family = 'Consolas')
        self.fontstyle2 = font.Font(self.window, size = 16, weight = 'bold',family = 'Consolas')
        self.setupButton()
        self.setupLabel()

        self.player = Player("player")
        self.dealer = Player("dealer")
        self.mastercards = []
        self.betMoney = 10
        self.playerMoney = 990
        self.nCardsDealer = 0
        self.nCardsPlayer = 0
        self.LcardsDealer = []
        self.LcardsPlayer = []
        self.Lmatercards = []
        self.statusPlayer = ""
        self.statusDealer = ""

        self.deckN = 0

        self.window.mainloop()


MainGame()