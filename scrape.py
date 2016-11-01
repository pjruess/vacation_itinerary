from tripadvisor_scraper.run_tripadvisor_spider import TACrawler
# import cPickle
import pandas

search = 'austin'
form = 'csv'

try: 
	nodes = pandas.read_csv(search + '.' + form)
except IOError as e:
	print 'No data to read. TACrawler initiated to collect data'
	TACrawler(search=search,form='csv')
	nodes = pandas.read_csv(search + '.' + form)

print nodes

