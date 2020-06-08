class TourInfo:
    def __init__(self, iter):
        if iter.find("title") != None: #이름
            self.title =iter.find("title").text
        if iter.find("tel") != None: #전화번호
            self.telephone =iter.find("tel").text
        if iter.find("mapx") != None: #x좌표
            self.x = iter.find("mapx").text
        if iter.find("mapy") != None: #y좌표
            self.y = iter.find("mapy").text
        if iter.find("readcount") != None: #조회수
            self.readcount = iter.find("readcount").text
        if iter.find("firstimage") != None: #대표이미지
            self.image = iter.find("firstimage").text
        if iter.find("addr1") != None: #주소
            self.addr1 = iter.find("addr1").text
        if iter.find("addr2") != None: #상세주소
            self.addr2 = iter.find("addr2").text
