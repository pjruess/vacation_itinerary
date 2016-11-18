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

		# creates networkx graph
		self.createNetworkxGraph()

	# creates the networkx graph for the road network
	def createNetworkxGraph(self): 

        #creates a networkx graph
	    self.gd = networkx.DiGraph()

	    # F Streets
	    self.Fds = self.ds[self.ds.oneway=='F']
	    self.FstartPTS = zip(str(self.Fds.startlon.values).strip('[]').split(), str(self.Fds.startlat.values).strip('[]').split())
	    self.FendPTS = zip(str(self.Fds.endlon.values).strip('[]').split(), str(self.Fds.endlat.values).strip('[]').split())

	    # T Streets
	    self.Tds = self.ds[self.ds.oneway=='T']
	    self.TstartPTS = zip(str(self.Tds.startlon.values).strip('[]').split(), str(self.Tds.startlat.values).strip('[]').split())
	    self.TendPTS = zip(str(self.Tds.endlon.values).strip('[]').split(), str(self.Tds.endlat.values).strip('[]').split())

	    # B Streets
	    self.Bds = self.ds[self.ds.oneway=='B']
	    self.BstartPTS = zip(str(self.Bds.startlon.values).strip('[]').split(), str(self.Bds.startlat.values).strip('[]').split())
	    self.BendPTS = zip(str(self.Bds.endlon.values).strip('[]').split(), str(self.Bds.endlat.values).strip('[]').split())

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
	temp = austin_itinerary.attr.attraction.values
	print temp
	austin_itinerary.getItineraryReward(itin=temp)

