from tkinter import *
from tkinter import ttk #combobox 용

class MainGUI:
    def Bookmark(self): #북마크 띄우기
        self.bookmark['state'] = DISABLED
        self.information['state'] = NORMAL
        #canvas 초기화하고 book리스트보여주기

    def Information(self): # 정보 띄우기
        self.bookmark['state'] = NORMAL
        self.information['state'] = DISABLED
        # canvas 초기화하고 Info리스트보여주기

    def InitInsert(self): #지역들 xml로부터 읽어와 combobox에 넣어주기 self.do, self.city
        pass

    def Search(self): #combobox로부터 선택된 값을 얻어와 해당 지역의 관광지를 listbox로 뽑음
        pass

    def __init__(self):
        self.window = Tk()
        self.window.iconbitmap("Kuide.ico")
        self.window.title("Kuide")
        self.window.geometry('1280x720')
        self.window.configure(bg= "light pink")

        Label(self.window, text = "도",bg= "light pink").place(x = 20, y = 50) #충청남도 할때 도
        Label(self.window, text = "시/군/구",bg= "light pink").place(x= 130, y = 50) #시,군,구
        self.do = ttk.Combobox(self.window, width = 8) #도 선택 버튼
        self.do.place(x = 20, y = 80)
        self.city = ttk.Combobox(self.window, width = 10) # 시/군/구 선택버튼
        self.city.place(x = 130, y = 80)
        self.InitInsert() # 선택창에 지역 넣어주기

        Button(self.window,text = "검색",bg = "pale violet red", command = self.Search).place(x = 410, y = 77)

        self.TouristDestination = Listbox(self.window, selectmode = 'multiple', width = 60, height= 30)
        self.TouristDestination.place(x= 20, y = 120)
        self.information = Button(self.window, text = "정보", bg = "pink", width = 8, command = self.Information)
        self.information.place(x =  500, y =95)
        self.bookmark = Button(self.window, text = "북마크", bg = "pink", width = 8, command = self.Bookmark)
        self.bookmark.place(x = 568, y=95)

        self.InfoandbookmarkList = Listbox(self.window, selectmode = 'multiple', width = 60, height = 15)
        self.InfoandbookmarkList.place(x = 500, y = 120)

        self.picture = Canvas(self.window, width = 420, height = 210) #관광지 이미지
        self.picture.place(x = 500, y =  390)

        Label(self.window, text= "지도",bg= "light pink").place(x =  950, y =95)
        self.map = Canvas(self.window, width = 300, height = 450) #지도
        self.map.place(x = 950, y = 120)

        self.window.mainloop()

MainGUI()