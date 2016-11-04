# Parse Tkinter gui search to create local variables
import argparse
import ast

parser = argparse.ArgumentParser() # allow the creation of arguments

namespace,unparsed = parser.parse_known_args() # unpack arguments

def parse_arg(arg):
	k,v = arg.split('=',1) # split over equal sign (ie. extract (q, query'))
	try:
		v = ast.literal_eval(v) # evaluate the string as a python literal
	except ValueError:
		pass # if not, evaluate as string

	return k.lstrip('-'),v

d = dict(parse_arg(arg) for arg in unparsed) # create dictionary of arguments

# Create nodes dataset, running scrapy if needed 
from tripadvisor_scraper.run_tripadvisor_spider import TACrawler
import pandas

search = d['q'] # extract search string (ie. 'austin')
form = 'csv'

try: 
	nodes = pandas.read_csv(search + '.' + form) # read csv if it already exists
except IOError:
	# If data does not exist, initiate scrapy spider to extract data
	print 'No data to read. TACrawler initiated to collect data'
	TACrawler(search=search,itemcount=1,numdata=1000,dldelay=0,form='csv')
	nodes = pandas.read_csv(search + '.' + form) # read data from csv

print nodes['latlon']