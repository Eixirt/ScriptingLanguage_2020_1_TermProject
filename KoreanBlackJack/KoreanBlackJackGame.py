from tkinter import *
from tkinter import font
from winsound import *
from PIL import Image, ImageTk
from KoreanBlackJackCard import *
from KoreanBlackJackPlayer import *
from random import *


class MainGame:
    def __init__(self):
        self.window = Tk()
        self.window.title("도리짓고땡")

        self.canvas = Canvas(self.window, height=720, width=1280)
        self.canvas.pack()

        backgroundImage = Image.open('Resource\\GodoriCards\\table.gif')
        resizeBackgroundImage = backgroundImage.resize((1300, 740), Image.ANTIALIAS)
        self.backgroundImage = ImageTk.PhotoImage(resizeBackgroundImage)

        self.backgroundLabel = self.canvas.create_image((640, 360), image=self.backgroundImage, anchor='center')

        self.fontBasicStyle = font.Font(self.window, size=24, weight='bold', family='Consolas')
        self.fontMiniStyle = font.Font(self.window, size=16, weight='bold', family='Consolas')

        self.buttons = {'player1': {'bet5Button': None, 'bet1Button': None},
                        'player2': {'bet5Button': None, 'bet1Button': None},
                        'player3': {'bet5Button': None, 'bet1Button': None},
                        'deal': None,
                        'again': None}

        self.players = {'player1': {'class': Player('player1'), 'betMoney': 0, 'cards': [], 'cardsText': [], 'valueText': [], 'subText': [], 'winText': []},
                        'player2': {'class': Player('player2'), 'betMoney': 0, 'cards': [], 'cardsText': [], 'valueText': [], 'subText': [], 'winText': []},
                        'player3': {'class': Player('player3'), 'betMoney': 0, 'cards': [], 'cardsText': [], 'valueText': [], 'subText': [], 'winText': []},
                        'dealer': {'class': Player('dealer'), 'cards': [], 'cardsText': [], 'valueText': [], 'subText': []}
                        }

        self.handRankings = {'콩콩팔': [1, 1, 8], '삐리칠': [1, 2, 7], '물삼육': [1, 3, 6], '빽새오': [1, 4, 5], '삥구장': [1, 9, 10],
                             '니니육': [2, 2, 6], '이삼오': [2, 3, 5], '이판장': [2, 8, 10],
                             '심심새': [3, 3, 4], '삼칠장': [3, 7, 10], '삼빡구': [3, 8, 9],
                             '살살이': [4, 4, 2], '사륙장': [4, 6, 10], '사칠구': [4, 7, 9],
                             '꼬꼬장': [5, 5, 10], '오륙구': [5, 6, 9], '오리발': [5, 7, 8],
                             '쭉쭉팔': [6, 6, 8],
                             '철철육': [7, 7, 6],
                             '팍팍싸': [8, 8, 4],
                             '구구리': [9, 9, 2]
                             }

        self.player1BetMoneyText = None
        self.player2BetMoneyText = None
        self.player3BetMoneyText = None

        self.totalMoney = 1000
        self.totalMoneyText = None

        self.turnState = 0

        self.cardDeck = [i for i in range(40)]
        self.currCardNum = 0

        self.SetupButtons()
        self.SetupLabels()

        self.window.mainloop()
        pass

    def SetupButtons(self):
        self.buttons['player1']['bet5Button'] = Button(self.window, text="5만", width=6, height=1, font=self.fontMiniStyle, command=lambda: self.PressBet(5, 'player1'))
        self.buttons['player1']['bet5Button'].place(x=40, y=650)
        self.buttons['player1']['bet1Button'] = Button(self.window, text="1만", width=6, height=1, font=self.fontMiniStyle, command=lambda: self.PressBet(1, 'player1'))
        self.buttons['player1']['bet1Button'].place(x=140, y=650)

        self.buttons['player2']['bet5Button'] = Button(self.window, text="5만", width=6, height=1, font=self.fontMiniStyle, command=lambda: self.PressBet(5, 'player2'))
        self.buttons['player2']['bet5Button'].place(x=380, y=650)
        self.buttons['player2']['bet1Button'] = Button(self.window, text="1만", width=6, height=1, font=self.fontMiniStyle, command=lambda: self.PressBet(1, 'player2'))
        self.buttons['player2']['bet1Button'].place(x=480, y=650)

        self.buttons['player3']['bet5Button'] = Button(self.window, text="5만", width=6, height=1, font=self.fontMiniStyle, command=lambda: self.PressBet(5, 'player3'))
        self.buttons['player3']['bet5Button'].place(x=720, y=650)
        self.buttons['player3']['bet1Button'] = Button(self.window, text="1만", width=6, height=1, font=self.fontMiniStyle, command=lambda: self.PressBet(1, 'player3'))
        self.buttons['player3']['bet1Button'].place(x=820, y=650)

        self.buttons['deal'] = Button(self.window, text="Deal", width=6, height=1, font=self.fontMiniStyle, command=lambda: self.PressDeal())
        self.buttons['deal'].place(x=1070, y=650)

        self.buttons['again'] = Button(self.window, text="Again", width=6, height=1, font=self.fontMiniStyle, command=lambda: self.PressAgain())
        self.buttons['again'].place(x=1170, y=650)

        self.buttons['again']['state'] = 'disabled'
        self.buttons['again']['bg'] = 'gray'
        pass

    def SetupLabels(self):
        self.player1BetMoneyText = self.canvas.create_text((135, 600), text=str(self.players['player1']['betMoney']) + "만", font=self.fontBasicStyle, fill='cyan')
        self.player2BetMoneyText = self.canvas.create_text((475, 600), text="0만", font=self.fontBasicStyle, fill='cyan')
        self.player3BetMoneyText = self.canvas.create_text((815, 600), text="0만", font=self.fontBasicStyle, fill='cyan')
        self.totalMoneyText = self.canvas.create_text((1165, 550), text="1000만원", font=self.fontBasicStyle, fill='dark blue')
        pass

    def PressBet(self, score, playerName):
        PlaySound('Resource/sounds/chip.wav', SND_FILENAME)

        self.players[playerName]['betMoney'] += score

        self.canvas.itemconfig(self.player1BetMoneyText, text=str(self.players['player1']['betMoney']) + "만")
        self.canvas.itemconfig(self.player2BetMoneyText, text=str(self.players['player2']['betMoney']) + "만")
        self.canvas.itemconfig(self.player3BetMoneyText, text=str(self.players['player3']['betMoney']) + "만")

        self.totalMoney -= score
        self.canvas.itemconfig(self.totalMoneyText, text=str(self.totalMoney) + "만원")
        pass

    def PressDeal(self):
        if self.turnState == 0:  # 카드 1장 받는다
            PlaySound('Resource/sounds/cardFlip1.wav', SND_FILENAME)
            self.ProgressFirstTurn()
            pass
        elif self.turnState == 1:  # 카드 3장 받는다
            PlaySound('Resource/sounds/cardFlip1.wav', SND_FILENAME)
            self.ProgressSecondTurn()
            pass
        elif self.turnState == 2:  # 대결!
            self.buttons['deal']['state'] = 'disabled'
            self.buttons['deal']['bg'] = 'gray'

            self.buttons['again']['state'] = 'active'
            self.buttons['again']['bg'] = 'white'

            for i in range(3):
                self.buttons['player' + str(i + 1)]['bet5Button']['state'] = 'disabled'
                self.buttons['player' + str(i + 1)]['bet5Button']['bg'] = 'gray'
                self.buttons['player' + str(i + 1)]['bet1Button']['state'] = 'disabled'
                self.buttons['player' + str(i + 1)]['bet1Button']['bg'] = 'gray'

            self.ProgressThirdTurn()
            pass
        self.turnState = (self.turnState + 1) % 3
        pass

    def ProgressFirstTurn(self):
        self.cardDeck = [i for i in range(40)]
        shuffle(self.cardDeck)

        for i in range(3):
            newCard = Card(self.cardDeck[self.currCardNum])
            self.currCardNum += 1
            self.players["player" + str(i + 1)]["class"].AddCard(newCard)

            p = ImageTk.PhotoImage(file=newCard.CardFileName())
            # self.players["player"+str(i+1)]["cards"].append(self.canvas.create_image((300 * i + 30, 400), image=p, anchor='center'))
            self.players["player" + str(i + 1)]["cards"].append(Label(self.window, image=p))
            self.players["player" + str(i + 1)]["cardsText"].append(self.canvas.create_text((340 * i + 65, 380), text=str(newCard.GetPattern()),
                                                                                            font=self.fontMiniStyle, anchor='center', fill='white'))

            self.players["player" + str(i + 1)]["cards"][self.players["player" + str(i + 1)]["class"].InHand() - 1].image = p
            self.players["player" + str(i + 1)]["cards"][self.players["player" + str(i + 1)]["class"].InHand() - 1].place(x=340 * i + 30, y=400)
            pass

        newCard = Card(self.cardDeck[self.currCardNum])
        self.currCardNum += 1

        self.players["dealer"]["class"].AddCard(newCard)
        p = ImageTk.PhotoImage(file="Resource/GodoriCards/cardback.gif")
        self.players["dealer"]["cards"].append(Label(self.window, image=p))
        self.players["dealer"]["cards"][self.players["dealer"]["class"].InHand() - 1].image = p
        self.players["dealer"]["cards"][self.players["dealer"]["class"].InHand() - 1].place(x=340 * 1 + 30, y=150)
        pass

    def ProgressSecondTurn(self):
        for i in range(3):
            for j in range(3):
                newCard = Card(self.cardDeck[self.currCardNum])
                self.currCardNum += 1
                self.players["player" + str(i + 1)]["class"].AddCard(newCard)

                p = ImageTk.PhotoImage(file=newCard.CardFileName())
                self.players["player" + str(i + 1)]["cards"].append(Label(self.window, image=p))
                self.players["player" + str(i + 1)]["cardsText"].append(self.canvas.create_text((340 * i + 65 + (j + 1) * 50, 380), text=str(newCard.GetPattern()),
                                                                                                font=self.fontMiniStyle, anchor='center', fill='white'))

                self.players["player" + str(i + 1)]["cards"][self.players["player" + str(i + 1)]["class"].InHand() - 1].image = p
                self.players["player" + str(i + 1)]["cards"][self.players["player" + str(i + 1)]["class"].InHand() - 1].place(x=340 * i + 30 + (j + 1) * 50, y=400)
            pass

        for i in range(3):
            newCard = Card(self.cardDeck[self.currCardNum])
            self.currCardNum += 1

            self.players["dealer"]["class"].AddCard(newCard)
            p = ImageTk.PhotoImage(file="Resource/GodoriCards/cardback.gif")
            self.players["dealer"]["cards"].append(Label(self.window, image=p))
            self.players["dealer"]["cards"][self.players["dealer"]["class"].InHand() - 1].image = p
            self.players["dealer"]["cards"][self.players["dealer"]["class"].InHand() - 1].place(x=340 * 1 + 30 + (i + 1) * 50, y=150)
        pass

    def ProgressThirdTurn(self):
        self.TakeLastCard()
        self.OpenDealerCard()
        self.CheckWinner()
        pass

    def TakeLastCard(self):
        for i in range(3):
            newCard = Card(self.cardDeck[self.currCardNum])
            self.currCardNum += 1
            self.players["player" + str(i + 1)]["class"].AddCard(newCard)

            p = ImageTk.PhotoImage(file=newCard.CardFileName())
            self.players["player" + str(i + 1)]["cards"].append(Label(self.window, image=p))
            self.players["player" + str(i + 1)]["cardsText"].append(self.canvas.create_text((340 * i + 65 + 4 * 50, 380), text=str(newCard.GetPattern()),
                                                                                            font=self.fontMiniStyle, anchor='center', fill='white'))

            self.players["player" + str(i + 1)]["cards"][self.players["player" + str(i + 1)]["class"].InHand() - 1].image = p
            self.players["player" + str(i + 1)]["cards"][self.players["player" + str(i + 1)]["class"].InHand() - 1].place(x=340 * i + 30 + 4 * 50, y=400)
        pass

    def OpenDealerCard(self):
        for i in range(4):
            dealerCardsList = self.players["dealer"]["class"].InCards()
            p = ImageTk.PhotoImage(file=dealerCardsList[i].CardFileName())
            self.players["dealer"]["cards"][i].configure(image=p)
            self.players["dealer"]["cards"][i].image = p

            self.players["dealer"]["cardsText"].append(self.canvas.create_text((340 * 1 + 65 + i * 50, 130), text=str(dealerCardsList[i].GetPattern()),
                                                                               font=self.fontMiniStyle, anchor='center', fill='white'))
            pass

        newCard = Card(self.cardDeck[self.currCardNum])
        self.currCardNum += 1

        self.players["dealer"]["class"].AddCard(newCard)
        p = ImageTk.PhotoImage(file=newCard.CardFileName())
        self.players["dealer"]["cards"].append(Label(self.window, image=p))
        self.players["dealer"]["cardsText"].append(self.canvas.create_text((340 * 1 + 65 + 4 * 50, 130), text=str(newCard.GetPattern()),
                                                                           font=self.fontMiniStyle, anchor='center', fill='white'))

        self.players["dealer"]["cards"][self.players["dealer"]["class"].InHand() - 1].image = p
        self.players["dealer"]["cards"][self.players["dealer"]["class"].InHand() - 1].place(x=340 * 1 + 30 + 4 * 50, y=150)
        pass

    def CheckWinner(self):
        # 메인 출력
        for i in range(3):
            text = self.players["player" + str(i + 1)]["class"].GetMainValue()
            rankCardNum = None
            if text == "노 메이드":
                self.players["player" + str(i + 1)]["valueText"].append(self.canvas.create_text((340 * i + 160, 350), text=str(text),
                                                                                                font=self.fontMiniStyle, anchor='center', fill='yellow'))
                pass
            else:
                rankCardNum = copy.copy(self.handRankings[text])
                print(rankCardNum)
                self.players["player" + str(i + 1)]["valueText"].append(self.canvas.create_text((340 * i + 130, 350),
                                                                                                text=str(text) + "(" + str(rankCardNum[0]) + ", " +
                                                                                                     str(rankCardNum[1]) + ", " + str(rankCardNum[2]) + ")",
                                                                                                font=self.fontMiniStyle, anchor='center', fill='yellow'))
                for j in range(5):
                    # print(self.players['player'+str(i + 1)]['class'].InCards()[j].GetPattern())
                    if int(self.players['player' + str(i + 1)]['class'].InCards()[j].GetPattern()) in rankCardNum:
                        self.canvas.delete(self.players["player" + str(i + 1)]["cardsText"][j])
                        self.players["player" + str(i + 1)]["cardsText"][j] = \
                            self.canvas.create_text((340 * i + 65 + j * 50, 390),
                                                    text=str(self.players['player' + str(i + 1)]['class'].InCards()[j].GetPattern()),
                                                    font=self.fontMiniStyle, anchor='center', fill='red')
                        self.players['player' + str(i + 1)]['cards'][j].place(x=340 * i + 30 + j * 50, y=410)
                        rankCardNum.remove(int(self.players['player' + str(i + 1)]['class'].InCards()[j].GetPattern()))
                pass
            pass

        text = self.players['dealer']['class'].GetMainValue()
        rankCardNum = None
        if text == '노 메이드':
            self.players["dealer"]["valueText"].append(self.canvas.create_text((340 * 1 + 160, 100), text=str(text),
                                                                               font=self.fontMiniStyle, anchor='center', fill='yellow'))
            pass
        else:
            rankCardNum = copy.copy(self.handRankings[text])
            self.players["dealer"]["valueText"].append(self.canvas.create_text((340 * 1 + 130, 100),
                                                                               text=str(text) + "(" + str(rankCardNum[0]) + ", " +
                                                                                    str(rankCardNum[1]) + ", " + str(rankCardNum[2]) + ")",
                                                                               font=self.fontMiniStyle, anchor='center', fill='yellow'))
            for j in range(5):
                if int(self.players['dealer']['class'].InCards()[j].GetPattern()) in rankCardNum:
                    self.canvas.delete(self.players["dealer"]["cardsText"][j])
                    self.players["dealer"]["cardsText"][j] = \
                        self.canvas.create_text((340 * 1 + 65 + j * 50, 140),
                                                text=str(self.players['dealer']['class'].InCards()[j].GetPattern()),
                                                font=self.fontMiniStyle, anchor='center', fill='red')
                    self.players['dealer']['cards'][j].place(x=340 * 1 + 30 + j * 50, y=160)
                    rankCardNum.remove(int(self.players['dealer']['class'].InCards()[j].GetPattern()))
            pass
        
        # 서브 출력
        for i in range(3):
            text = self.players["player" + str(i + 1)]["class"].GetSubValue()
            print(text)
            if text:
                self.players["player" + str(i + 1)]["subText"].append(self.canvas.create_text((340 * i + 250, 350), text=str(text),
                                                                                   font=self.fontMiniStyle, anchor='w', fill='black'))
            pass

        text = self.players['dealer']['class'].GetSubValue()
        if text:
            self.players["dealer"]["subText"].append(self.canvas.create_text((340 * 1 + 250, 100), text=str(text),
                                                                             font=self.fontMiniStyle, anchor='w', fill='black'))
        # 승패 출력
        isWin = False
        dealerLevel = self.players['dealer']['class'].GetSubValueLevel()
        for i in range(3):
            level = self.players["player" + str(i + 1)]["class"].GetSubValueLevel()
            if dealerLevel > level:  # 승
                self.players["player" + str(i + 1)]["winText"].append(self.canvas.create_text((340 * i + 160, 290), text="승", font=self.fontBasicStyle, anchor='center', fill="SkyBlue1"))
                self.totalMoney += self.players["player" + str(i + 1)]["betMoney"] * 2
                isWin = True
                pass
            else:
                self.players["player" + str(i + 1)]["winText"].append(self.canvas.create_text((340 * i + 160, 290), text="패", font=self.fontBasicStyle, anchor='center', fill="firebrick1"))
                pass
            pass
        self.canvas.itemconfig(self.totalMoneyText, text=str(self.totalMoney) + "만원")
        if isWin:
            PlaySound('Resource/sounds/win.wav', SND_FILENAME)
        else:
            PlaySound('Resource/sounds/wrong.wav', SND_FILENAME)
        pass

    def PressAgain(self):
        PlaySound('Resource/sounds/ding.wav', SND_FILENAME)

        for i in range(3):
            self.players['player' + str(i + 1)]['betMoney'] = 0
            self.players['player' + str(i + 1)]['class'].ResetCards()

            for j in self.players['player' + str(i + 1)]['cards']:
                j.destroy()
            self.players['player' + str(i + 1)]['cards'].clear()

            for j in self.players['player' + str(i + 1)]['cardsText']:
                self.canvas.delete(j)
                pass
            self.players['player' + str(i + 1)]['cardsText'].clear()

            for j in self.players['player' + str(i + 1)]['valueText']:
                self.canvas.delete(j)
                pass
            self.players['player' + str(i + 1)]['valueText'].clear()

            for j in self.players['player' + str(i + 1)]['subText']:
                self.canvas.delete(j)
                pass
            self.players['player' + str(i + 1)]['subText'].clear()

            for j in self.players['player' + str(i + 1)]['winText']:
                self.canvas.delete(j)
                pass
            self.players['player' + str(i + 1)]['winText'].clear()

            pass

        for i in self.players['dealer']['cards']:
            i.destroy()
        self.players['dealer']['cards'].clear()

        for i in self.players['dealer']['cardsText']:
            self.canvas.delete(i)
            pass
        self.players['dealer']['cardsText'].clear()

        for i in self.players['dealer']['valueText']:
            self.canvas.delete(i)
            pass
        self.players['dealer']['valueText'].clear()

        for i in self.players['dealer']['subText']:
            self.canvas.delete(i)
            pass
        self.players['dealer']['subText'].clear()
        self.players['dealer']['class'].ResetCards()

        self.canvas.itemconfig(self.player1BetMoneyText, text=str(self.players['player1']['betMoney']) + "만")
        self.canvas.itemconfig(self.player2BetMoneyText, text=str(self.players['player2']['betMoney']) + "만")
        self.canvas.itemconfig(self.player3BetMoneyText, text=str(self.players['player3']['betMoney']) + "만")

        self.buttons['again']['state'] = 'disabled'
        self.buttons['again']['bg'] = 'gray'

        self.buttons['deal']['state'] = 'active'
        self.buttons['deal']['bg'] = 'white'

        for i in range(3):
            self.buttons['player' + str(i + 1)]['bet5Button']['state'] = 'active'
            self.buttons['player' + str(i + 1)]['bet5Button']['bg'] = 'white'
            self.buttons['player' + str(i + 1)]['bet1Button']['state'] = 'active'
            self.buttons['player' + str(i + 1)]['bet1Button']['bg'] = 'white'

        self.currCardNum = 0
        pass

    pass


MainGame()
