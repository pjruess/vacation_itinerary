""" 
Module for finding the optimal vacation itinerary schedule based on the savings algorithm.

"""

import scipy
import pandas
import networkx
from geoplotter import *
import matplotlib.pyplot

TIME_VALUE_OF_MONEY = 12.

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

	    # Simplification - all roads speed = 50mph, D=RT
	    timeF = self.Fds.miles.values/50.
	    self.F_dict = [dict(time=mi) for mi in timeF]
	    timeT = self.Tds.miles.values/50.
	    self.T_dict = [dict(time=mi) for mi in timeT]
	    timeB = self.Bds.miles.values/50.
	    self.B_dict = [dict(time=mi) for mi in timeB]

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

	    # gets the connected subgraphs of the networkx graph and finds the subgraph with the largest number of edges
	    gdcon_temp = list(networkx.weakly_connected_component_subgraphs(self.gd,copy=True))
	    temp_edge_length = scipy.array([len(p.edges()) for p in gdcon_temp])
	    idx = scipy.where(temp_edge_length==max(temp_edge_length))[0][0]
	    self.gdcon = gdcon_temp[idx]

	    print 'There are some duplicate streets'
	    print '# of F streets: ', len(self.Fds.startlon.values)
	    print '# of T streets: ', len(self.Tds.startlon.values)
	    print '# of B streets: ', len(self.Bds.startlon.values)
	    print 'total: ',len(self.gd.edges())


	# finds the shortest path between two nodes using Dijkstra's algorithm in networkx
	def getSPNetworkx(self,startnode,destnode,GPH):
		return networkx.shortest_path(GPH,source=startnode,target=destnode,weight='time')


	# plots street network using geoplotter
	def drawStreetNetwork(self,GPH):
		# sets up edge lon and lat for passing into drawLines function from geoplotter
		street_lines = [[list(b) for b in c] for c in GPH.edges()]
		# draws the street network
		self.DSmap.drawLines(lines = street_lines,color = 'b',linewidth = 0.3)


	# plots a single address
	def drawAddress(self,addressLon,addressLat,marksz=75,co='r'):
		#cND = self.findClosestNode(addressLat,addressLon,GPH=GPH_draw)
		#self.DSmap.drawPoints(lat=cND[1],lon=cND[0],color=co,s=marksz)
		self.DSmap.drawPoints(lat=addressLat,lon=addressLon,color=co,s=marksz)


	# draws the path
	def drawPath(self,path,lw=5):
	    self.DSmap.drawLines(lines = path,color = 'y',linewidth = lw,alpha = 3)


	# formats map
	def zoomToFit(self):
		# gets range of longitude and latitude w.r.t. the attractions and zooms map
		lonLatRan = self.getLonLatRange()
		margin = 0.005
		self.DSmap.setZoom(lonLatRan[0][0]-margin, lonLatRan[1][0]-margin, lonLatRan[0][1]+margin, lonLatRan[1][1]+margin)
		ax = self.DSmap.getAxes()
		ax.axes.get_xaxis().set_ticks([])
		ax.get_yaxis().set_ticks([])
		matplotlib.pyplot.show()


	# finds longitude and latitude range w.r.t. lon and lat of attractions
	def getLonLatRange(self):
		return [[min(self.attr.lon.values),max(self.attr.lon.values)],[min(self.attr.lat.values),max(self.attr.lat.values)]]


	# finds the closest node to the set of addresses
	def findClosestNode(self,placeLat,placeLon,GPH):
	    pos_nodes_zero = True
	    lonLatRange = self.getLonLatRange()
	    lonRange = lonLatRange[0]
	    latRange = lonLatRange[1]
	    # a little more than 2 seconds longitude and latitude
	    latdf = 0.0005
	    londf = 0.0005
	    ct = 0
	    listLon = [u for u,v in GPH.nodes_iter()]
	    listLat = [v for u,v in GPH.nodes_iter()]

	    while pos_nodes_zero==True and ((latdf<scipy.absolute(latRange[0]-latRange[1])/2) and (londf<scipy.absolute(lonRange[0]-lonRange[1]))):
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
	        pos_nodes = [[tempLonList[d],tempLatList[d]] for d in lonidx]
	        pos_nodes = map(list, zip(*pos_nodes))
	        #print pos_nodes
	        if len(pos_nodes)!=0:
	        	pos_nodes_zero = False
	    
	    if len(pos_nodes)==0:
	        return None
	    else:
	        dist = scipy.sqrt(scipy.sum(scipy.array([pos_nodes[0]-placeLon, pos_nodes[1]-placeLat])**2,axis=0))
	        # returns the name of the closest node as a string
	        #return str(pos_nodes[0][scipy.where(dist==min(dist))][0])+' '+str(pos_nodes[1][scipy.where(dist==min(dist))][0])
	        # recall, [lon, lat]
	        closeNode = [pos_nodes[0][scipy.where(dist==min(dist))[0][0]], pos_nodes[1][scipy.where(dist==min(dist))[0][0]]]
	        return closeNode
	        
	    
	

	# finds the total reward given an itinerary
	def getItineraryReward(self,itin):
		print itin
		print
		# calculates reward for visiting all the attractions in the itinerary
		# reward is in terms of USD
		attr_reward_temp = [self.attr[(self.attr.attraction == nm)].rating.values[0]*10. for nm in itin if (nm != 'hotel')]
		attr_reward = scipy.sum(attr_reward_temp)
		print 'Total Attraction Reward = ', attr_reward
		
		time_reward_temp = [networkx.shortest_path_length(self.gdcon, source=tuple(self.findClosestNode(placeLon=self.attr[self.attr.attraction==itin[p]].lon.values[0],placeLat=self.attr[self.attr.attraction==itin[p]].lat.values[0],GPH=self.gdcon)), target=tuple(self.findClosestNode(placeLon=self.attr[self.attr.attraction==itin[p+1]].lon.values[0],placeLat=self.attr[self.attr.attraction==itin[p+1]].lat.values[0],GPH=self.gdcon)), weight='time') for p in range(len(itin)-1)]
		time_reward = scipy.sum(time_reward_temp)*TIME_VALUE_OF_MONEY*(-1)
		print 'Time Reward (Negative) = ', time_reward
		
		print
		
		self.drawStreetNetwork(GPH=self.gd)

		for h in range(len(itin)):
			print itin[h]
			temp1 = [self.attr[self.attr.attraction==itin[h]].lon.values[0],self.attr[self.attr.attraction==itin[h]].lat.values[0]]
			print temp1
			if h==17:
				self.drawAddress(addressLon=temp1[0],addressLat=temp1[1],co='r')
				temp1_closeN = self.findClosestNode(placeLon=temp1[0],placeLat=temp1[1],GPH=self.gdcon)
				self.drawAddress(addressLon=temp1_closeN[0],addressLat=temp1_closeN[1],co='m')
			elif h==18:
				self.drawAddress(addressLon=temp1[0],addressLat=temp1[1],co='c')
				temp1_closeN = self.findClosestNode(placeLon=temp1[0],placeLat=temp1[1],GPH=self.gdcon)
				self.drawAddress(addressLon=temp1_closeN[0],addressLat=temp1_closeN[1],co='m')
			else:
				self.drawAddress(addressLon=temp1[0],addressLat=temp1[1],co='g')
				temp1_closeN = self.findClosestNode(placeLon=temp1[0],placeLat=temp1[1],GPH=self.gdcon)
				self.drawAddress(addressLon=temp1_closeN[0],addressLat=temp1_closeN[1],co='m')

		"""
		print itin[18]
		temp5 = [self.attr[self.attr.attraction==itin[18]].lon.values[0],self.attr[self.attr.attraction==itin[18]].lat.values[0]]
		print temp5
		self.drawAddress(addressLon=temp5[0],addressLat=temp5[1],co='c')
		temp5_closeN = self.findClosestNode(placeLon=temp5[0],placeLat=temp5[1],GPH=self.gdcon)
		self.drawAddress(addressLon=temp5_closeN[0],addressLat=temp5_closeN[1],co='c')
		print temp5_closeN
		"""
		#self.zoomToFit()


		#return attr_reward + time_reward


	def savings_alg(self):

		# Compute shortest path between source and all other reachable nodes for a weighted graph.
		# May not want this since computationally expensive
		# all_shortest_paths(G, source, target, weight=None)
		# OR single_source_dijkstra_path(G, source, cutoff=None, weight='weight')

		return 0


