# http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaBasedList?ServiceKey=인증키&contentTypeid=15&areaCode=4&sigunguCode=4&MobileOS=ETC&MobileApp=AppTesting
import urllib
import http.client
from xml.etree import ElementTree

#서비스키: 3h26d5M7s37jjaUjVQmMPSy%2FIU9swTtAQJ2tM6ZHwkA6aBqZuv1Hban%2B3fB3cRCuVoFzPIMTpjHbjDQN74TGEQ%3D%3D


# 지역 검색했을 때 리스트로 반환
def getTouristList(Docode, Sigungu):
    conn = http.client.HTTPConnection("api.visitkorea.or.kr")
    conn.request("GET","/openapi/service/rest/KorService/areaBasedList?ServiceKey=3h26d5M7s37jjaUjVQmMPSy%2FIU9swTtAQJ2tM6ZHwkA6aBqZuv1Hban%2B3fB3cRCuVoFzPIMTpjHbjDQN74TGEQ%3D%3D&contentTypeid=15&areaCode="+ str(Docode) +"&sigunguCode=" +str(Sigungu) + "&MobileOS=ETC&MobileApp=AppTesting&numOfRows=30&arrange=A")
    res = conn.getresponse()
    # print(res.read().decode('utf-8'))
    tree = ElementTree.fromstring(res.read().decode('utf-8'))

    itemElement = tree.getiterator("item")
    tourist = []
    for item in itemElement:
        tname = item.find("title").text
        tourist.append(tname)

    return tourist


# 관광지 클릭했을 때
def getTouristInfo(Docode, Sigungu, Ttitle):
    conn = http.client.HTTPConnection("api.visitkorea.or.kr")
    conn.request("GET","/openapi/service/rest/KorService/areaBasedList?ServiceKey=3h26d5M7s37jjaUjVQmMPSy%2FIU9swTtAQJ2tM6ZHwkA6aBqZuv1Hban%2B3fB3cRCuVoFzPIMTpjHbjDQN74TGEQ%3D%3D&contentTypeid=15&areaCode=" + str(Docode) + "&sigunguCode=" + str(Sigungu) + "&MobileOS=ETC&MobileApp=AppTesting&numOfRows=30&arrange=A")
    res = conn.getresponse()
    # print(res.read().decode('utf-8'))
    tree = ElementTree.fromstring(res.read().decode('utf-8'))
    itemElement = tree.getiterator("item")

    for item in itemElement:
        if Ttitle == item.find('title').text:
            # print(item.find('title').text)
            return item