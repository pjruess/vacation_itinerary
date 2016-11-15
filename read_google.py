import googlemaps
from datetime import datetime
import urllib, json
# pip install Image
import PIL.Image as img

def build_url_text_search(query, output = 'json', key = 'AIzaSyBsILob4SDyR5z0IurzRUylOjioqiTxXP4', **kwargs):
	"""
		Builds URL to search for places on Google Maps using Google APIs.
		Text Search returns info about a set of places based on a string: for example, 'pizza in Austin', 'Indian restaurants in Dallas'
		Search Request Form: https://maps.googleapis.com/maps/api/place/textsearch/output?parameters (output: json, xml)
		This method assumes the JSON output.

		Required params:
		key -- API key
		query -- text string on which to search; this param becomes optional when the type param is also used in the search request

		Some Optional params:
		location -- specified as latitude,longitude (NO SPACE after comma); must also specify radius if this param is used
		radius -- distance (in meters); max allowed is 50000; radius is not included if rankby=distance
		language -- en
		minprice and maxprice -- values range from 0 (most affordable) to 4 (most expensive)
		opennow -- Returns only those places that are open for business at the time the query is sent.
		Note: Places that do not specify opening hours in the Google Places database will not be returned if you include this parameter in your query.
		pagetoken -- next 20 results from previously run search
		type -- at most one type allowed (example: accounting; hospital; library; airport, etc.)
		See https://developers.google.com/places/web-service/supported_types for more types
		You may bias results to a specified circle by passing a location and a radius parameter.
		This will instruct the Google Places service to prefer showing results within that circle. Results outside the defined area may still be displayed.

		The below example shows a search for restaurants near Austin.
		https://maps.googleapis.com/maps/api/place/textsearch/xml?query=restaurants+in+Austin&key=YOUR_API_KEY

		Returns a URL.
	"""
	base_url = 'https://maps.googleapis.com/maps/api/place/textsearch/'
	url = base_url + output + '?key=' + key + '&query=' + query
	for key in kwargs:
		url = url + '&{0}={1}'.format(key, kwargs[key])
	return url

def GetResults(myresponse):
	"""
		Returns a dictionary of the relevant info from Text Search.

		myresponse -- JSON object returned by GetResponse()

		Returns a dict
	"""
	results = []
	if myresponse['status'] == 'OK':
		# print 'Attributions:\n{}'.format(myresponse['html_attributions'])
		count = 1
		for result in myresponse['results']:
			# print '\n\nResult {}'.format(count)
			# if 'icon' in result:
			# 	print 'Icon url: {}'.format(result['icon'])
			# else:
			# 	print 'Icon url: {}'.format('MISSING DATA!')
			# print 'PLace ID: {}'.format(result['place_id'])
			results.append({'place_id': result['place_id']})
			if 'geometry' in result:
				if 'location' in result['geometry']:
					# print 'Geometry location: {}'.format(result['geometry']['location'])
					results[count - 1]['location'] = result['geometry']['location']
				if 'viewport' in result['geometry']:
					# print 'Geometry viewport: {}'.format(result['geometry']['viewport'])
					results[count - 1]['viewport'] = result['geometry']['viewport']
			if 'name' in result:
				# print 'Name: {}'.format(result['name'].encode('utf-8'))
				results[count - 1]['name'] = result['name'].encode('utf-8')
			# else:
			# 	print 'Name: {}'.format('NAME MISSING!')
			# if 'opening_hours' in result:
			# 	print 'Opening Hours: {}'.format(result['opening_hours'])
			# # print 'Photos: {}'.format(result['photos'])
			# if 'scope' in result:
			# 	print 'Scope: {}'.format(result['scope'])	#can be either APP or GOOGLE
			# if 'price_level' in result:
			# 	print 'Price Level: {}'.format(result['price_level'])	# Free (0), Inexpensive, Moderate, Expensive, Very Expensive (4)
			# if 'rating' in result:
			# 	print 'Rating: {}'.format(result['rating'])		
			# if 'types' in result:
			# 	print 'Types: {}'.format(result['types'])
			# if 'vicinity' in result:
			# 	print 'Vicinity: {}'.format(result['vicinity'])
			if 'formatted_address' in result:
				# print 'Address: {}'.format(result['formatted_address'].encode('utf-8'))
				results[count - 1]['address'] = result['formatted_address'].encode('utf-8')
			# if 'permanently_closed' in result:
			# 	print 'Is this place permanently closed? {}'.format(result['permanently_closed'])
			count += 1
	else:
		if myresponse['status'] == 'ZERO_RESULTS':
			print 'No Results found!'
		if myresponse['status'] == 'OVER_QUERY_LIMIT':
			print 'Your over your quota of usage limit!'
		if myresponse['status'] == 'REQUEST_DENIED ':
			print 'Your request has been denied! Please verify your API key.'
		if myresponse['status'] == 'INVALID_REQUEST ':
			print 'Some required parameter is PROBABLY missing!'

	return results

def build_url_place_details(placeid, output = 'json', key = 'AIzaSyBsILob4SDyR5z0IurzRUylOjioqiTxXP4', **kwargs):
	"""
		Builds URL to get the details of a place on Google Maps using Google APIs.
		Place details returns info about a particular establishment or point of interest.
		Need a place_id for this request.
		Search Request Form: https://maps.googleapis.com/maps/api/place/details/output?parameters (output: json, xml)
		This method assumes the JSON output.

		Required params:
		key -- API key
		placeid -- textual identifier that uniquely identifies a place

		Some Optional params:
		language -- en

		The following example requests the details of a place by placeid:
		https://maps.googleapis.com/maps/api/place/details/json?placeid=ChIJN1t_tDeuEmsRUsoyG83frY4&key=YOUR_API_KEY

		Returns a URL.
	"""
	base_url = 'https://maps.googleapis.com/maps/api/place/details/'
	url = base_url + output + '?key=' + key + '&placeid=' + placeid
	for key in kwargs:
		url = url + '&{0}={1}'.format(key, kwargs[key])
	return url

def GetResponse(url, raw = False):
	"""
		Opens a passed URL and collects a JSON response.

		url -- URL whose response is to be read
		raw -- If True, then will return raw response from the URL, otherwise will deserealize the response to a Python object
	"""
	response = urllib.urlopen(url)
	jsonRaw = response.read()
	if raw:
		return jsonRaw
	jsonData = json.loads(jsonRaw)
	return jsonData



if __name__ == '__main__':
	myurl = build_url_text_search(query = 'restaurants in New York')
	myresponse = GetResponse(myurl)
	myresults = GetResults(myresponse)
	for result in myresults:
		print '{0}: {1}'.format(result['name'], result['address'])
