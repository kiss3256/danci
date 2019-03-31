# -*- coding: utf-8 -*-
import scrapy


class NkmbaSpider(scrapy.Spider):
    name = 'nkmba'
    allowed_domains = ['nkmba.com']
    start_urls = ['http://www.nkmba.com/article-cigen']

    def parse(self, response):
        urls = response.xpath('//*[@id="xuexi_yingyu_danci"]/div[1]/dl')
        for url in urls:
            href = url.xpath('dt/a/@href').get()
            yield scrapy.Request(response.urljoin(href), callback=self.parsePage)

    def parsePage(self, response):
        root = response.xpath('//*[@id="xuexi_yingyu_danci"]/div[1]/dl/dt/a[1]/text()').get()
        discription = response.xpath('//*[@id="xuexi_yingyu_danci"]/div[1]/dl/dd/text()').get()
        content = response.xpath('//*[@id="xuexi_yingyu_danci"]/div[2]/dl')

        words = []
        for word in content:
            words.append({
                'word': word.xpath('dt/text()').get(),
                'definition': word.xpath('dd/text()').get()
                })

        yield {
        'root': root,
        'discription': discription,
        'words': words
        }
