# from twisted.internet import reactor
# from scrapy.crawler import Crawler
# from scrapy.conf import settings
# import logging
# import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from tripadvisor_scraper.spiders.tripadvisor_spider import TripAdvisorSpider

class TACrawler:

	def __init__(self,search,form='csv'):
		self.search = search
		spider = TripAdvisorSpider(search=search)
		self.spider = spider
		self.form = form
		self.start_crawler()

# Need to figure out how to save to local variable
	def start_crawler(self):
		# Set up settings
		settings = get_project_settings()
		if self.form == 'csv':
			settings.set('FEED_FORMAT','csv')
			settings.set('FEED_URI','{0}.csv'.format(self.search))
		if self.form == 'pickle':
			settings.set('FEED_FORMAT','pickle')
			settings.set('FEED_URI','{0}.pkl'.format(self.search))
		settings.set('ROBOTSTXT_OBEY',False)
		# settings.set('CLOSESPIDER_ITEMCOUNT',1)
		# settings.set('DOWNLOAD_DELAY',3)
		settings.set('COOKIES_ENABLED',False)
		# settings.set('ITEM_PIPELINES',{
		# 		'tripadvisor_scraper.pipelines.TripadvisorScraperPipeline': 300
		# 	})
		# settings.set('LOG_FILENAME','log.log')

		# Start crawler
		process = CrawlerProcess(settings)
		process.crawl(self.spider,search=self.search)
		process.start()

# 	spider = TripAdvisorSpider(domain=url) #domain=domain
# 	# settings = get_project_settings()
# 	# settings.overrides['LOG_FILE']='Log.log'
# 	crawler = Crawler(settings)
# 	crawler.configure()
# 	crawler.crawl(spider)
# 	crawler.start()

# spider = 'tripadvisor'
# search = 'san diego'

if __name__ == '__main__':

	TACrawler('san diego')

# start_crawler(spider,search)
# log.start()
# result = reactor.run()
# print result