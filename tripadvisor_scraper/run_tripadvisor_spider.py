# from twisted.internet import reactor
# from scrapy.crawler import Crawler
# from scrapy.conf import settings
# import logging
# import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from tripadvisor_scraper.spiders.tripadvisor_spider_2 import TripAdvisorSpider


spider = 'tripadvisor'
search = 'austin'

def setup_crawler(spider,search):
	url = 'https://www.tripadvisor.com/ \
		Search?redirect=true&q={0}&ssrc=g&type=eat'.format(search) 
	process = CrawlerProcess(get_project_settings())
	process.crawl(spider,domain=url)
	process.start()

# 	spider = TripAdvisorSpider(domain=url) #domain=domain
# 	# settings = get_project_settings()
# 	# settings.overrides['LOG_FILE']='Log.log'
# 	crawler = Crawler(settings)
# 	crawler.configure()
# 	crawler.crawl(spider)
# 	crawler.start()

setup_crawler(spider,search)
# log.start()
# result = reactor.run()
# print result