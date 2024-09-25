import json
import datetime
from urllib.parse import urlencode, urljoin

import scrapy

from fixprice.items import FixpriceItem
from utils import calculate_discount


class FixPriceSpider(scrapy.Spider):
    name = 'fixprice'
    allowed_domains = ['fix-price.com']
    start_urls = ['https://fix-price.com']

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'x-city': '55',
            'x-language': 'ru',
            'referer': 'https://fix-price.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        },
    }

    def __init__(self, categories=None, *args, **kwargs):
        super(FixPriceSpider, self).__init__(*args, **kwargs)
        if categories:
            self.categories = categories
        else:
            self.categories = [
                'odezhda/detskaya-odezhda',
                'kosmetika-i-gigiena/ukhod-za-polostyu-rta',
                'kosmetika-i-gigiena/gigienicheskie-sredstva',
                'kosmetika-i-gigiena/ukhod-za-telom'
            ]
        self.page_limit = 24

    def start_requests(self):
        params = {'page': '1', 'limit': str(self.page_limit), 'sort': 'sold'}
        for category in self.categories:
            url = f'https://api.fix-price.com/buyer/v1/product/in/{category}?{urlencode(params)}'
            json_data = {
                'category': category,
                'brand': [],
                'price': [],
                'isDividedPrice': False,
                'isNew': False,
                'isHit': False,
                'isSpecialPrice': False,
            }

            yield scrapy.http.JsonRequest(
                url=url,
                method='POST',
                body=json.dumps(json_data),
                headers={'Content-Type': 'application/json'},
                meta={'category': category, 'page': 1},
                callback=self.parse_category,
            )

    def parse_category(self, response):
        page_items = response.json()
        category = response.meta['category']
        page = response.meta['page']

        for item in page_items:
            for result in self.parse_item(item):
                yield result

        total_items = int(response.headers.get('x-count', 0))
        if (page * self.page_limit) < total_items:
            next_page = page + 1
            params = {'page': str(next_page), 'limit': str(self.page_limit), 'sort': 'sold'}
            url = f'https://api.fix-price.com/buyer/v1/product/in/{category}?{urlencode(params)}'

            json_data = {'category': category, 'brand': [], 'price': []}
            yield scrapy.http.JsonRequest(
                url=url,
                method='POST',
                body=json.dumps(json_data),
                headers={'Content-Type': 'application/json'},
                meta={'category': category, 'page': next_page},
                callback=self.parse_category
            )

    def parse_item(self, item):
        item_url = urljoin('https://api.fix-price.com/buyer/v1/product/', item['url'])
        product = FixpriceItem()
        product['timestamp'] = int(datetime.datetime.now().timestamp())
        product['RPC'] = item['sku']
        product['url'] = urljoin('https://fix-price.com/catalog/', item['url'])
        product['title'] = item['title']
        product['marketing_tags'] = [
            'Популярный' if item['isHit'] else '',
            'Акция' if item['isPromo'] else ''
        ]
        product['brand'] = item['brand']['title'] if item['brand'] else 'No brand'
        product['section'] = [item['category']['title']]
        product['price_data'] = {
            'current': float(item['specialPrice']['price']) if item['specialPrice'] else float(item['price']),
            'original': float(item['price']),
            'sale_tag': calculate_discount(
                float(item['price']), float(item['specialPrice']['price'])
            ) if item['specialPrice'] else 'Скидка отсутствует'
        }
        product['stock'] = {
            'in_stock': bool(item['inStock']),
            'count': item.get('inStock', 0)
        }

        yield scrapy.http.JsonRequest(
            url=item_url,
            method='GET',
            callback=self.parse_product_details,
            meta={'product': product}
        )

    def parse_product_details(self, response):
        product = response.meta['product']
        item = response.json()
        product['assets'] = {
            'main_image': item['images'][0].get('src') if item['images'] else None,  # заменить на получение по ключу
            'set_images': [image.get('src') for image in item['images']],
            'view360': ['Найти изображение 360'],  # найти изображение 360
            'video': [urljoin('https://youtu.be/', item['video'])] if item['video'] else []
        }
        product['metadata'] = {
            '__description': item['description'],
            'sku': item['sku'],
            'prodCountry': item['properties'][0].get('prodCountry') if item.get('properties') else None,
            'dimensions': item['variants'][0].get('dimensions'),
        }
        product['variants'] = len(item['variants'])

        yield product

