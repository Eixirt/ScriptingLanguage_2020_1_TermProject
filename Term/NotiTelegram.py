#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import requests
from datetime import date, datetime, timedelta
import traceback

# 경기도 키
key = '2anybj3QVonkHWCDnuvtKc%2BODpt7fk2eYr7bH49dUkB%2BD%2FzHkoXLVTgiJRJJJReH8sKK4S3vUFPQzNQZhQjbXg%3D%3D'
siKey = "3h26d5M7s37jjaUjVQmMPSy%2FIU9swTtAQJ2tM6ZHwkA6aBqZuv1Hban%2B3fB3cRCuVoFzPIMTpjHbjDQN74TGEQ%3D%3D&&&MobileOS=ETC&MobileApp=AppTest&numOfRows=100&areaCode="
landMarkKey = '3h26d5M7s37jjaUjVQmMPSy%2FIU9swTtAQJ2tM6ZHwkA6aBqZuv1Hban%2B3fB3cRCuVoFzPIMTpjHbjDQN74TGEQ%3D%3D&&contentTypeid=15&areaCode=' + str() + "&sigunguCode=" + str() + "&MobileOS=ETC&MobileApp=AppTesting&numOfRows=30&arrange=A"

TOKEN = '1144307322:AAFwG1aQwtRTq1F5Qhit5AeYOfnxbO-ospk'
MAX_MSG_LENGTH = 300

baseurl = 'api.visitkorea.or.kr/openapi/service/rest/KorService/areaCode?serviceKey='
restUrl = 'api.visitkorea.or.kr/openapi/service/rest/KorService/areaBasedList?ServiceKey='

bot = telepot.Bot(TOKEN)

def getData(loc_param):
    res_list = []
    url = "http://" + baseurl + siKey + loc_param+"&"
    #print(url)
    res_body = requests.get(url)
    html = res_body.text

    #print(res_body)
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('name')
    itemCodes = soup.findAll('code')
    for item, itemCode in zip(items, itemCodes):
        print(item.text)
        item = re.sub('<.*?>', '-', item.text)
        itemCode = re.sub('<.*?>', '-', itemCode.text)

        print(item)
        print(type(item))
        parsed = item.split('-')
        parsed.append(itemCode)
        print(parsed)
        try:
            row = "지역: " + parsed[0] + " - 코드: " + parsed[1] +'\n'
        except IndexError:
            row = item.replace('|', ',')

        if row:
            res_list.append(row.strip())
    return res_list


def getData2(loc_param1, loc_param2):
    res_list = []

    url = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaBasedList?ServiceKey=2anybj3QVonkHWCDnuvtKc%2BODpt7fk2eYr7bH49dUkB%2BD%2FzHkoXLVTgiJRJJJReH8sKK4S3vUFPQzNQZhQjbXg%3D%3D&&contentTypeid=15&areaCode=' + str(loc_param1) + '&sigunguCode=' + str(loc_param2) +'&MobileOS=ETC&MobileApp=AppTesting&numOfRows=30&arrange=A'
    #print(url)
    res_body = requests.get(url)
    html = res_body.text

    #print(res_body)
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('title')
    itemCodes = soup.findAll('addr1')
    for item, itemCode in zip(items, itemCodes):
        print(item.text)
        item = re.sub('<.*?>', '-', item.text)
        itemCode = re.sub('<.*?>', '-', itemCode.text)

        print(item)
        print(type(item))
        parsed = item.split('-')
        parsed.append(itemCode)
        print(parsed)
        try:
            row = "랜드마크 이름: " + parsed[0] + " - 구역 " + parsed[1] +'\n'
        except IndexError:
            row = item.replace('|', ',')

        if row:
            res_list.append(row.strip())
    return res_list


def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)


def run(date_param, param='11710'):
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS logs( user TEXT, log TEXT, PRIMARY KEY(user, log) )')
    conn.commit()

    user_cursor = sqlite3.connect('users.db').cursor()
    user_cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    user_cursor.execute('SELECT * from users')

    for data in user_cursor.fetchall():
        user, param = data[0], data[1]
        print(user, date_param, param)
        res_list = getData( param, date_param )
        msg = ''
        for r in res_list:
            try:
                cursor.execute('INSERT INTO logs (user,log) VALUES ("%s", "%s")'%(user,r))
            except sqlite3.IntegrityError:
                # 이미 해당 데이터가 있다는 것을 의미합니다.
                pass
            else:
                print( str(datetime.now()).split('.')[0], r )
                if len(r+msg)+1>MAX_MSG_LENGTH:
                    sendMessage( user, msg )
                    msg = r+'\n'
                else:
                    msg += r+'\n'
        if msg:
            sendMessage( user, msg )
    conn.commit()


if __name__=='__main__':
    today = date.today()
    current_month = today.strftime('%Y%m')

    print( '[',today,']received token :', TOKEN )

    pprint( bot.getMe() )

    run(current_month)
