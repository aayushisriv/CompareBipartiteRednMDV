"""
@author-Aayushi Srivastava
Comparison based on number of edges added and run time between Reduction and MDV in Bipartite Graphs.
No graph plotting here, can compare biig graphs.


"""
import networkx as nx 
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
import copy

import operator
import itertools
import random
import timeit
import time

class BipartCh:

	def __init__(self,noNodes1, noNodes2,noEdges):
		self.noNodes1 = noNodes1
		self.noNodes2 = noNodes2
		self.noEdges = noEdges
		self.W = {}
		self.WEdgeList = []
		self.rankList = []
		self.vertexList1 = []
		self.vertexList2 = []
		self.GEdgeList = []
		self.HEdgeList = []
		self.REdgeList = []
		self.G = {}
		self.R = {} #graph for MDV
		self.fd = {}
		self.bta = {}
		self.NEdgeList = []
		self.CEdgeList = []
		self.DEdgeList = []
		self.firstrank = []
		self.H = {} #graph For Reduction
		self.getrank = 0
		self.neb2 = []
		self.rankList1 = []
		self.C2 = {}
		self.C2EdgeList = []
		self.maxv = {}
		self.m_ver1 = 0
		self.maxn = {}
		self.m_ver2 = 0
		self.neb1 = []
		self.neb2 = []
		self.vertexLstcom = []
		self.MEdgeList = []

	def createBipartiteGraph(self):
		self.G = bipartite.gnmk_random_graph(self.noNodes1,self.noNodes2,self.noEdges)

		if type(self.G) is not dict:
			self.G = nx.to_dict_of_lists(self.G)
			#print self.G
		for key,value in self.G.iteritems():
			for v in value:
				if key < v:
					e = []
					e.append(key)
					e.append(v)
					self.GEdgeList.append(e)
		self.G = nx.Graph(self.G)
		#self.checkChain(self.G)
		for i in range (0,self.noNodes1):
			self.vertexList1.append(i)
		for j in range(self.noNodes1,(self.noNodes1+self.noNodes2)):
			self.vertexList2.append(j)
			#print "M list",self.vertexList2
		#self.plotBipartGraph(self.G)
		#self.createChainGraph(self.G)


	def createChainGraph(self,gra):
		self.HEdgeList = copy.deepcopy(self.GEdgeList)
		self.H = copy.deepcopy(self.G)
		print "---START CONVERTING FROM BIPARTITE GRAPH TO CHAIN GRAPH---"
		self.chaindeck(self.vertexList1,self.vertexList2,self.H)
		#self.plotChainGraph(self.G,self.NEdgeList,self.vertexList1,self.vertexList2)
		print "---END CONVERSION FROM BIPARTITE TO CHAIN GRAPH---"
		#self.ChordalProcess(self.H)

	def plotBipartGraph(self, graphpl):
		self.G = nx.Graph(self.G)
		GD = nx.Graph(self.G)
		pos = nx.spring_layout(GD)
		#nx.draw(GD,pos,width=8.0,with_labels=True)
		nx.draw_networkx_nodes(GD,pos, width = 1)
		nx.draw_networkx_edges(GD, pos, width=1.2, alpha=0.5)
		nx.draw_networkx_labels(GD,pos)
		plt.draw()
		plt.show()


	def chaindeck(self,firstdi,seconddi,graphChain):
		self.H = nx.Graph(self.H)
		#print "GList",self.vertexList1
		dv = self.H.degree(self.H)
		#print "See Degree list",dv
		dvdict = dict(dv)
		#print "Dictinary of node-degree",dvdict
		self.fd =  sorted(dvdict.items(), key=lambda kv:(kv[1],kv[0]))
		#print "Sorted node-degree dictionary",self.fd
		for i in self.fd:
			if i[0] in self.vertexList1:
				#print "Found",i[0]
				self.firstrank.append((i[0],i[1]))
				#print "my new liste", self.firstrank
			elif i[0] not in self.vertexList2:
				#print "Not found",i[0]
				pass
		rdi = dict(self.firstrank)
		#print "Phir le aaya",rdi
		self.bta = sorted(rdi.items(), key=lambda kv:(kv[1],kv[0]))
		#print "Ranking on index:",self.bta
		#print type(self.G)
		for x in self.bta:
			
			ind = self.bta.index(x)
			#print "Ranks are below:"
			#print "Node---Rank (for first part)"
			#print x[0],":",ind
			self.rankList1.append((x[0],ind))
		#print "My first side nodes with ranks",self.rankList1
		#print "My second vertex list",self.vertexList2
		
		for v2 in self.vertexList2:
			abc = []
			self.neb2 = list(self.H.neighbors(v2))
			if self.neb2:
				#print "Neighbors of",v2,"are:",self.neb2
				for y in self.rankList1:
					for j in self.neb2:
						if j == y[0]:
							#print "My checks",j,y
							abc.append((y[0],y[1]))
							#print "ABC",abc
							#print "ver",y[0]
							self.getrank = max(abc, key = lambda i:i[1])[1]
							#print type(getrank)
				#print type(self.H)
				self.H = nx.Graph(self.H)
				#print "We found the rank for:",v2,"as:",self.getrank
				#print "See list of all ranked neighbours of:",v2,"here",abc
				#print "Node---Rank (for second part)"
				#print v2, ":", self.getrank
				#print self.rankList1
				#for k in self.rankList1:
					#if self.getrank == k[1]:
						#print "Hey found Rank of ",v2, k[1]
				for y in self.rankList1:
					if self.getrank > y[1]:
						#if self.H.has_edge(v2,y[0]):
							#print "Already edge is there between",v2, "and",k[0]
							#pass
						if not self.H.has_edge(v2,y[0]):
							self.H.add_edge(v2,y[0])
							self.NEdgeList.append((v2,y[0]))
							#print "Edge added between:", v2, "and", y[0]
						#elif self.getrank <  y[1]:
							#print "Not seen"
						#	pass
					#print "New edge list",self.NEdgeList
			#if not self.neb2:
				#print "No neighbors of the vertex",v2
			#	pass
					
					
		#print "New edge list",self.NEdgeList		
		#print "Total Edges added to Bipartite Graph to make it Chain graph:",len(self.NEdgeList)
		self.H = nx.to_dict_of_lists(self.H)
		#print "Changed",self.H
		self.H = nx.Graph(self.H)
		#vertexlist = vertexlist + vertexList2	
		
		


	"""	
	def plotChainGraph(self,graphPlot,newEdgeList,vertexList1,vertexList2):
		GD = nx.Graph(self.G)
		pos = nx.spring_layout(GD)
		F = copy.deepcopy(self.G)
		F.add_edges_from(newEdgeList)
		F = nx.to_dict_of_lists(F)
		print "Final chain Graph",F
		#vertexlist = vertexlist + vertexList2
		nx.draw_networkx_nodes(GD, pos, nodelist=(vertexList1 + vertexList2), node_color='red', node_size=300, alpha=0.8)
		#nx.draw_networkx_nodes(GD, pos, nodelist=NEdgeList, node_color='r', node_size=500, alpha=0.8)
			
		nx.draw_networkx_edges(GD, pos, width=1.0, alpha=0.5)
		nx.draw_networkx_edges(GD, pos, edgelist=newEdgeList, width=3.0, alpha=0.5, edge_color='blue')
		nx.draw_networkx_labels(GD,pos)
		plt.draw()
		#plt.show()
		plt.show(block = False)
		self.G = nx.Graph(self.G)
		GD = nx.Graph(self.G)
		pos = nx.spring_layout(GD)
		nx.draw(GD,pos,width=8.0,with_labels=True)
		plt.draw()
		plt.show()
    """
	def ChordalProcess(self):
		#start = time.time()
		starttime = timeit.default_timer()
		self.W = copy.deepcopy(self.H)
		self.WEdgeList = copy.deepcopy(self.HEdgeList)

		print "---START CONVERTING FROM CHAIN GRAPH TO CHORDAL GRAPH"
		#self.ChordalGraph(self.W,self.vertexList1,self.vertexList2)
		self.createChainGraph(self.G)
		self.Chordal2(self.C2, self.vertexList1, self.vertexList2)
		#self.plotChordalGraph(self.C2,self.CEdgeList,self.DEdgeList,self.vertexList1,self.vertexList2)
		print "---END CONVERSION FROM CHAIN TO CHORDAL GRAPH"
		print "Total Edges added in Reduction Method: ", len(self.CEdgeList + self.DEdgeList)
		#end = time.time()
		#print "Runtime of Reduction Method is:", {end - start}--epoch
		#print (timeit.timeit(self.ChordalProcess(), number = 10000))
		print "Runtime of Reduction method:",timeit.default_timer() - starttime
			
	
	def Chordal2(self, graph2, vert1, vert2):
		self.C2 = copy.deepcopy(self.H)
		self.C2EdgeList = copy.deepcopy(self.HEdgeList)
		#print "First one", vert1
		#print "Second one", vert2
		#for v in vert1:
		#print type(self.H)
		self.H = nx.Graph(self.H)
		dv = list(self.C2.degree(vert1)) #list of tuples
		#print "Make deg",dv
		#dv = list(graphtoCons.degree(graphtoCons)) 
		#print "see the  degree list:"
		#print dv
		#print self.HEdgeList
		dvdict = dict(dv)
		#print "Dictionary of node-degree is", dvdict
		self.maxv = dict(sorted(dvdict.items(), key=lambda kv:(kv[1], kv[0])))
		#print "Sorted dictionary of node-degree:",self.maxv
		self.m_ver1 = max(self.maxv.keys(), key=(lambda k:self.maxv[k]))
		#print type(self.m_ver1)
		#print "Vertex of Maximum Degree is:",self.m_ver1
		self.neb1 = list(self.H.neighbors(self.m_ver1))
		#print "Neighbors of the chosen vertex are:",self.neb1
		nebcomb1 = list(itertools.combinations(self.neb1,2))
		#print "See combinations of first side:",nebcomb1
		for p in nebcomb1:
			#print p
			self.C2.add_edges_from(nebcomb1)
			self.CEdgeList.append(p)
		#print "My List for vertex1", self.CEdgeList
		#print "Edges added in first part of graph to make it chordal",len(self.CEdgeList)
		neblen = len(self.neb1)
		#for n in vert2:
			#print type(self.H)
		self.H = nx.Graph(self.H)
		nv = list(self.C2.degree(vert2)) #list of tuples
		#dv = list(graphtoCons.degree(graphtoCons)) 
		#print "see the  degree list:"
		#print nv
		#print self.HEdgeList
		nvdict = dict(nv)
		#print "Dictionary of node-degree is", nvdict
		self.maxn = dict(sorted(nvdict.items(), key=lambda kv:(kv[1], kv[0])))
		#print "Sorted dictionary of node-degree:",self.maxn
		self.m_ver2 = max(self.maxn.keys(), key=(lambda k:self.maxn[k]))
		#print type(self.m_ver2)
		#print "The chosen vertex of maximum degree", self.m_ver2
		self.neb2 = list(self.H.neighbors(self.m_ver2))
		#print "Neighbors of the chosen vertex are:",self.neb2
		nebcomb2 = list(itertools.combinations(self.neb2,2))
		#print "See combinations of second side:",nebcomb2
		for q in nebcomb2:
			#print q
			self.C2.add_edges_from(nebcomb2)
			self.DEdgeList.append(q)
		#print "My List for vertex2",self.DEdgeList
		#print "Edges added in second part of graph to make it chordal",len(self.DEdgeList)
		#print "Total edges added to chain graph to make it chordal:",(len(self.CEdgeList) + len(self.DEdgeList))




	def plotChordalGraph(self,graphPlot,newEdgeList1,newEdgeList2,vertexList1,vertexList2):
		GD = nx.Graph(self.H)
		pos = nx.spring_layout(GD)
		J = copy.deepcopy(self.H)
		J.add_edges_from(newEdgeList1 + newEdgeList2)
		print "Total Edges added in Reduction: ",(newEdgeList1 + newEdgeList2)
		J = nx.to_dict_of_lists(J)
		#print "Final chain Graph",J
		#vertexlist = vertexlist + vertexList2
		nx.draw_networkx_nodes(GD, pos, nodelist=(vertexList1 + vertexList2), node_color='red', node_size=300, alpha=0.8)
		#nx.draw_networkx_nodes(GD, pos, nodelist=NEdgeList, node_color='r', node_size=500, alpha=0.8)
			
		nx.draw_networkx_edges(GD, pos, width=1.0, alpha=0.5)
		nx.draw_networkx_edges(GD, pos, edgelist=newEdgeList1, width=3.0, alpha=0.5, edge_color='blue')

		nx.draw_networkx_edges(GD, pos, width=1.0, alpha=0.5)
		nx.draw_networkx_edges(GD, pos, edgelist=newEdgeList2, width=3.0, alpha=0.5, edge_color='green')
		nx.draw_networkx_labels(GD,pos)
		plt.draw()
		#plt.show()
		plt.show()
		

		#Recognition
		self.C2 = nx.Graph(self.C2)
		graph = nx.Graph(self.C2)
		if nx.is_chordal(graph):
			print "BGraph: IT IS CHORDAL"
		else:
			print "Graph: NO IT IS NOT CHORDAL"
	
	def createChrdG(self):
		#start = time.time()
		starttime = timeit.default_timer()
		self.REdgeList = copy.deepcopy(self.GEdgeList)
		self.R = copy.deepcopy(self.G)
		self.R = nx.Graph(self.R)
		self.vertexLstcom = self.vertexList1 + self.vertexList2
		#print "Entire vertexlist : ",self.vertexLstcom

		print "Start Minimum Vertex Process"
		self.Minvertex(self.vertexLstcom,self.REdgeList,self.R)
		#self.FinalGraph(self.G,self.MEdgeList,self.vertexLstcom)
		print "End Minimum Vertex Process"
		#return True
		#self.FinalGraph(self.G,self.NEdgeList,self.vertexList)
		print "Total Edges added in MDV: ",len(self.NEdgeList)
		#end = time.time()
		#print (timeit.timeit(self.createChrdG(), number = 1))
		#print "Runtime of MDV:", {end - start}--Epoch
		print "Runtime of MDV:",timeit.default_timer() - starttime #seconds

	def Minvertex(self,vertexList,edgeList, graphtoCons):
		graphtoCons = nx.Graph(graphtoCons)
		self.R = nx.Graph(self.R)
		#isChordal = False
		#self.H = nx.Graph(self.H)
		random.shuffle(vertexList)
		self.R = nx.Graph(self.R)
		for v in vertexList:
			#print "check type"
			#print type(self.H)
			self.R = nx.Graph(self.R)
			dv = list(self.R.degree(self.R)) #list of tuples
			#print "see the list:"
			#print dv
		
			dvdict = dict(dv)
			#print "Dictionary of node-degree is", dvdict
			self.minv = dict(sorted(dvdict.items(), key=lambda kv:(kv[1], kv[0])))
			#print "Sorted dictionary of node-degree:",self.minv
			self.R = nx.to_dict_of_lists(self.R)
			#print "The dictionary looks like:", self.H
			mincp = copy.deepcopy(self.minv)
			try:
				for key,value in mincp.iteritems():
					if value < 2:
				#del minv[key]
						self.minv.pop(key)
				#print "Deleted"
				#print "Updates:",self.minv
				graphtoCons = nx.Graph(graphtoCons)
				self.R = nx.Graph(self.R)
				nodeH = self.R.nodes()
				#print "Old Nodes are:",nodeH
				#print "New nodes are",list(self.minv)
				self.R.add_nodes_from(list(self.minv))
				self.R.remove_nodes_from(list(list(set(nodeH) - set(list(self.minv)))))
				self.R = nx.to_dict_of_lists(self.R)
				#print "New Dictionary:",self.H
				self.m_vert = min(self.minv.keys(), key=(lambda k:self.minv[k]))
				#print type(self.m_vert)
				#print "Minimum degree vertex is:",self.m_vert
				#print type(self.H)
				self.R = nx.Graph(self.R)
				#self.H = nx.Graph(self.H)
				#print "The chosen Minimum vertex is", self.m_vert
				
				self.neb = list(self.R.neighbors(self.m_vert))
				#print "Neighbors of the chosen vertex are:",self.neb
				neblen = len(self.neb)
				
				self.R = nx.Graph(self.R)
				self.R.remove_node(self.m_vert)
				self.neighbcomp(self.m_vert,self.R)

				self.R = nx.Graph(self.R)
			except ValueError as e:
				#print "Dictionary is Empty now"
				break

		#self.FinalGraph(self.G,self.NEdgeList,self.vertexList)

	def neighbcomp(self,chosvert,graphtoRecreate):
		#eb = 0
		self.R = nx.Graph(self.R)
		nebcomb = list(itertools.combinations(self.neb,2))
		#print "See combinations:",nebcomb
		for p in nebcomb:
			v1 =  p[0]
			v2 = p[1]
			#print p
			if self.R.has_edge(*p) :
				#print p
				#print "Already edge is there"
				continue
			else:
				self.R.add_edge(*p)
				#print "Check this"
				self.MEdgeList.append(p)
				#print "My list", self.NEdgeList
				continue
		#print "Edges added using Minimum Degree",len(self.MEdgeList)

		self.R = nx.to_dict_of_lists(self.R)
		#print "See change",self.H
		#self.graphtoRecreate = nx.to_dict_of_lists(graphtoRecreate)

		
	

	def FinalGraph(self,graphVerify,newaddedgelist,vertexlist):
		print "EdgeList verifying",newaddedgelist
		print "Total Edges added in Minimum Degree Process is ",len(newaddedgelist)
		GD = nx.Graph(self.G)
		pos = nx.spring_layout(GD)

		B = copy.deepcopy(self.G)
		B = nx.Graph(B)
		B.add_nodes_from(vertexlist)
		B.add_edges_from(newaddedgelist)
		B = nx.to_dict_of_lists(B)
		print "see B", B
		##Recognition----
		graph = nx.Graph(B)
		print type(B)
		if nx.is_chordal(graph):
			print "IT IS CHORDAL"
		else :
			print "NO IT IS NOT CHORDAL"
		#print "Draw graph"
		nx.draw_networkx_nodes(GD, pos, nodelist=vertexlist, node_color='red', node_size=300, alpha=0.8,label='Min degree')	
		nx.draw_networkx_edges(GD, pos, width=1.0, alpha=0.5)
		nx.draw_networkx_edges(GD, pos, edgelist=newaddedgelist, width=8.0, alpha=0.5, edge_color='blue',label='Min degree')
		nx.draw_networkx_labels(GD,pos)
		plt.draw()
		plt.show()	

	
	def plotWhole(self,graphTe, graphnum):
		if graphnum == 1:
			self.plotBipartGraph(self.G)
		elif graphnum == 2:
			self.plotChordalGraph(self.G,self.CEdgeList,self.DEdgeList,self.vertexList1,self.vertexList2)
		elif graphnum == 3:
			self.FinalGraph(self.C2,self.MEdgeList,self.vertexLstcom)
	
	#print "Total Edges added in Reduction: ",
	

	#print (timeit.timeit(self.createChrdG(), number = 10000))


val1 = int(raw_input("Enter no. of nodes in first part of graph:"))
val2 = int(raw_input("Enter no. of nodes in second part of graph:"))
val3 = int(raw_input("Enter no. of edges:"))
gvert = BipartCh(val1,val2,val3)
gvert.createBipartiteGraph() 
gvert.ChordalProcess()
gvert.createChrdG() 



			








