class Card:
    def __init__(self, temp):  # 0...39 -> 1...40
        self.cardValue = temp % 4 + 1  # 월 중에서 몇 번째 카드인지
        self.x = temp // 4  # 월
        self.cardType = None
        self.cardPattern = None
        pass

    def GetValue(self):
        return self.cardValue
        pass

    def GetPattern(self):
        self.cardPattern = str(self.x + 1)
        return self.cardPattern

    def CardFileName(self):
        return "Resource/GodoriCards/" + str(self.GetPattern()) + "." + str(self.cardValue) + ".gif"
        pass

    pass

