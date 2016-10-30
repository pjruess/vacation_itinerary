import scrapy
from tripadvisor_scraper.items import TripAdvisorReviewItem
import re

"""
scrapy crawl tripadvisor -o itemsTripadvisor.csv -s CLOSESPIDER_ITEMCOUNT=40
"""

class TripAdvisorSpider(scrapy.Spider):
	name = "tripadvisor"

	def start_requests(self):
		urls = [
		'https://www.tripadvisor.com/Attractions-g30196-Activities-Austin_Texas.html'
			]
		for url in urls: 
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		attractions = response.xpath('//div[@class="property_title"]/a/text()').extract()
		rankings = response.xpath('//div[@class="popRanking wrap"]/text()').extract()
		rating_links = response.xpath('//div[@class="property_title"]/a/@href').extract()
		for attr,rank,rate_link in zip(attractions,rankings,rating_links):
			yield {
				'attraction': attr,
				'ranking': re.search('\d+',rank).group(),
				'link': rate_link,
			}

		next_page = response.xpath('//div[@class="unified pagination "]/a/@href').extract()[-1]
		if next_page:
			url = response.urljoin(next_page.extract())
			yield scrapy.Request(url, self.parse)

	# def parse_review(self, response):
	# 	item = TripAdvisorReviewItem()
	# 	item['stars'] = response.xpath('//span[@class="rate sprite-rating_s rating_s"]/img/@alt').extract()[0]
	# 	return item

	# def parse_hotel(self, response):
	# 	for href in response.xpath('//div[starts-with(@class,"quote")]/a/@href'):
	# 		url = response.urljoin(href.extract())
	# 		yield scrapy.Request(url, callback=self.parse_review)

	# 	next_page = response.xpath('//div[@class="unified pagination "]/child::*[2][self::a]/@href')
	# 	if next_page:
	# 		url = response.urljoin(next_page[0].extract())
	# 		yield scrapy.Request(url, self.parse_hotel)