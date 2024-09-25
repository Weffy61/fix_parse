from typing import Any, Dict, List

import scrapy


class FixpriceItem(scrapy.Item):
    timestamp: int = scrapy.Field()
    RPC: str = scrapy.Field()
    url: str = scrapy.Field()
    title: str = scrapy.Field()
    marketing_tags: List[str] = scrapy.Field()
    brand: str = scrapy.Field()
    section: List[str] = scrapy.Field()

    price_data: Dict[str, Any] = scrapy.Field()
    price_data['current']: float = scrapy.Field()
    price_data['original']: float = scrapy.Field()
    price_data['sale_tag']: str = scrapy.Field()

    stock: Dict[str, Any] = scrapy.Field()
    stock['in_stock']: bool = scrapy.Field()
    stock['count']: int = scrapy.Field()

    assets: Dict[str, Any] = scrapy.Field()
    assets['main_image']: str = scrapy.Field()
    assets['set_images']: List[str] = scrapy.Field()
    assets['view360']: List[str] = scrapy.Field()
    assets['video']: List[str] = scrapy.Field()

    metadata: Dict[str, Any] = scrapy.Field()
    metadata['__description']: str = scrapy.Field()
    metadata['sku']: int = scrapy.Field()
    metadata['prodCountry']: str = scrapy.Field()
    metadata['dimensions']: Dict[str, Any] = scrapy.Field()

    variants: int = scrapy.Field()
