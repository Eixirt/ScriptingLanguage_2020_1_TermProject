# http://api.visitkorea.or.kr/openapi/service/rest/KorService/searchStay?serviceKey=2anybj3QVonkHWCDnuvtKc%2BODpt7fk2eYr7bH49dUkB%2BD%2FzHkoXLVTgiJRJJJReH8sKK4S3vUFPQzNQZhQjbXg%3D%3D&numOfRows=10&pageNo=1&MobileOS=ETC&MobileApp=AppTest&arrange=A&listYN=Y&areaCode=&sigunguCode=&hanOk=&benikia=&goodStay=&modifiedtime=&

import urllib
import http.client
from xml.etree import ElementTree

numOfRows = 10
currPage = 1

conn = http.client.HTTPConnection("api.visitkorea.or.kr")
conn.request("GET", "/openapi/service/rest/KorService/searchStay?serviceKey=2anybj3QVonkHWCDnuvtKc%2BODpt7fk2eYr7bH49dUkB%2BD%2FzHkoXLVTgiJRJJJReH8sKK4S3vUFPQzNQZhQjbXg%3D%3D&"
                    "numOfRows=" + str(numOfRows) + "&pageNo=" + str(currPage) + "&MobileOS=ETC&MobileApp=AppTest&arrange=A&listYN=Y&areaCode=&sigunguCode=&"
                                                                                 "hanOk=&benikia=&goodStay=&modifiedtime=&")


req = conn.getresponse()
print(req.status, req.reason)

hotelListsDataTree = ElementTree.fromstring(req.read().decode('utf-8'))
hotelList = hotelListsDataTree.getiterator("item")

# print(req.read().decode('utf-8'))
print(hotelList)
address = [x.findtext("addr1") for x in hotelList]

print(address)