if __name__ == '__main__':
	austin_itinerary = vacation_itinerary(city_file='austin_edges.csv',attractions_file='austin_nodes.csv')
	"""
	austin_itinerary.drawStreetNetwork(GPH=austin_itinerary.gd)
	austin_itinerary.drawAddress(addressLon=austin_itinerary.attr.lon.values[0],addressLat=austin_itinerary.attr.lat.values[0])
	austin_itinerary.zoomToFit()
	"""
	temp = ['hotel']
	# took out Zilker because not working in shortest path
	temp.extend(austin_itinerary.attr[austin_itinerary.attr.attraction != 'Zilker Metropolitan Park'].attraction.values)
	total_reward = austin_itinerary.getItineraryReward(itin=temp)
	# working on graphing the path
	for locidx in range(2): #range(len(temp)-1):
		startN_temp = austin_itinerary.findClosestNode(placeLon=austin_itinerary.attr[austin_itinerary.attr.attraction==temp[locidx]].lon.values[0], placeLat=austin_itinerary.attr[austin_itinerary.attr.attraction==temp[locidx]].lat.values[0],GPH=austin_itinerary.gdcon)
		startN = (startN_temp[0],startN_temp[1])
		endN_temp = austin_itinerary.findClosestNode(placeLon=austin_itinerary.attr[austin_itinerary.attr.attraction==temp[locidx+1]].lon.values[0], placeLat=austin_itinerary.attr[austin_itinerary.attr.attraction==temp[locidx+1]].lat.values[0],GPH=austin_itinerary.gdcon)
		endN = (endN_temp[0],endN_temp[1])
		p=austin_itinerary.getSPNetworkx(startnode=startN, destnode=endN, GPH=austin_itinerary.gdcon)
		p_new = [[list(b) for b in p]]
		austin_itinerary.drawPath(path=p_new,lw=2)
	austin_itinerary.zoomToFit()
			



	

