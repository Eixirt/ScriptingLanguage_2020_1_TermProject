import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback

import NotiTelegram


def replyAptData(user, loc_param):
    print(user, loc_param)
    res_list = NotiTelegram.getData( loc_param )
    msg = ''
    for r in res_list:
        print( str(datetime.now()).split('.')[0], r )
        if len(r+msg)+1>NotiTelegram.MAX_MSG_LENGTH:
            NotiTelegram.sendMessage( user, msg )
            msg = r+'\n'
        else:
            msg += r+'\n'
    if msg:
        NotiTelegram.sendMessage( user, msg )
    else:
        NotiTelegram.sendMessage( user, '해당하는 데이터가 없습니다.' )


def replyLandMarkData(user, loc_param1, loc_param2):
    print(user, loc_param1, loc_param2)
    res_list = NotiTelegram.getData2(loc_param1, loc_param2)
    msg = ''
    for r in res_list:
        print( str(datetime.now()).split('.')[0], r )
        if len(r+msg)+1>NotiTelegram.MAX_MSG_LENGTH:
            NotiTelegram.sendMessage( user, msg )
            msg = r+'\n'
        else:
            msg += r+'\n'
    if msg:
        NotiTelegram.sendMessage( user, msg )
    else:
        NotiTelegram.sendMessage( user, '해당하는 데이터가 없습니다.' )


def save( user, loc_param ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    try:
        cursor.execute('INSERT INTO users(user, location) VALUES ("%s", "%s")' % (user, loc_param))
    except sqlite3.IntegrityError:
        NotiTelegram.sendMessage( user, '이미 해당 정보가 저장되어 있습니다.' )
        return
    else:
        NotiTelegram.sendMessage( user, '저장되었습니다.' )
        conn.commit()


def check(user):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    cursor.execute('SELECT * from users WHERE user="%s"' % user)
    for data in cursor.fetchall():
        row = 'id:' + str(data[0]) + ', location:' + data[1]
        NotiTelegram.sendMessage( user, row )


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        NotiTelegram.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')

    if text.startswith('시') and len(args)>1:
        print('try to 시', args[1])
        replyAptData(chat_id, args[1])
    elif text.startswith('지역') and len(args)>2:
        print('try to 지역', args[1], args[2])
        replyLandMarkData(chat_id, args[1], args[2])
    elif text.startswith('저장') and len(args)>1:
        print('try to 저장', args[1])
        save(chat_id, args[1])
    elif text.startswith('확인'):
        print('try to 확인')
        check( chat_id )
    else:
        NotiTelegram.sendMessage(chat_id, '모르는 명령어입니다.\n시 [시/도 번호], 지역 [시/도 번호] [지역번호] 중 하나의 명령을 입력하세요. \n'
                                          '=========================================================\n'
                                          '서울 : 1, 인천 : 2, 대전 : 3, 대구 : 4, 광주 : 5, 부산 : 6, 울산 : 7, 세종특별자치시 : 8, 경기도 : 31, 강원도 : 32,'
                                          ' 충청북도 : 33, 충청남도 : 34, 경상북도 : 35, 경상남도 : 36, 전라북도 : 37, 전라남도 : 38, 제주도 : 39')


def StartTelegram():

    today = date.today()
    current_month = today.strftime('%Y%m')

    print('[', today, ']received token :', NotiTelegram.TOKEN)

    bot = telepot.Bot(NotiTelegram.TOKEN)
    pprint( bot.getMe() )

    bot.message_loop(handle)

    print('Listening...')

    while 1:
      time.sleep(10)
      yield None