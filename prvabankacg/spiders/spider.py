import scrapy

from scrapy.loader import ItemLoader
from ..items import PrvabankacgItem
from itemloaders.processors import TakeFirst


class PrvabankacgSpider(scrapy.Spider):
	name = 'prvabankacg'
	start_urls = ['https://www.prvabankacg.com/en/press_release.php']

	def parse(self, response):
		post_links = response.xpath('//div[@class="col-sm-4 saznajVise"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="jp-next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)


	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="container containerDetalji"]/div[@class="row"]//text()[normalize-space() and not(ancestor::h1)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="datumDetalji"]/p/text()').get()

		item = ItemLoader(item=PrvabankacgItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
