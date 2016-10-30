import scrapy
# from tripadvisor_scraper.items import TripAdvisorReviewItem
import re
import scipy
import geocoder

"""
UBUNTU TERMINAL CALL: 
scrapy crawl tripadvisor2 -o itemsTripadvisor.csv -s CLOSESPIDER_ITEMCOUNT=40
"""

class TripAdvisorSpider(scrapy.Spider):
	name = "tripadvisor2"

	def start_requests(self):
		urls = [
		'https://www.tripadvisor.com/Attractions-g30196-Activities-Austin_Texas.html'
			]
		for url in urls: 
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		for href in response.xpath('//div[@class="property_title"]/a/@href').extract():
			url = response.urljoin(href)
			yield scrapy.Request(url, callback=self.parse_review, priority=1)

		next_page = response.xpath('//div[@class="unified pagination "]/a/@href').extract()[-1]
		if next_page:
			url = response.urljoin(next_page)
			yield scrapy.Request(url, self.parse)

	def parse_review(self, response):
		# from scrapy.shell import inspect_response
		# inspect_response(response, self)


		# Pull all review data for attraction
		rating_info = response.xpath('//ul[@class="barChart"]')
		if len(rating_info) == 0: # check if list of activities
			# Take only first item out of list
			href = response.xpath('//div[@class="property_title"]/a/@href').extract()[0]
			url = response.urljoin(href)
			yield scrapy.Request(url, callback=self.parse_review)
		else: 
			# Pull name of attraction
			attraction = response.xpath('//h1[@id="HEADING"]/text()').extract()[1]
			attraction = re.sub('\n','',attraction)
			
			# Pull ranking of attraction
			# ranking = response.xpath('//div[@class="slim_ranking"]//span[@class]/text()').extract()[0]
			# ranking = re.sub('#','',ranking)

			# Calculate average rating
			nums = rating_info.xpath('//div[@class="valueCount fr part"]/text()').extract()
			ratings = scipy.array([float(n) for n in nums if n])
			values = scipy.arange(5,0,-1)
			rateavg = scipy.sum(ratings*values)/scipy.sum(ratings)
			rateavg = str( scipy.around( rateavg, decimals=2 ) )

			# Pull address
			street = response.xpath('//span[@property="streetAddress"]/text()').extract()[0]
			city = response.xpath('//span[@property="addressLocality"]/text()').extract()[0]
			state = response.xpath('//span[@property="addressRegion"]/text()').extract()[0]
			postal = response.xpath('//span[@property="postalCode"]/text()').extract()[0]
			country = response.xpath('//span[@property="addressCountry"]/@content').extract()[0]
			address = street + ', ' + city + ', ' + state + ' ' + postal + ' ' + country
			latlon = geocoder.google(address).latlng # geocode address

			# Return results
			yield {
				'attraction': attraction,
				# 'ranking': ranking,
				'rating': rateavg,
				'address': address,
				'latlon': latlon,
			}
