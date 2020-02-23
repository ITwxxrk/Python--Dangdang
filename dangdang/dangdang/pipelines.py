# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

def condb():
    conn = pymysql.connect(host='localhost',port=3306,user='root',password='cxks20121221!',db='dangdang',charset='utf8mb4')
    return conn

class DangdangPipeline(object):
    def process_item(self, item, spider):
        dbObject = condb()
        cursor = dbObject.cursor()
        sql = 'INSERT INTO products(shop,title,link,price,comment) VALUES(%s,%s,%s,%s,%s)'
        # 将数据导入到本地数据库中
        for j in range(len(item['title'])):
            try:
                cursor.execute(sql,(item['shop'][j],item['title'][j],item['link'][j],item['price'][j],item['comment'][j],))
                cursor.close()
                dbObject.commit()
            except Exception as e:
                print(e)
                dbObject.rollback()
        return item