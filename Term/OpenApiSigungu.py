import urllib
import http.client
from xml.etree import ElementTree

#지역정보
#/openapi/service/rest/KorService/areaCode?serviceKey=3h26d5M7s37jjaUjVQmMPSy%2FIU9swTtAQJ2tM6ZHwkA6aBqZuv1Hban%2B3fB3cRCuVoFzPIMTpjHbjDQN74TGEQ%3D%3D&numOfRows=10&pageNo=1&MobileOS=ETC&MobileApp=AppTest&areaCode=1&
def getSigunguList(Docode):
    conn = http.client.HTTPConnection("api.visitkorea.or.kr")
    conn.request("GET","/openapi/service/rest/KorService/areaCode?serviceKey=2anybj3QVonkHWCDnuvtKc%2BODpt7fk2eYr7bH49dUkB%2BD%2FzHkoXLVTgiJRJJJReH8sKK4S3vUFPQzNQZhQjbXg%3D%3D&&&MobileOS=ETC&MobileApp=AppTest&numOfRows=100&areaCode=" + str(Docode) +"&")
    res = conn.getresponse()

    tree = ElementTree.fromstring(res.read().decode('utf-8'))

    itemElement = tree.getiterator("item")
    sigungulist = []
    for item in itemElement:
        sigunguname =  item.find("name").text
        sigungulist.append(sigunguname)

    return sigungulist

def getSigunguCode(sigungu, Docode):
    conn = http.client.HTTPConnection("api.visitkorea.or.kr")
    conn.request("GET","/openapi/service/rest/KorService/areaCode?serviceKey=2anybj3QVonkHWCDnuvtKc%2BODpt7fk2eYr7bH49dUkB%2BD%2FzHkoXLVTgiJRJJJReH8sKK4S3vUFPQzNQZhQjbXg%3D%3D&&MobileOS=ETC&MobileApp=AppTest&numOfRows=100&areaCode=" + str(Docode))
    res = conn.getresponse()

    tree = ElementTree.fromstring(res.read().decode('utf-8'))

    itemElement = tree.getiterator("item")
    for item in itemElement:
        if item.find("name").text == sigungu:
            return item.find("code").text