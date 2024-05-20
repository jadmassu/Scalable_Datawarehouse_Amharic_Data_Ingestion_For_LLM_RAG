import scrapy


class SwahiliSpiderSpider(scrapy.Spider):
    name = "swahili_spider"
    allowed_domains = ["www.bbc.com"]
    start_urls = ["https://www.bbc.com/swahili/live/czddw48727vt"]

    def parse(self, response):
        pass
