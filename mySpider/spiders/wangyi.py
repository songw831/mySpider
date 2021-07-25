import scrapy
from selenium import webdriver
from mySpider.items import  MyspiderItem

class FundSpider(scrapy.Spider):
    name = 'wangyi'
    #allowed_domains = ['www.xxx.com']
    start_urls = ['http://news.163.com/']
    modules_url = [] #存放五个版块的url
    def __init__(self):
        self.bro = webdriver.Chrome(executable_path='D:\PyCharm\mySpider\chromedriver.exe')

    def parse(self, response):
        li_list = response.xpath('//*[@id="index2016_wrap"]/div[1]/div[2]/div[2]/div[2]/div[2]/div/ul')
        alist = [3,4,6,7,8]
        for index in alist:
            module_url = li_list[index].xpath('./a/@href').extract_first()
            self.modules_url.append(module_url)
        #依次对每一个版块进行请求
        for url in self.module_url:
            yield scrapy.Request(url, callback= self.parse_module)

    def parse_module(self, response):
        div_list = response.xpath('/html/body/div/div[3]/div[4]/div[1]/div[1]/div/ul/li/div/div')
        for div in div_list:
            title = div.xpath('./div/div[1]/h3/a/text()').extract_fisrt()
            new_detail_url = div.xpath('./div/div[1]/h3/a/@href').extract_first()
            item = MyspiderItem()
            item.title = title
            yield  scrapy.Request(url=new_detail_url, callback=self.parse_detail, meta={'item':item})

    def parse_detail(self,response):
        content = response.xpath('//*[@id="content"]/div[2]//text()').extract()
        content = ''.join(content)
        item = response.meta('item')
        item['content'] = content
        yield  item

    def closed(self, spider):
        self.bro.quit()
