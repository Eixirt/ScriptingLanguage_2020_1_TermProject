from KoreanBlackJackCard import *
import copy

tier1 = [[1, 1, 8], [1, 2, 7], [1, 3, 6], [1, 4, 5], [1, 9, 10]]  # 콩콩팔/삐리칠/물삼육/빽새오/삥구장
tier2 = [[2, 2, 6], [2, 3, 5], [2, 8, 10]]  # 니니육/이삼오/이판장
tier3 = [[3, 3, 4], [3, 7, 10], [3, 8, 9]]  # 심심새/삼칠장/삼빡구
tier4 = [[4, 4, 2], [4, 6, 10], [4, 7, 9]]  # 살살이/사륙장/사칠구
tier5 = [[5, 5, 10], [5, 6, 9], [5, 7, 8]]  # 꼬꼬장/오륙구/오리발
tier6 = [[6, 6, 8]]  # 쭉쭉팔
tier7 = [[7, 7, 6]]  # 철철육
tier8 = [[8, 8, 4]]  # 팍팍싸
tier9 = [[9, 9, 2]]  # 구구리
tierList = [tier1, tier2, tier3, tier4, tier5, tier6, tier7, tier8, tier9]
tierNameList = [
    ["콩콩팔", "삐리칠", "물삼육", "빽새오", "삥구장"],
    ["니니육", "이삼오", "이판장"],
    ["심심새", '삼칠장', '삼빡구'],
    ['살살이', '사륙장', '사칠구'],
    ['꼬꼬장', '오륙구', '오리발'],
    ['쭉쭉팔'],
    ['철철육'],
    ['팍팍싸'],
    ['구구리']
]

subTier = ["38광땡",
           "18광땡", "13광땡",
           "장땡", "땡", "삥땡",
           "끗", "망통"]

subTierLevelDic = {"38광땡": 0,
                   "18광땡": 1, "13광땡": 1.1,
                   "장땡": 2, "9땡": 2.1, "8땡": 2.2, "7땡": 2.3, "6땡": 2.4, "5땡": 2.5, "4땡": 2.6, "3땡": 2.7, "2땡": 2.8, "삥땡": 2.9,
                   "9끗": 3, "8끗": 3.1, "7끗": 3.2, "6끗": 3.3, "5끗": 3.4, "4끗": 3.5, "3끗": 3.6, "2끗": 3.7, "1끗": 3.8,
                   "망통": 5}


class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.N = 0

        self.mainValue = []  # 메인 족보
        self.mainValueNum = []

        self.subValue = None  # 자투리 값
        self.subValueNum = []
        self.subValueLevel = 10000

    def InHand(self):
        return self.N

    def AddCard(self, c):
        self.cards.append(c)
        self.N += 1

    def InCards(self):
        return self.cards

    def ResetCards(self):
        self.N = 0
        self.cards.clear()

        self.mainValue = []  # 메인 족보
        self.mainValueNum = []

        self.subValue = None  # 자투리 값
        self.subValueNum = []
        self.subValueLevel = 10000

    def GetMainValue(self):
        tierScore = 0
        holdingTierCardsIndex = []  # 티어에 속한다면 속하는 카드들의 인덱스를 담아주는 리스트

        cardPatterns = []  # 현재 들고 있는 카드의 월을 표기하는 리스트
        for j in self.cards:
            cardPatterns.append(int(j.GetPattern()))
            pass

        for tier in tierList:
            tierScore += 1  # 1...9 티어
            for index, i in enumerate(tier):
                # print(i) 리스트 하나씩 꺼내옴
                copiedCardPatterns = copy.copy(cardPatterns)

                tierResult = [k for k in i if not k in copiedCardPatterns or copiedCardPatterns.remove(k)]  # tier - cardPatterns == [] 일 경우
                # print(tierResult)
                # print(i)
                # print("=================")
                if not tierResult:  # tierResult 가 [] 이면
                    self.mainValueNum.append(i)
                    tierValue = tierScore + 0.1 * (index + 1)
                    self.mainValue.append(tierValue)
                    pass
                pass
        pass
        # print("data: " + str(self.mainValue))
        if not self.mainValue:
            self.mainValue = "노 메이드"
            pass
        else:
            # 제일 최고 조합을 찾아야한다 sub 중에서
            self.FindSubValue()

            # self.mainValue = tierNameList[int(self.mainValue % 10) - 1][int(self.mainValue * 10 % 10) - 1]
            pass
        return self.mainValue

    def FindSubValue(self):
        cardPatterns = []
        for j in self.cards:
            cardPatterns.append(int(j.GetPattern()))
            pass

        count = 0
        valX = None
        valY = None

        for i in self.mainValueNum:
            copiedCardPatterns = copy.copy(cardPatterns)
            copiedValue = copy.copy(i)

            tierResult = [k for k in copiedCardPatterns if not k in copiedValue or copiedValue.remove(k)]

            tierResult.sort()

            currSubValue = 10
            subValue = None

            if tierResult == [3, 8]:
                subValue = subTier[0]
            elif tierResult == [1, 8]:
                subValue = subTier[1]
            elif tierResult == [1, 3]:
                subValue = subTier[2]
            elif tierResult[0] == tierResult[1]:
                if tierResult[0] == 10:
                    subValue = subTier[3]
                elif tierResult[0] == 1:
                    subValue = subTier[5]
                else:
                    subValue = str(tierResult[0]) + subTier[4]
                pass
            else:
                tierResultSum = tierResult[0] + tierResult[1]
                newTierResultSum = tierResultSum % 10

                if newTierResultSum == 0:
                    subValue = subTier[7]
                else:
                    subValue = str(newTierResultSum) + subTier[6]

            if currSubValue > subTierLevelDic[subValue]:
                currSubValue = subTierLevelDic[subValue]
                self.subValue = subValue
                self.subValueNum = tierResult

                print("1:" + str(self.mainValue))
                print("2:" + str(self.mainValue[count]))

                valX = int(self.mainValue[count]) % 10 - 1
                print(valX)

                valY = int(float(self.mainValue[count]) * 10 % 10) - 1
                print(valY)

            count += 1
        self.mainValue = tierNameList[valX][valY]
        self.subValueLevel = currSubValue
        pass

    def GetSubValue(self):
        return self.subValue

    def GetSubValueLevel(self):
        return self.subValueLevel
    pass

