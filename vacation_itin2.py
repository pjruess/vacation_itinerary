""" 
Module for finding the optimal vacation itinerary schedule based on the savings algorithm.

"""

import scipy
import pandas
import networkx
from geoplotter import *
import matplotlib.pyplot

TIME_VALUE_OF_MONEY = 12.
SAMPLE_SIZE = 5

class vacation_itinerary:

	def __init__(self,city_file,attractions_file,**kwargs):
		# reads road network file
		self.ds = pandas.read_csv(city_file)
		# reads attraction address file
		self.attr = pandas.read_csv(attractions_file)
		self.initial_itinerary = ['hotel']
		self.initial_itinerary.extend(self.attr.attraction.values)
		# creates GeoPlotter object
		self.DSmap = GeoPlotter()
		# creates networkx graph
		self.createNetworkxGraph()


	def identifyStartPoints(self,df,exp):
	    startPts = df.LINESTRING.str.extract('LINESTRING \(([0-9-.]* [0-9-.]*),',expand=exp)
	    return startPts
	        
	def identifyEndPoints(self,df,exp):
	    endPts = df.LINESTRING.str.extract(', ([0-9-.]* [0-9-.]*)\)',expand=exp)
	    return endPts
	    

	# creates the networkx graph for the road network
	def createNetworkxGraph(self): 
        #creates a networkx graph
	    self.gd = networkx.DiGraph()

	    # Sets up edge sets 
	    # F Streets
	    self.Fds = self.ds[self.ds.oneway=='F']
	    self.FstartPTS = self.identifyStartPoints(df=self.Fds,exp=False)
	    self.FendPTS = self.identifyEndPoints(df=self.Fds,exp=False)
	    
	    # T Streets
	    self.Tds = self.ds[self.ds.oneway=='T']
	    self.TstartPTS = self.identifyStartPoints(df=self.Tds,exp=False)
	    self.TendPTS = self.identifyEndPoints(df=self.Tds,exp=False)
	    
	    # B Streets
	    self.Bds = self.ds[self.ds.oneway=='B']
	    self.BstartPTS = self.identifyStartPoints(df=self.Bds,exp=False)
	    self.BendPTS = self.identifyEndPoints(df=self.Bds,exp=False)

	    # Simplification - all roads speed = 50mph, D=RT
	    timeF = self.Fds.miles.values/50.
	    self.F_dict = [dict(time=mi) for mi in timeF]
	    timeT = self.Tds.miles.values/50.
	    self.T_dict = [dict(time=mi) for mi in timeT]
	    timeB = self.Bds.miles.values/50.
	    self.B_dict = [dict(time=mi) for mi in timeB]

	    # add F streets        
	    F_edges = zip(list(self.FstartPTS.values), list(self.FendPTS.values),self.F_dict)
	    self.gd.add_edges_from(F_edges)
	    
	    # add T streets
	    T_edges = zip(list(self.TendPTS.values), list(self.TstartPTS.values),self.T_dict)
	    self.gd.add_edges_from(T_edges) 
	    
	    # add B streets
	    B_edges1 = zip(list(self.BstartPTS.values), list(self.BendPTS.values),self.B_dict)
	    B_edges2 = zip(list(self.BendPTS.values), list(self.BstartPTS.values),self.B_dict)
	    self.gd.add_edges_from(B_edges1) 
	    self.gd.add_edges_from(B_edges2)

	    # gets the connected subgraphs of the networkx graph and finds the subgraph with the largest number of edges
	    gdcon_temp = list(networkx.strongly_connected_component_subgraphs(self.gd,copy=True))
	    temp_edge_length = scipy.array([len(p.edges()) for p in gdcon_temp])
	    idx = scipy.where(temp_edge_length==max(temp_edge_length))[0][0]
	    self.gdcon = gdcon_temp[idx]


	# finds the shortest path between two nodes using Dijkstra's algorithm in networkx
	def getSPNetworkx(self,startnode,destnode,GPH):
		return networkx.shortest_path(GPH,source=startnode,target=destnode,weight='time')


	# plots street network using geoplotter
	def drawStreetNetwork(self,GPH):
		# extracts line segment points
		maplinestemp = self.ds.LINESTRING.str.extract('LINESTRING \(([0-9-.]* [0-9-.]*, [0-9-.]* [0-9-.]*)\)',expand=True)
		maplinestemp.columns = ['TotLine']
		# separates out points and reformats to feed into drawLines from geoplotter
		temp = [r.split(',') for r in maplinestemp.TotLine.values]
		stLines = [[[float(dw) for dw in p.split()] for p in g] for g in temp]		
		self.DSmap.drawLines(lines = stLines,color = 'b',linewidth = 0.3)		
		

	# plots address(es) - addresLon and addressLat can be lists
	def drawAddress(self,addressLon,addressLat,marksz=75,co='r'):
		self.DSmap.drawPoints(lat=addressLat,lon=addressLon,color=co,s=marksz)


	# draws the path
	def drawPath(self,path,lw=2.5):
		stLines = [[[float(dw) for dw in g.split()] for g in path]]
		self.DSmap.drawLines(lines = stLines,color = 'y',linewidth = lw,alpha = 1)


	# draws the itinerary path
	def drawItineraryPath(self,itin):
		for locidx in range(len(itin)-1):
			startN = self.findClosestNode(placeLon=self.attr[self.attr.attraction==itin[locidx]].lon.values[0], placeLat=self.attr[self.attr.attraction==itin[locidx]].lat.values[0],GPH=self.gdcon)[0]
			endN = self.findClosestNode(placeLon=self.attr[self.attr.attraction==itin[locidx+1]].lon.values[0], placeLat=self.attr[self.attr.attraction==itin[locidx+1]].lat.values[0],GPH=self.gdcon)[0]
			p=self.getSPNetworkx(startnode=startN, destnode=endN, GPH=self.gdcon)
			self.drawPath(path=p)


	# formats map
	def zoomToFit(self):
		# gets range of longitude and latitude w.r.t. the attractions and zooms map
		lonLatRan = self.getLonLatRange()
		margin = 0.05
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

	    nodesNM_set = [r.split(',') for r in self.gdcon.nodes_iter()]
	    stLines = [[[float(dw) for dw in p.split()] for p in g] for g in nodesNM_set]
	    listLon = scipy.array([u[0][0] for u in stLines])
	    listLat = scipy.array([u[0][1] for u in stLines])

	    while pos_nodes_zero==True and ((latdf<scipy.absolute(latRange[0]-latRange[1])/2) and (londf<scipy.absolute(lonRange[0]-lonRange[1]))):
	        pos_nodes = scipy.array([])
	        nodesNM_set = [r.split(',') for r in self.gdcon.nodes_iter()]
	        ct = ct + 1
	        latidx1 = scipy.where((listLat<placeLat+ct*latdf))
	        tempLatList = listLat[latidx1]
	        tempLonList = listLon[latidx1]
	        nodesNM_set = [nodesNM_set[b] for b in latidx1[0]]
	        latidx = scipy.where(tempLatList>placeLat-ct*latdf)
	        tempLatList = tempLatList[latidx]
	        tempLonList = tempLonList[latidx]
	        nodesNM_set = [nodesNM_set[c] for c in latidx[0]]
	        lonidx1 = scipy.where(tempLonList>placeLon-ct*londf)
	        tempLatList = tempLatList[lonidx1]
	        tempLonList = tempLonList[lonidx1]
	        nodesNM_set = [nodesNM_set[d] for d in lonidx1[0]]
	        lonidx = scipy.where(tempLonList<placeLon+ct*londf)
	        pos_nodes = scipy.array([tempLonList[lonidx],tempLatList[lonidx]])
	        nodesNM_set = [nodesNM_set[e] for e in lonidx[0]]
	        if len(pos_nodes[0])!=0:
	        	pos_nodes_zero = False
	    
	    if len(pos_nodes)==0:
	        return None
	    else:
	        dist = scipy.sqrt(scipy.sum(scipy.array([pos_nodes[0]-placeLon, pos_nodes[1]-placeLat])**2,axis=0))
	        # recall, [lon, lat]
	        idxCN = scipy.where(dist==min(dist))[0][0]
	        closeNode = [pos_nodes[0][idxCN], pos_nodes[1][idxCN]]	    
	        # name of the closest node
	        closeNodeNM = nodesNM_set[idxCN][0]
	        return [closeNodeNM, closeNode]
	

	# finds the total reward given an itinerary
	def getItineraryReward(self,itin):
		#print itin

		# calculates reward for visiting all the attractions in the itinerary
		# reward is in terms of USD
		attr_reward_temp = [self.attr[(self.attr.attraction == nm)].rating.values[0]*10. for nm in itin if (nm != 'hotel')]
		attr_reward = scipy.sum(attr_reward_temp)

		time_reward_temp = [networkx.shortest_path_length(self.gdcon, source=self.findClosestNode(placeLon=self.attr[self.attr.attraction==itin[p]].lon.values[0],placeLat=self.attr[self.attr.attraction==itin[p]].lat.values[0],GPH=self.gdcon)[0], target=self.findClosestNode(placeLon=self.attr[self.attr.attraction==itin[p+1]].lon.values[0],placeLat=self.attr[self.attr.attraction==itin[p+1]].lat.values[0],GPH=self.gdcon)[0], weight='time') for p in range(len(itin)-1)]
		time_reward = scipy.sum(time_reward_temp)*TIME_VALUE_OF_MONEY*(-1)
		#print 'Time Reward (Negative) = ', time_reward
		

		"""
		self.drawStreetNetwork(GPH=self.gd)
		
		for h in range(len(itin)):
			temp1 = [self.attr[self.attr.attraction==itin[h]].lon.values[0],self.attr[self.attr.attraction==itin[h]].lat.values[0]]
			
			#self.drawAddress(addressLon=temp1[0],addressLat=temp1[1],co='g')
			#temp1_closeN = self.findClosestNode(placeLon=temp1[0],placeLat=temp1[1],GPH=self.gdcon)[1]
			#self.drawAddress(addressLon=temp1_closeN[0],addressLat=temp1_closeN[1],co='m')
			
			if h==17:
				self.drawAddress(addressLon=temp1[0],addressLat=temp1[1],co='r')
				temp1_closeN = self.findClosestNode(placeLon=temp1[0],placeLat=temp1[1],GPH=self.gdcon)[1]
				self.drawAddress(addressLon=temp1_closeN[0],addressLat=temp1_closeN[1],co='m')
			elif h==18:
				self.drawAddress(addressLon=temp1[0],addressLat=temp1[1],co='c')
				temp1_closeN = self.findClosestNode(placeLon=temp1[0],placeLat=temp1[1],GPH=self.gdcon)[1]
				self.drawAddress(addressLon=temp1_closeN[0],addressLat=temp1_closeN[1],co='m')
			else:
				self.drawAddress(addressLon=temp1[0],addressLat=temp1[1],co='g')
				temp1_closeN = self.findClosestNode(placeLon=temp1[0],placeLat=temp1[1],GPH=self.gdcon)[1]
				self.drawAddress(addressLon=temp1_closeN[0],addressLat=temp1_closeN[1],co='m')
		"""

		return attr_reward + time_reward

	# calculates total travel time
	def getTotalTravelTime(self,itin):
		time_reward_temp = [networkx.shortest_path_length(self.gdcon, source=self.findClosestNode(placeLon=self.attr[self.attr.attraction==itin[p]].lon.values[0],placeLat=self.attr[self.attr.attraction==itin[p]].lat.values[0],GPH=self.gdcon)[0], target=self.findClosestNode(placeLon=self.attr[self.attr.attraction==itin[p+1]].lon.values[0],placeLat=self.attr[self.attr.attraction==itin[p+1]].lat.values[0],GPH=self.gdcon)[0], weight='time') for p in range(len(itin)-1)]
		return scipy.sum(time_reward_temp)


	# calculates total travel time and time spent at all attractions (does not include travel time back to hotel)
	def getTotalTime(self,itin):
		time_reward_temp = [networkx.shortest_path_length(self.gdcon, source=self.findClosestNode(placeLon=self.attr[self.attr.attraction==itin[p]].lon.values[0],placeLat=self.attr[self.attr.attraction==itin[p]].lat.values[0],GPH=self.gdcon)[0], target=self.findClosestNode(placeLon=self.attr[self.attr.attraction==itin[p+1]].lon.values[0],placeLat=self.attr[self.attr.attraction==itin[p+1]].lat.values[0],GPH=self.gdcon)[0], weight='time') for p in range(len(itin)-1)]
		return scipy.sum(time_reward_temp) + 2*(len(itin))


	def solve_optimal_itinerary(self,itin):

		# Select n random attractions later in the list to node in question
		maxCost = self.getItineraryReward(itin=itin)
		itinTemp = list(itin)
		# counter for item in itinerary
		i = 1
		totTime = 0
		while totTime<12 and i < len(itin):
			switchIdx = i
			print 'i = ', i
			rand_attr = scipy.random.randint(low=i, high=len(itin)-1, size=SAMPLE_SIZE)
			for j in rand_attr:
				itinTemp[i], itinTemp[j] = itinTemp[j], itinTemp[i]
				tempCost = self.getItineraryReward(itin=itinTemp)
				if tempCost > maxCost:
					maxCost = tempCost
					switchIdx = j
				itinTemp = list(itin)
			itin[i], itin[switchIdx] = itin[switchIdx], itin[i]
			totTime = self.getTotalTime(itin=itin[0:i])
			print 'reward = ', maxCost
			print 'totTime = ', totTime
			print
			i = i + 1			

		itinFinal = itin[0:i-1]
		itinFinal.extend(['hotel'])
		return itinFinal


	# draw the attractions and paths for the optimal itinerary
	def draw_optimal_itinerary(self,opt_itin):
		# draws path for the optimal itinerary
		for locidx in range(len(opt_itin)-1):
			startN = austin_itinerary.findClosestNode(placeLon=austin_itinerary.attr[austin_itinerary.attr.attraction==temp[locidx]].lon.values[0], placeLat=austin_itinerary.attr[austin_itinerary.attr.attraction==temp[locidx]].lat.values[0],GPH=austin_itinerary.gdcon)[0]
			endN = austin_itinerary.findClosestNode(placeLon=austin_itinerary.attr[austin_itinerary.attr.attraction==temp[locidx+1]].lon.values[0], placeLat=austin_itinerary.attr[austin_itinerary.attr.attraction==temp[locidx+1]].lat.values[0],GPH=austin_itinerary.gdcon)[0]
			p=austin_itinerary.getSPNetworkx(startnode=startN, destnode=endN, GPH=austin_itinerary.gdcon)
			austin_itinerary.drawPath(path=p,lw=2)

		# draws the attractions
		self.draw_all_attractions(itin=opt_itin)


	# draws all attractions as a red dot on the map
	def draw_all_attractions(self,itin,closestNode=True):
		attr_lon = [self.attr[self.attr.attraction==h].lon.values[0] for h in itin]
		attr_lat = [self.attr[self.attr.attraction==h].lat.values[0] for h in itin]
		if closestNode==True:
			nodes_temp = scipy.array([self.findClosestNode(placeLon=self.attr[self.attr.attraction==h].lon.values[0],placeLat=self.attr[self.attr.attraction==h].lat.values[0],GPH=self.gdcon)[1] for h in itin])
			attr_lon = nodes_temp[:,0]
			attr_lat = nodes_temp[:,1]
		self.DSmap.drawPoints(lat=attr_lat[0],lon=attr_lon[0],color='m',s=75)
		self.DSmap.drawPoints(lat=attr_lat[1:],lon=attr_lon[1:],color='r',s=75)


if __name__ == '__main__':
	austin_itinerary = vacation_itinerary(city_file='austin_edges.csv',attractions_file='austin_nodes.csv')
	optimalItin = austin_itinerary.solve_optimal_itinerary(itin=austin_itinerary.initial_itinerary)
	print optimalItin
	print 'total reward: ', austin_itinerary.getItineraryReward(itin=optimalItin)
	austin_itinerary.drawStreetNetwork(GPH=austin_itinerary.gd)
	austin_itinerary.drawItineraryPath(itin=optimalItin)
	austin_itinerary.draw_all_attractions(itin=optimalItin)
	#matplotlib.pyplot.savefig('optimal_itinerary.png')
	austin_itinerary.zoomToFit()
	



	

