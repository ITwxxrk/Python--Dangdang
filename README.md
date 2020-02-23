# Python--Dangdang
基于python语言的当当网商品信息爬虫系统
开发环境为Windows 10、Python 3.7和MySQL 8.0.18
主要设计和实现:
1 创建爬虫项目
具体操作：打开cmd界面，用cd操作跳转到你想要存储文件的位置，输入：scrapy startproject dangdang，创建dangdang爬虫项目
2 创建一个以基础爬虫为模板的爬虫文件，命令为：dd.py
具体操作：在cmd界面输入：scrapy genspider -t dd dangdang.com即可。结果如下图所示，在spiders文件夹中生成了文件dd.py。
3 确定需要爬取的数据
具体操作：在配置文件items.py中创建要爬取的数据定义，具体代码如下：
import scrapy
class DangdangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    comment = scrapy.Field()
    shop = scrapy.Field()
price = scrapy.Field()
4 确定网页以及数据的命名规律
具体操作：打开当当网（dangdang.com）,按F12查看网页源代码，确定想要爬虫的数据在网页中的命名方式。同时找寻多个网页地址的规律，便于编程。在爬虫文件dd.py中基于Xpath爬取网站信息，并且实现多页爬取。具体代码如下：
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import scrapy
from dangdang.items import DangdangItem
from scrapy.http import Request # 依次爬取的工具
class DdSpider(scrapy.Spider):
    name = 'dd'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://category.dangdang.com/pgl-cid4008154.html']
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64:x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',}
   		def parse(self, response):
       		 item = DangdangItem()
        	item["title"] = response.xpath('//p[@name="title"]/a/@title').extract()
       		 item["link"] = response.xpath('//p[@name="title"]/a/@href').extract()
        	item["comment"] = response.xpath('//a[@dd_name="单品评论"]/text()').extract()
        	item["shop"] = response.xpath('//p/a[@dd_name="单品店铺"]/text()').extract()
        	item["price"] = response.xpath('//span[@class="price_n"]/text()').extract()
        	print(item)
        	yield item # 将数据提交到Pipeline中
        	for i in range(2,2001):
            	url = 'http://category.dangdang.com/pg'+str(i)+'-cid4008154.html'
            	# callback为回调函数
            	yield Request(url,callback=self.parse,headers=self.header)
5 爬虫风险规避
由于可能会出现爬虫失败，以及我们需要将获取的数据进行相关处理，因此我们在settings.py文件处，要修改三处：
① BOT_NAME = 'dangdang
SPIDER_MODULES = ['dangdang.spiders']
NEWSPIDER_MODULE = 'dangdang.spiders'
② ROBOTSTXT_OBEY = False
③ ITEM_PIPELINES = {	'dangdang.pipelines.DangdangPipeline': 300,}
6 创建数据库和表
本系统选择的是MySQL数据库，采用Navicat for MySQL实现系统与数据库的简单连接。打开Navicat ，新建数据库，并且创建相应的SQL表，用于存储数据，命名为products。查询代码如下：
CREATE TABLE `products`(
`id` int(10) NOT NULL AUTO_INCREMENT,
`shop` varchar(100) DEFAULT NULL COMMENT '出售店铺',
`title` varchar(100) DEFAULT NULL COMMENT '商品标题',
`link` varchar(100) DEFAULT NULL COMMENT '商品链接',
`price` varchar(100) DEFAULT NULL COMMENT '商品价格',
`comment` varchar(100) DEFAULT NULL COMMENT '商品评论',
PRIMARY KEY (`id`)
)ENGINE=INNODB DEFAULT CHARSET=utf8;
7 实现连接数据库功能
在Pipelines.py文件中编写相应的数据库链接函数，以及数据库存储操作将数据存入本地数据库中，具体代码如下：
import pymysql
def condb():
    conn = pymysql.connect(host='localhost',port=3306,user='root',
password='cxks20121221!',db='dangdang',charset='utf8mb4')
    return conn
class DangdangPipeline(object):
    def process_item(self, item, spider):
        dbObject = condb()
        cursor = dbObject.cursor()
        sql = 'INSERT INTO products(shop,title,link,price,comment) VALUES(%s,%s,
%s,%s,%s)'
        # 将数据导入到本地数据库中
        for j in range(len(item['title'])):
            try:
                cursor.execute(sql,(item['shop'][j],item['title'][j],item['link'][j],
item['price'][j],item['comment'][j],))
                cursor.close()
                dbObject.commit()
            except Exception as e:
                print(e)
                dbObject.rollback()
        return item
8 运行系统功能
新建run.py，用于直接运行爬虫。具体代码如下：
from scrapy import cmdline
cmdline.execute('scrapy crawl zhihu_topic'.split())
