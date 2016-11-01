# from twisted.internet import reactor
# from scrapy.crawler import Crawler
# from scrapy.conf import settings
# import logging
# import scrapy
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import signals
from scrapy.utils.project import get_project_settings
from tripadvisor_scraper.spiders.tripadvisor_spider import TripAdvisorSpider
from tripadvisor_scraper.pipelines import spider_closed

spider = 'tripadvisor'
search = 'austin'

def setup_crawler(spider,search):
	url = 'https://www.tripadvisor.com/ \
		Search?redirect=true&q={0}&ssrc=g&type=eat'.format(search) 
	settings = get_project_settings()
	spider = TripAdvisorSpider(domain=url)
	crawler = Crawler(spider,settings)

	crawler.signals.connect(spider_closed, signal=signals.spider_closed)

	crawler.crawl(spider)
	crawler.start()

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