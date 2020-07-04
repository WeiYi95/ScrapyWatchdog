# -*- coding:utf-8 -*-
# @Author: Wei Yi

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import urllib.request
import os
class SbookPipeline(object):

    def process_item(self, item, spider):
        if "book_info" in item.keys():
            path,file_name = self.getDir(item["book_info"])
            file = path + '\\' + file_name + ".txt"
            with open(file,'w',encoding="utf-8") as tfile:
                tfile.write(item["text"] + '\n')
                tfile.write(item["book_info"] + '\t' + item["text"] + '\t' + item["url"] + '\t' + item["img_url"] + '\n')
            with open("record.txt", 'a', encoding="utf-8") as rfile:
                rfile.write(item["url"] + '\n')
        elif "img_info" in item.keys():
            path, file_name = self.getDir(item["img_info"])
            file = path + '\\' + file_name + ".png"
            try:
                reader = urllib.request.urlopen(item["image_url"],timeout=10)
                byte = reader.read()
                with open(file, 'wb') as ifile:
                    ifile.write(byte)
            except:
                pass
        else:
            path = "SK_BOOK\\图片字"
            if (not (os.path.exists(path))):
                os.mkdir(path)
            name = item["image_url"].replace("http://siku.guoxuedashi.com/ziimg/images/","")
            path = path + "\\" + name
            try:
                wreader = urllib.request.urlopen(item["image_url"],timeout=10)
                byte = wreader.read()
                with open(path, 'wb') as zifile:
                    # if (not (os.path.exists(path))):
                    zifile.write(byte)
            except:
                pass


    def getDir(self,s):
        pre = "SK_BOOK"
        if (not (os.path.exists(pre))):
            os.mkdir(pre)
        list = s.split("~")
        #address = "\\".join(list[:-1])
        path = pre
        for i in range(0,len(list)-1):
            path = path + "\\" + list[i]
            if (not (os.path.exists(path))):
                os.mkdir(path)
        file_name = s.replace("~","_")
        return path,file_name