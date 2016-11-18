""" 
Module for finding the optimal vacation itinerary schedule based on the savings algorithm.

"""

import pandas
import networkx
from geoplotter import *
import matplotlib.pyplot

class vacation_itinerary:

	def __init__(self,city_file,attractions_file,**kwargs):
		# reads road network file
		self.ds = pandas.read_csv(city_file)
		# reads attraction address file
		self.attr = pandas.read_csv(attractions_file)
		# creates GeoPlotter object
		self.DSmap = GeoPlotter()
		# creates networkx graph
		self.createNetworkxGraph()


	# creates the networkx graph for the road network
	def createNetworkxGraph(self): 
        #creates a networkx graph
	    self.gd = networkx.DiGraph()

	    # F Streets
	    self.Fds = self.ds[self.ds.oneway=='F']
	    self.FstartPTS = zip(self.Fds.startlon.values, self.Fds.startlat.values)
	    self.FendPTS = zip(self.Fds.endlon.values, self.Fds.endlat.values)

	    # T Streets
	    self.Tds = self.ds[self.ds.oneway=='T']
	    self.TstartPTS = zip(self.Tds.startlon.values, self.Tds.startlat.values)
	    self.TendPTS = zip(self.Tds.endlon.values, self.Tds.endlat.values)

	    # B Streets
	    self.Bds = self.ds[self.ds.oneway=='B']
	    self.BstartPTS = zip(self.Bds.startlon.values, self.Bds.startlat.values)
	    self.BendPTS = zip(self.Bds.endlon.values, self.Bds.endlat.values)

	    # Simplification - all roads speed = 50mph
	    timeF = scipy.ones((len(self.Fds.miles.values),1))*50.
	    self.F_dict = [dict(weight=mi[0]) for mi in timeF]
	    timeT = scipy.ones((len(self.Tds.miles.values),1))*50.
	    self.T_dict = [dict(weight=mi[0]) for mi in timeT]
	    timeB = scipy.ones((len(self.Bds.miles.values),1))*50.
	    self.B_dict = [dict(weight=mi[0]) for mi in timeB]

	    # add F streets        
	    F_edges = zip(self.FstartPTS, self.FendPTS, self.F_dict)
	    self.gd.add_edges_from(F_edges)
	    
	    # add T streets
	    T_edges = zip(self.TendPTS, self.TstartPTS, self.T_dict)
	    self.gd.add_edges_from(T_edges) 
	    
	    # add B streets
	    B_edges1 = zip(self.BstartPTS, self.BendPTS,self.B_dict)
	    B_edges2 = zip(self.BendPTS, self.BstartPTS,self.B_dict)
	    self.gd.add_edges_from(B_edges1) 
	    self.gd.add_edges_from(B_edges2)


	# finds the shortest path between two nodes using Dijkstra's algorithm in networkx
	def getSPNetworkx(self,startnode,destnode):
		return networkx.shortest_path(self.gd,source=startnode,target=destnode,weight='weight')


	# plots street network using geoplotter
	def drawStreetNetwork(self):
		# sets up edge lon and lat for passing into drawLines function from geoplotter
		street_lines = [[list(b) for b in c] for c in self.gd.edges()]
		# draws the street network
		self.DSmap.drawLines(lines = street_lines,color = 'b',linewidth = 0.3)

	def zoomToFit(self):
		# gets range of longitude and latitude w.r.t. the attractions and zooms map
		lonLatRan = self.getLonLatRange()
		self.DSmap.setZoom(lonLatRan[0][0], lonLatRan[1][0], lonLatRan[0][1], lonLatRan[1][1])
		ax = self.DSmap.getAxes()
		ax.axes.get_xaxis().set_ticks([])
		ax.get_yaxis().set_ticks([])
		matplotlib.pyplot.show()


	# plots a single address
	def drawAddress(self,addressLon,addressLat,marksz=75):
		cND = self.findClosestNode(addressLat,addressLon)
		self.DSmap.drawPoints(lat=cND[1],lon=cND[0],color='r',s=marksz)


	# finds longitude and latitude range w.r.t. lon and lat of attractions
	def getLonLatRange(self):
		return [[min(self.attr.lon.values),max(self.attr.lon.values)],[min(self.attr.lat.values),max(self.attr.lat.values)]]


	# finds the closest node to the set of addresses
	def findClosestNode(self,placeLat,placeLon):
	    pos_nodes = scipy.array([])
	    lonLatRange = self.getLonLatRange()
	    lonRange = lonLatRange[0]
	    latRange = lonLatRange[1]
	    # a little more than 2 seconds longitude and latitude
	    latdf = 0.0005
	    londf = 0.0005
	    ct = 0
	    listLon = list(zip(*self.gd.nodes())[0])
	    listLat = list(zip(*self.gd.nodes())[1])
	    
	    while len(pos_nodes)==0 and ((latdf<scipy.absolute(latRange[0]-latRange[1])/2) and (londf<scipy.absolute(lonRange[0]-lonRange[1]))):
	        pos_nodes = scipy.array([])
	        ct = ct + 1
	        latidx1 = scipy.where((listLat<placeLat+ct*latdf))[0]
	        tempLatList = [listLat[a] for a in latidx1]
	        tempLonList = [listLon[a] for a in latidx1]
	        latidx = scipy.where(tempLatList>placeLat-ct*latdf)[0]
	        tempLatList = [tempLatList[b] for b in latidx]
	        tempLonList = [tempLonList[b] for b in latidx]
	        lonidx1 = scipy.where(tempLonList>placeLon-ct*londf)[0]
	        tempLatList = [tempLatList[c] for c in lonidx1]
	        tempLonList = [tempLonList[c] for c in lonidx1]
	        lonidx = scipy.where(tempLonList<placeLon+ct*londf)[0]
	        pos_nodes = scipy.array([[tempLonList[d],tempLatList[d]] for d in lonidx])
	        
	    if len(pos_nodes)==0:
	        return None
	    else:
	        dist = scipy.sqrt(scipy.sum(scipy.array([pos_nodes.T[0]-placeLon, pos_nodes.T[1]-placeLat])**2,axis=0))
	        # returns the name of the closest node as a string
	        #return str(pos_nodes[0][scipy.where(dist==min(dist))][0])+' '+str(pos_nodes[1][scipy.where(dist==min(dist))][0])
	        # recall, [lon, lat]
	        closeNode = scipy.array([pos_nodes.T[0][scipy.where(dist==min(dist))][0],
	                            pos_nodes.T[1][scipy.where(dist==min(dist))][0]])
	        return closeNode
	

	# finds the total reward given an itinerary
	def getItineraryReward(self,itin):

		# calculates reward for visiting all the attractions in the itinerary
		# reward is in terms of USD
		attr_reward_temp = [self.attr[self.attr.attraction == nm].rating.values[0]*10. for nm in itin]
		attr_reward = scipy.sum(attr_reward_temp)
		print attr_reward

		time_reward_temp = [networkx.shortest_path_length(self.gd, source=(self.attr[self.attr.attraction==itin[p]].lon.values[0],self.attr[self.attr.attraction==itin[p]].lat.values[0]), target=(str(self.attr[self.attr.attraction==itin[p+1]].lon.values[0]),str(self.attr[self.attr.attraction==itin[p+1]].lat.values[0])), weight='weight') for p in range(1)] # range(len(itin)-1)]

		return 0


	def savings_alg(self):

		# Compute shortest path between source and all other reachable nodes for a weighted graph.
		# May not want this since computationally expensive
		# all_shortest_paths(G, source, target, weight=None)
		# OR single_source_dijkstra_path(G, source, cutoff=None, weight='weight')

		return 0


if __name__ == '__main__':
	austin_itinerary = vacation_itinerary(city_file='austin_edges.csv',attractions_file='austin_nodes.csv')
	austin_itinerary.drawStreetNetwork()
	austin_itinerary.drawAddress(addressLon=austin_itinerary.attr.lon.values[0],addressLat=austin_itinerary.attr.lat.values[0])
	austin_itinerary.zoomToFit()
	
	#austin_itinerary.getItineraryReward(itin=temp)

	

