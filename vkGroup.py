# -*- coding: utf-8 -*-
import vk
import time
import os
import random
import logging
import re
import threading
import requests
import requests
import six
import json
import urllib.request
import datetime
import emoji

def too_many_rps_handler(dd,timeint,userfilename,token,user_id):

        time.sleep(1)
        return MessageChecker(dd,timeint,userfilename,token,user_id)

def MessageChecker(dd,timeint,userfilename,token,user_id):
    while True:  
        monthtext=''
        writetextattach=''
        dstr=str(dd-1)
        req = urllib.request.Request("https://api.vk.com/method/messages.getHistory?user_id="+user_id+"&v=5.101&offset="+dstr+"&count=1&extended=1&access_token="+token)
        r = urllib.request.urlopen(req).read()
        cont = json.loads(r.decode('utf-8'))
        conterror = r.decode('utf-8')
        if conterror[38:66] == "Too many requests per second":
            too_many_rps_handler(dd,timeint,userfilename,token,user_id)     
        countmessage=cont['response']['count']
        messagetext = cont['response']['items'][0]['text']
        messagedate = cont['response']['items'][0]['date']
        profilename = cont['response']['profiles'][0]['first_name']
        profilelastname = cont['response']['profiles'][0]['last_name']
        profileid = cont['response']['profiles'][0]['id']
        profileshorturl = cont['response']['profiles'][0]['screen_name']
        profilephoto = cont['response']['profiles'][0]['photo_100']
        #checkgeo = cont['response']['items'][0]['geo']
       # geolat = cont['response']['items'][0]['geo']['coordinates']['latitude']
       # geolong = cont['response']['items'][0]['geo']['coordinates']['longitude']
        if len(cont['response']['items'][0]['attachments']) != 0:
            attachtype = cont['response']['items'][0]['attachments'][0]['type']
            if attachtype == "sticker":
                attachsticker = cont['response']['items'][0]['attachments'][0]['sticker']['images'][4]['url']
                writetextattach="----------[STICKER]\n--{url:"+attachsticker+"}"
            if attachtype == "video":
                attachvideotitle = cont['response']['items'][0]['attachments'][0]['video']['title']
                attachvideoimage = cont['response']['items'][0]['attachments'][0]['video']['image'][0]['url']
                attachvideodurationint = cont['response']['items'][0]['attachments'][0]['video']['duration']
                attachvideoduration = str(attachvideodurationint)
                writetextattach="----------[VIDEO]\n---{Title:"+attachvideotitle+"}\n---{Image:"+attachvideoimage+"}\n---{Duartion:"+attachvideoduration+"}"
            if attachtype == "doc":
                attachdocurl = cont['response']['items'][0]['attachments'][0]['doc']['url']
                writetextattach="----------[DOCUMENT]\n--{url:"+attachdocurl+"}"
            if attachtype == "graffiti":
                attachgraffitiurl = cont['response']['items'][0]['attachments'][0]['graffiti']['url']
                writetextattach="----------[GRAFFITI]\n--{url:"+attachgraffitiurl+"}"
            if attachtype == "audio_message":
                attachaudiomessageurl = cont['response']['items'][0]['attachments'][0]['audio_message']['link_mp3']
                writetextattach="----------[AUDIO_MESSAGE]\n--{url:"+attachaudiomessageurl+"}"
            if attachtype == "audio":
                attachauidoartist = cont['response']['items'][0]['attachments'][0]['audio']['artist']
                attachauidoname = cont['response']['items'][0]['attachments'][0]['audio']['title']
                attachauidurl = cont['response']['items'][0]['attachments'][0]['audio']['url']
                writetextattach="----------[AUDIO]\n--{url:"+attachauidurl+"\n---{Artist:"+attachauidoartist+"}\n---{Title:"+attachauidoname+"}"
            if attachtype == "photo":
                attachphotourl = cont['response']['items'][0]['attachments'][0]['photo']['sizes'][4]['url']
                writetextattach="----------[PHOTO]\n--{url:"+attachphotourl+"}"        	
        timestamp = datetime.datetime.fromtimestamp(messagedate).isoformat()
        yearandmonth = timestamp.split('-')
        dayandtime = yearandmonth[2].split('T')
        if yearandmonth[1] == '01':
            monthtext=" Января "
        if yearandmonth[1] == '02':
            monthtext=" Февраля "
        if yearandmonth[1] == '03':
            monthtext=" Марта "
        if yearandmonth[1] == '04':
            monthtext=" Апреля "
        if yearandmonth[1] == '05':
            monthtext=" Мая "
        if yearandmonth[1] == '06':
            monthtext=" Июня "
        if yearandmonth[1] == '07':
            monthtext=" Июля "
        if yearandmonth[1] == '08':
            monthtext=" Августа "
        if yearandmonth[1] == '09':
            monthtext=" Сентября "
        if yearandmonth[1] == '10':
            monthtext=" Октября "
        if yearandmonth[1] == '11':
            monthtext=" Ноября "
        if yearandmonth[1] == '12':
            monthtext=" Декабря "
        dds=str(dd)
        datetext=dayandtime[0]+monthtext+yearandmonth[0]+" ["+dayandtime[1]+"]"
        fulltext=emoji.demojize("________________________________________________________________________\n"+dds+' Сообщение / '+datetext+"\n\n"+profilename+" "+profilelastname+": "+messagetext+"\n"+writetextattach+"\n")
        if dd == 1:
            profileid=str(profileid)
            fulltext="____________________________________\nИмя:"+profilename+"\nФамилия:"+profilelastname+"\nКороткая ссылка:vk.com/"+profileshorturl+"\nid:"+profileid+"\nФото:"+profilephoto+"\n____________________________________\n\n\n"+fulltext    
        percentint=dd/countmessage*100
        if dd == 1:
            timeint=countmessage/3
        if dd % 3 == 0:
          timeint-=1
        timestr=str(timeint) 
        percent=str(percentint)
        print(str(dd)+'/'+str(countmessage)+'('+percent[0:3]+'%)               '+timestr.split('.')[0]+' секунд')
        file = open(userfilename+".txt",'a')
        file.write(fulltext)
        file.close()
        dd+=1
userfilename = input("Введите имя файла:")
user_id = input("Введите id пользователя:")
token = input("Введите ваш access_token:")
timeint=1
dd=1
MessageChecker(dd,timeint,userfilename,token,user_id)