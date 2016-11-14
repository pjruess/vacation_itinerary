import argparse
import ast
import pandas
import scipy
import os
import shapefile # https://github.com/GeospatialPython/pyshp

# **********************
# Read in arguments passed in from Tkinter gui in scrape_gui.py
# **********************
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

search = d['q'] + ' ' + d['s']# extract search string (ie. 'austin')
form = 'csv' # data extension

# **********************
# Create nodes dataset from attractions, running scrapy if needed
# **********************
try: 
	nodes = pandas.read_csv(search + '.' + form) # read csv if it already exists
	print 'Existing scrapy .csv output retrieved.'
except IOError:
	# If data does not exist, import crawler and extract data
	from tripadvisor_scraper.run_tripadvisor_spider import TACrawler
	print 'No data to read. TACrawler initiated to collect data.'
	TACrawler(search=search,numdata=20,dldelay=0,form='csv')
	nodes = pandas.read_csv(search + '.' + form) # read data from csv
	print 'New scrapy .csv output retrieved.'	

# Retrieve lat and lon values as floats, and write to nodes df
lat = nodes.latlon.str.extract('\[([0-9-.]*),',expand=True) # get latitudes
lon = nodes.latlon.str.extract(', ([0-9-.]*)\]',expand=True) # get longitudes
nodes['lat'] = lat.astype(float).round(9) # round to 6th decimal
nodes['lon'] = lon.astype(float).round(9) # round to 6th decimal

del nodes['latlon']
print nodes
# nodes.to_csv('austin_nodes.csv',index=False) # for testing

# **********************
# Convert road network into pandas dataframe
# **********************
def shp2df(fname,fields=False): 
	"""Convert from ESRI shapefile to Pandas dataframe
	from: http://permalink.gmane.org/gmane.comp.python.pydata/1870"""
	shp = shapefile.Reader(fname)
	records = shp.records() # records (rows)
	fld = scipy.array(shp.fields[1:],dtype=str)
	data = pandas.DataFrame(records, columns=fld[:,0])
	del shp
	if fields:
		data = data[[f for f in fields]]
	return data

# File location for locally-clipped output
state = d['s']

out_shp = 'spatial/output/' + d['q'].lower() + '_roads.shp'

try: 
	road_df = shp2df(out_shp,fields=['oneway','LENGTH_GEO',
		'START_X','START_Y','END_X','END_Y'])
	print 'Existing clipped shapefile retrieved.'
except: 
	# **********************
	# Clip State shapefile to local shapefile
	# **********************
	print 'Clipping new shapefile for local region...'

	# File location for State shapefile to clip from
	roads_shp = 'spatial/{0}/texas.shp'.format(state)

	# Retrieve max and min lat and lon values for clip bounding box
	# Note this only works in North-Eastern quarter of the globe
	# due to positive lat and negative lon values
	left = nodes.min(0,-1)['lon'] # minimum longitude
	bot = nodes.min(0,-2)['lat'] # minimum latitude
	right = nodes.max(0,-1)['lon'] # maximum longitude
	top = nodes.max(0,-2)['lat'] # maximum latitude

	# Add buffer to bounding box values
	buf = 0.1 # Buffer out this many decimal degrees in all directions
	left = left - buf
	bot = bot - buf
	right = right + buf
	top = top + buf

	# ogr2ogr -f "ESRI Shapefile" output.shp input.shp -clipsrc <x_min> <y_min> <x_max> <y_max>
	# Without buffer: -97.8732112 30.1341647 -97.6384294 30.2975692
	# With buffer: -97.9732112 30.0341647 -97.5384294 30.3975692
	clip = 'ogr2ogr -f "ESRI Shapefile" ' + out_shp + ' ' + roads_shp + ' -clipsrc ' + \
			str(left) + ' ' + str(bot) + ' ' + str(right) + ' ' + str(top)
	print clip
	os.system(clip)
	road_df = shp2df(out_shp,fields=['oneway','LENGTH_GEO',
		'START_X','START_Y','END_X','END_Y'])
	print 'Newly clipped shapefile retrieved'
	print 'Verifying new outputs...'
	# Compare outputs to verify. Generally seem pretty close! 
	print top, max( road_df.max(0,3)['START_Y'], road_df.max(0,5)['END_Y'] )
	print bot, min( road_df.min(0,3)['START_Y'], road_df.min(0,5)['END_Y'] )
	print right, max( road_df.max(0,2)['START_X'], road_df.max(0,4)['END_X'] )
	print left, min( road_df.min(0,2)['START_X'], road_df.min(0,4)['END_X'] )

print road_df
road_df.columns = ['oneway','miles','startlon','startlat','endlon','endlat']
# road_df.to_csv('austin_edges.csv',index=False) # for testing

# **********************
# Create road network
# **********************