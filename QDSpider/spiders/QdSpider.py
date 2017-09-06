import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor
from ..items import QdBookListItem, QdBookDetailItem

class QdSpider(Spider):
    name = 'qidian'
    start_urls = [
        'http://a.qidian.com/',
    ]
    allowed_domains = [
        'qidian.com'
    ]

    def parse(self, response):
        selector = Selector(response)
        books = selector.xpath('//div[@class="all-book-list"]/div/ul/li')
        for book in books:
            item_loader = ItemLoader(item=QdBookListItem(), selector=book)
            item_loader.add_xpath('novelId', './div[1]/a/@data-bid')
            item_loader.add_xpath('novelName', './div[2]/h4/a/text()')
            item_loader.add_xpath('novelLink', './div[2]/h4/a/@href')
            item_loader.add_xpath('novelAuthor', './div[2]/p[1]/a[1]/text()')
            item_loader.add_xpath('novelType', './div[2]/p[1]/a[2]/text()')
            item_loader.add_xpath('novelType', './div[2]/p[1]/a[3]/text()')
            item_loader.add_xpath('novelStatus', './div[2]/p[1]/span/text()')
            item_loader.add_xpath('novelWords', './div[2]/p[3]/span/text()')
            item_loader.add_xpath('novelImageUrl', './div[1]/a/img/@src')
            bookListItem = item_loader.load_item()
            yield bookListItem

            request = scrapy.Request(url='http:' + bookListItem['novelLink'][0], callback=self.parse_book_detail)
            request.meta['novelId'] = bookListItem['novelId'][0]
            yield request

        next_page = response.xpath('//a[@class="lbf-pagination-next "]/@href').extract_first()
        if next_page:
            next_page_url = 'http:' + next_page[0:14] + '/' + next_page[14:]
            next_page_request = scrapy.Request(url=next_page_url, callback=self.parse)
            yield next_page_request

    def parse_book_detail(self, response):
        item_loader = ItemLoader(item=QdBookDetailItem(), response=response)
        item_loader.add_value('novelId', response.meta['novelId'])
        item_loader.add_xpath('novelLabel', '//div[@class="book-info "]/p[1]/span/text()')
        item_loader.add_xpath('novelLabel', '//div[@class="book-info "]/p[1]/a/text()')
        item_loader.add_xpath('novelClick', '//div[@class="book-info "]/p[3]/em[2]/text()')
        item_loader.add_xpath('novelClick', '//div[@class="book-info "]/p[3]/cite[2]/text()')
        item_loader.add_xpath('novelComm', '//div[@class="book-info "]/p[3]/em[3]/text()')
        item_loader.add_xpath('novelComm', '//div[@class="book-info "]/p[3]/cite[3]/text()')
        item_loader.add_xpath('novelComment', '//div[@class="nav-wrap fl"]/ul/li[3]/a/i/span/text()')
        bookDetailItem = item_loader.load_item()
        yield bookDetailItem
