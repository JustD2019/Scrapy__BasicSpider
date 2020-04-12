# -*- coding: utf-8 -*-
import scrapy
from test_spider.items import TestSpiderItem #导入item类
from scrapy import cmdline

class JobSpider(scrapy.Spider):
    name = 'job'
    allowed_domains = ['51job.com']
    start_urls = ['https://search.51job.com/list/140000,000000,0000,00,9,99,java,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=']

    def parse(self, response):
        print()
        data = response.xpath("//div[@class = 'el']")
        for spider_data in data:
            try:
                spider_job = spider_data.xpath("./p/span/a/text()").get().strip()
                spider_company = spider_data.xpath("./span/a/text()").get().strip()
                # print("正在爬取")

                item = TestSpiderItem(job = spider_job,company = spider_company)
                yield item  #返回item，并没有在此处结束函数
            except Exception as e:
                print("错误%s"%e)
        #通过xpath找出下一页按钮的链接，last()为最后一个li标签
        next_url = response.xpath("//div[@class = 'dw_page']//li[last()]/a/@href").extract_first()
        #通过是否有链接来判断爬虫接下来操作
        if not next_url:
            return #如果没有下一页就结束
        else:
            yield scrapy.Request(next_url,callback = self.parse) #有下一页就继续执行parse

def main():
    scrapy.cmdline.execute(['scrapy', 'crawl', 'job'])

main()
