import scrapy
from scrapy.spiders import SitemapSpider


class AppsSpider(SitemapSpider):
    name = "apps"
    allowed_domains = ["play.google.com"]
    sitemap_urls = ['https://play.google.com/robots.txt']
    sitemap_rules = [
        ('/store/apps/details', 'parse')
    ]

    def parse(self, response):
        if 'editorial' in response.url:
            return None
        name = response.xpath('//span[@class="AfwdI"]/text()').get()
        developer = {
            'url': response.xpath('//div[@class="Vbfug auoIOc"]/a/@href').get(),
            'name': response.xpath('//div[@class="Vbfug auoIOc"]/a/span/text()').get()
        }
        rating = response.xpath('//div[@class="jILTFe"]/text()').get()
        reviews_count = response.xpath('//div[@class="EHUI5b"]/text()').get()
        about_raw = response.xpath('//div[@data-g-id="description"]//text()').getall()
        monetization_model = list(set(response.xpath('//div[@class="ulKokd"]//span[@class="UIuSk"]/text()').getall()))
        age_rating = response.xpath('//div[@class="g1rdde"]//span[@itemprop="contentRating"]/span/text()').get()
        age_rating = age_rating.split()[0] if age_rating else None
        about = ''.join(about_raw).strip()
        categories = response.xpath('//div[@class="Uc6QCc"]//span[@jsname="V67aGc"]/text()').getall()
        updatedOn = response.xpath('//div[@class="xg1aie"]/text()').get()
        yield {
            'url': response.url,
            'name': name,
            'developer': developer,
            'rating': rating,
            'reviews_count': reviews_count,
            'updatedOn': updatedOn,
            'about': str(about),
            'categories': categories,
            'monetization_model': monetization_model,
            'age_rating': age_rating
        }
