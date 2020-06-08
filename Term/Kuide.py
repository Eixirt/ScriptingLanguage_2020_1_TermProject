from tkinter import *
from tkinter import ttk #combobox 용

import OpenApiDo
import OpenApiSigungu

class MainGUI:
    def SendEmail(self): #이메일 전송
        pass
    
    def CheckBookmark(self): #북마크 버튼눌렀을 때/
        pass

    def Bookmark(self): #북마크 띄우기
        self.bookmark['state'] = DISABLED
        self.information['state'] = NORMAL
        #canvas 초기화하고 book리스트보여주기

    def Information(self): # 정보 띄우기
        self.bookmark['state'] = NORMAL
        self.information['state'] = DISABLED
        # canvas 초기화하고 Info리스트보여주기

    def InitInsert(self): #지역들 xml로부터 읽어와 combobox에 넣어주기 self.do, self.city
        dolist = ['경기도','강원도','충청북도','충청남도','전라북도',
                  '전라남도','경상북도','경상남도', '서울','제주도',
                  '부산','대구','인천','광주','대전','울산','세종특별자치시']

        self.do['value'] = dolist
        self.do.current(0)

    def Refresh(self): # 관광지 리스트박스에서 선택 후 누르면 정보 창의 정보 갱신
        pass

    def Search(self): #combobox로부터 선택된 값을 얻어와 해당 지역의 관광지를 listbox로 뽑음
        #리스트 박스에 해당 지역의 유명 관광지 xml로부터 이름 불러와 insert
        DoCode = OpenApiDo.getSidoCode(self.do.get())
        SigunguCode = OpenApiSigungu.getSigunguCode(self.city.get())

    def ChangeDo(self,event): #Do 콤보박스 내용 바꿨을 때-> 시군구 콤보박스 내용 바꾸기
        code = OpenApiDo.getSidoCode(self.do.get())
        self.city['value'] = OpenApiSigungu.getSigunguList(code)
        self.city.current(0)

    def __init__(self):
        self.window = Tk()
        self.window.iconbitmap("Resource/Kuide.ico")
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
        self.do.bind("<<ComboboxSelected>>", self.ChangeDo)

        Button(self.window,text = "검색",bg = "pale violet red", command = self.Search).place(x = 360, y = 77) #지역 검색 버튼
        Button(self.window,text = "갱신", bg ="pale violet red", command = self.Refresh).place(x = 400, y= 77) #관광지 선택시 관광지 정보 갱신

        self.TouristDestination = Listbox(self.window, selectmode = 'multiple', width = 60, height= 30) #관광지 리스트
        self.TouristDestination.place(x= 20, y = 120)
        self.information = Button(self.window, text = "정보", bg = "pink", width = 8, command = self.Information) #정보 버튼
        self.information.place(x =  500, y =95)
        self.bookmark = Button(self.window, text = "북마크", bg = "pink", width = 8, command = self.Bookmark) #북마크 버튼
        self.bookmark.place(x = 568, y=95)

        self.InfoandbookmarkList = Listbox(self.window, selectmode = 'multiple', width = 60, height = 15)#정보,북마크버튼 및의 정보 띄워주는 창
        self.InfoandbookmarkList.place(x = 500, y = 120)

        self.Picture = Canvas(self.window, width = 420, height = 210) #관광지 이미지
        self.Picture.place(x = 500, y =  390)

        Label(self.window, text= "지도",bg= "light pink").place(x =  950, y =95)
        self.Map = Canvas(self.window, width = 300, height = 450) #지도
        self.Map.place(x = 950, y = 120)

        #0601추가_북마크버튼
        self.PhotoBookmark = PhotoImage(file='Resource/BookmarkButton.png')
        Button(self.window, image = self.PhotoBookmark, command = self.CheckBookmark, bg = "pink").place(x = 840, y=85)

        #0601추가_이메일전송버튼
        self.PhotoEmail = PhotoImage(file='Resource/Email.png')
        Button(self.window, image = self.PhotoEmail, command = self.SendEmail, bg = "pink").place(x = 880, y = 85)

        self.window.mainloop()

MainGUI()