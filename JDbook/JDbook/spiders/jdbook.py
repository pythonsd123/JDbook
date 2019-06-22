# -*- coding: utf-8 -*-
import scrapy
from JDbook.items import JdbookItem
import re
import json

class JdbookSpider(scrapy.Spider):
    name = 'jdbook'
    # allowed_domains = ['jindong.com']
    start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):

        # 获取图书的每个大类
        dt_list = response.xpath('//div[@class="mc"]/dl/dt')
        for dt in dt_list:
            # 获取大分类的名字和url
            b_name = dt.xpath('./a/text()').extract_first()
            b_href = dt.xpath('./a/@href').extract_first()
            b_href = 'https:'+b_href
            # 获取小分类的名字和url
            em_list = dt.xpath('./following-sibling::dd[1]/em')
            # 获取小分类的名字和url,包含在em中
            for em in em_list:
                s_name = em.xpath('./a/text()').extract_first()
                s_href = em.xpath('./a/@href').extract_first()
                s_href = 'https:'+s_href
                item =JdbookItem()
                item['b_name'] = b_name
                item['b_href'] = b_href
                item['s_name'] = s_name
                item['s_href'] = s_href
                yield scrapy.Request(url=s_href, callback=self.parse_book,meta={'data':item},dont_filter=True)
                break
    # 进入每个类型图书页面
    def parse_book(self,response):
        # print(response.body.decode('utf-8'))
        # 获取最大页面
        item = response.meta['data']
        max_page = response.xpath('//span[@class="fp-text"]/i/text()').extract()
       
        max_page = int(max_page[0]) if max_page else ''
        if max_page:
            for page in range(1,max_page+1):
                page_url = response.url+'&page={}'.format(page)
                yield scrapy.Request(url=page_url,callback=self.change_page,meta={'data':item},dont_filter=True)

    def change_page(self,response):
        item = response.meta['data']
        li_list = response.xpath('//div[@id="plist"]/ul/li')
        for li in li_list:
            # 获取图片的属性不同有两种
            img = li.xpath('.//div[contains(@class,"p-img")]//img/@src | '
                           './/div[contains(@class,"p-img")]//img/@data-lazy-img').extract_first()
            img = 'https:' + img
            book_name = li.xpath('.//div[contains(@class,"p-name")]/a/em/text()').extract()[0].strip()
            book_url = li.xpath('.//div[contains(@class,"p-img")]/a/@href').extract_first()
            book_url = 'https:' + book_url
            # print(book_url)
            # 获取作者、出版社、出版时间
            book_author = li.xpath(
                './/div[contains(@class,"p-bookdetails")]//span[@class="author_type_1"]/a/text()').extract_first()
            publisher = li.xpath(
                './/div[contains(@class,"p-bookdetails")]//span[@class="p-bi-store"]/a/text()').extract_first()
            publish_date = li.xpath(
                './/div[contains(@class,"p-bookdetails")]//span[@class="p-bi-date"]/text()').extract_first().strip()
            item['img'] = img
            item['book_name'] = book_name
            item['book_href'] = book_url
            item['book_author'] = book_author
            item['publisher'] = publisher
            item['publish_date'] = publish_date
            if book_url:
                data_sku = re.findall('https://item.jd.com/(\d+).html', book_url)[0]
                data_sku = data_sku if data_sku else ''
                if data_sku:
                    price_url = 'https://p.3.cn/prices/mgets?skuIds=J_{}'.format(data_sku)
                    yield scrapy.Request(url=price_url, callback=self.get_price, meta={'data': item}, dont_filter=True)

    def get_price(self, response):
        item = response.meta['data']
        # response.body.decode() 是个字符串
        price = json.loads(response.body.decode())[0]['p']
        item['price'] = price
        yield item










