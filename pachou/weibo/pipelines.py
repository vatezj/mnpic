# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import random
import os
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from aip import AipFace
import base64
import mysql.connector

APP_ID = '17174146'
API_KEY = 'MyKcGkviUKBQCpZGhOkFoX2L'
SECRET_KEY = 'vtt8kak80lFhYRNtpBaq9jWmCvvgBRlo'

APP_ID1 = '17181482'
API_KEY1 = 'rsS6060o13VBfZZ6fwATnHVH'
SECRET_KEY1 = 'DtmNEpfirwfOrD42YSLtcRlZfX7pNwZe'
class WeiboPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        url = item['image_urls']
        USER_AGENT_LIST = [
            'MSIE (MSIE 6.0; X11; Linux; i686) Opera 7.23',
            'Opera/9.20 (Macintosh; Intel Mac OS X; U; en)',
            'Opera/9.0 (Macintosh; PPC Mac OS X; U; en)',
            'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
            'Mozilla/4.76 [en_jp] (X11; U; SunOS 5.8 sun4u)',
            'iTunes/4.2 (Macintosh; U; PPC Mac OS X 10.2)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0) Gecko/20100101 Firefox/5.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0) Gecko/20100101 Firefox/9.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:16.0) Gecko/20120813 Firefox/16.0',
            'Mozilla/4.77 [en] (X11; I; IRIX;64 6.5 IP30)',
            'Mozilla/4.8 [en] (X11; U; SunOS; 5.7 sun4u)'
        ]
        # 随机生成user agent
        USER_AGENT = random.choice(USER_AGENT_LIST)
        headers = {
            'Referer': "http://www.umei.cc/",
            'User-Agent': USER_AGENT,
        }
        conn = mysql.connector.connect(host='127.0.0.1', user='root', password='root', database='bigdata')
        db = conn
        cursor = db.cursor()
        sql = "SELECT * from pic where img_url = %s LIMIT 1"
        val = (url,)
        cursor.execute(sql, val)
        myresult = cursor.fetchone()
        cursor.close()
        if myresult:
            return item
        else:
            yield Request(url, headers=headers)

    def item_completed(self, results, item, info):
        print(item)
        print('thisis pix')
        conn = mysql.connector.connect(host='127.0.0.1', user='root', password='root', database='bigdata')
        db = conn
        image_paths = [x['path'] for ok, x in results if ok]  # ok判断是否下载成功
        if not image_paths:
            raise DropItem("Item contains no images")
        # item['image_paths'] = image_paths
        else:
            print('dowok')
            for ok, x in results:
                path = x['path']
            rootpath = os.path.abspath('..')
            filePath = rootpath + "\\images\\"+path
            print(filePath)
            aipFace = AipFace(APP_ID, API_KEY, SECRET_KEY)
            imageType = "BASE64"
            options = {}
            options["face_field"] = "age,gender,beauty"
            with open(filePath, 'rb') as fp:
                content = base64.b64encode(fp.read())
                base64ss =  content.decode('utf-8')
            result = aipFace.detect(base64ss, imageType, options)
            beauty = 0
            if result['error_code'] == 0:
                face = result['result']['face_list']
                beauty = face[len(face)-1]['beauty']
            elif  result['error_code']==18:
                aipFace1 = AipFace(APP_ID1, API_KEY1, SECRET_KEY1)
                result1 = aipFace1.detect(base64ss, imageType, options)
                if result1['error_code'] == 0:
                    face = result1['result']['face_list']
                    beauty = face[len(face) - 1]['beauty']
            img_url = item['image_urls']
            type = 1
            cursor = db.cursor()
            sql = "INSERT INTO pic (img_url,`type`,beauty) VALUES (%s,%s,%s)"
            val = (img_url,type,beauty)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            print("1 条记录已插入, ID:", cursor.lastrowid)

        return item

    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            content = base64.b64encode(fp.read())
            return content.decode('utf-8')




