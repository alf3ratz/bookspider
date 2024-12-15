from scrapy_redis.spiders import RedisSpider
import re
import logging

class BookspiderSpider(RedisSpider):
    name = "bookspider"
    redis_key = 'bookspider:start_urls'

    def parse(self, response):
        for book in response.css('div.product-card'):
            try:
                name = book.css('div.product-card::attr(data-product-name)').get().strip()
                author = book.css('span.ui-comma-separated-links__tag::text').get().strip()
                price = re.sub("[^\d\.]", "", str(book.css('span.price-info__price::text')))
                if price.isnumeric():
                    yield {
                        'name': name,
                        'author': author,
                        'price': price
                    }
            except:
                logging.error("Can't parse data: %s" % (name))

        next_page = response.css("a.base-link--active.base-link--exact-active.ui-button.ui-button--size-s.ui-button--color-secondary-blue").attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)