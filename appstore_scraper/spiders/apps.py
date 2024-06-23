import scrapy
from scrapy.spiders import SitemapSpider


class AppsSpider(SitemapSpider):
    name = "apps"
    allowed_domains = ["play.google.com"]
    sitemap_urls = ['https://play.google.com/robots.txt']
    sitemap_rules = [
        ('/apps/', 'parse')
    ]

    def parse(self, response):
        name = response.xpath('//h1/text()').get()
        developer = {
            'url': response.xpath('//div[@class="Vbfug auoIOc"]/a/@href').get(),
            'name': response.xpath('//div[@class="Vbfug auoIOc"]/a/span/text()').get()
        }
        rating = response.xpath('//div[@class="jILTFe"]/text()').get()
        about_raw = response.xpath('//div[@data-g-id="description"]//text()').getall()
        about = ''.join(about_raw).strip()
        yield {
            'url': response.url,
            'name': name,
            'developer': developer,
            'rating': rating,
            'about': about
        }
