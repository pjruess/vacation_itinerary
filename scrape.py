from tripadvisor_scraper.run_tripadvisor_spider import TACrawler
# import cPickle
import pandas

search = 'austin'
form = 'csv'

# TACrawler(search=search,form='var')

try: 
	nodes = pandas.read_csv(search + '.' + form)
except IOError:
	print 'No data to read. TACrawler initiated to collect data'
	TACrawler(search=search,itemcount=1,numdata=1000,dldelay=0,form='csv')
	nodes = pandas.read_csv(search + '.' + form)

print nodes['latlon']