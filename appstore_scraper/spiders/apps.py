import scrapy
from scrapy.spiders import SitemapSpider
import re


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
        
        def convert_to_number(text):
            if not text:
                return None
            
            # Remove '+' if present
            text = text.replace('+', '')
            
            multipliers = {
                'K': 1000,
                'M': 1000000,
                'B': 1000000000
            }
            
            try:
                if text[-1] in multipliers:
                    number = float(text[:-1]) * multipliers[text[-1]]
                    return int(number)
                return int(text.replace(',', ''))
            except (ValueError, IndexError):
                return None

        downloads_raw = response.xpath('//div[@class="ClM7O"]/text()').get()
        downloads = convert_to_number(downloads_raw.split()[0]) if downloads_raw else None
        
        rating_raw = response.xpath('//div[@class="jILTFe"]/text()').get()
        rating = rating_raw.split()[0] if rating_raw else None
        
        reviews_count_raw = response.xpath('//div[@class="EHUI5b"]/text()').get()
        reviews_count = convert_to_number(reviews_count_raw.split()[0]) if reviews_count_raw else None
        
        about_raw = response.xpath('//div[@data-g-id="description"]//text()').getall()
        about = ''.join(about_raw).strip()

        monetization_model = list(set(response.xpath('//div[@class="ulKokd"]//span[@class="UIuSk"]/text()').getall()))
        
        age_rating_raw = response.xpath('//div[@class="g1rdde"]//span[@itemprop="contentRating"]/span/text()').get()
        age_rating = age_rating_raw.split()[-1] if age_rating_raw else None
        
        price_raw = response.xpath('//div[@class="u4ICaf"]//span[@jsname="V67aGc"]/text()').get()
        # Clean up price: keep currency symbol and number, remove extra text
        if price_raw:
            # Match any text followed by a number (with optional decimal places)
            price_match = re.search(r'^([^\d]*\d+(?:\.\d+)?)', price_raw)
            price = price_match.group(1) if price_match else None
            
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
            'age_rating': age_rating,
            'price': price,
            'downloads': downloads
        }
