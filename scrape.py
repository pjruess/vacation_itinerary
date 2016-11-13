import argparse
import ast
import pandas
import scipy

# Read in arguments passed in from Tkinter gui in scrape_gui.py
parser = argparse.ArgumentParser() # allow the creation of arguments
namespace,unparsed = parser.parse_known_args() # unpack arguments

def parse_arg(arg):
	k,v = arg.split('=',1) # split over equal sign (ie. extract (q, 'query'))
	try:
		v = ast.literal_eval(v) # evaluate the string as a python literal
	except ValueError:
		pass # if not, evaluate as string

	return k.lstrip('-'),v # parsed argument

d = dict(parse_arg(arg) for arg in unparsed) # create dictionary of arguments

# Create nodes dataset, running scrapy if needed 
search = d['q'] # extract search string (ie. 'austin')
form = 'csv' # data extension

try: 
	nodes = pandas.read_csv(search + '.' + form) # read csv if it already exists
except IOError:
	# If data does not exist, import crawler and extract data
	from tripadvisor_scraper.run_tripadvisor_spider import TACrawler
	print 'No data to read. TACrawler initiated to collect data'
	TACrawler(search=search,numdata=20,dldelay=0,form='csv')
	nodes = pandas.read_csv(search + '.' + form) # read data from csv

lat = nodes.latlon.str.extract('\[([0-9-.]*),',expand=True) # get latitudes
lon = nodes.latlon.str.extract(', ([0-9-.]*)\]',expand=True) # get longitudes
nodes['lat'] = lat.astype(float).round(9) # round to 6th decimal
nodes['lon'] = lon.astype(float).round(9) # round to 6th decimal

# Note this only works in North-Eastern quarter of the globe due to 
# positive lat and negative lon values
latmax = nodes.max(0,-2)['lat']
latmin = nodes.min(0,-2)['lat']
lonmax = nodes.max(0,-1)['lon']
lonmin = nodes.min(0,-1)['lon']
ur = (latmax,lonmin)
ll = (latmin,lonmax)

print nodes[['lat','lon']]

# *******************
# NEXT TODO: Define bounding box and clip us-road-network shapefile
# using ogr2ogr clipping capabilities
# *******************