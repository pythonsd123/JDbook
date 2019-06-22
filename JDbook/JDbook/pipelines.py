# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class JdbookPipeline(object):
    def __init__(self):
        self.conn_pymysql()

    def conn_pymysql(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root',password='123456',
                                 database='jdbook',charset='utf8')
        self.cur = self.conn.cursor()


    def process_item(self, item, spider):
        img = item['img']
        book_name = item['book_name']
        book_href = item['book_href']
        book_author = item['book_author']
        publisher = item['publisher']
        publish_date = item['publish_date']
        b_name = item['b_name']
        b_href = item['b_href']
        s_name = item['s_name']
        s_href = item['s_href']
        price = item['price']
        sql = '''
        insert into jdbook(img,book_name,book_href,book_author,publisher,publish_date,b_name,
        b_href,s_name,s_href,price) VALUES ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}",{})
        '''.format(img,book_name,book_href,book_author,publisher,publish_date,b_name,b_href,s_name,s_href,price)
        try :
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        return item
    def __del__(self):
        self.cur.close()
        self.conn.close()



