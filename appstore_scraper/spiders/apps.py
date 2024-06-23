import scrapy


class AppsSpider(scrapy.Spider):
    name = "apps"
    allowed_domains = ["play.google.com"]
    start_urls = ["https://play.google.com"]

    def parse(self, response):
        pass
