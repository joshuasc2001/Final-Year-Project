#!/usr/bin/env python
# coding: utf-8

# In[1]:


import networkx as nx
class rotationSystem:

    def __init__(self, vertex, edge):
        """Takes in two lists of tuples of half edges"""
        self.vertex = vertex
        self.edge = edge
        
    def noVertices(self):
        return len(self.vertex)
    
    def noEdges(self):
        return len(self.edge)

    def conversion(self):
        """Converts a list of half edges and a list of half edge pairs into a list of edges to
            be used with networkx"""
        vertices = []
        edges = []
        vertexHalfEdge = {}

        for i in range(len(self.vertex)):  # creates a list of the vertices
            vertexHalfEdge[i] = self.vertex[i]
            vertices.append(i)

        for e in self.edge:
            x, y = e
            for key, value in vertexHalfEdge.items():
                try:
                    if x in value:
                        vertex1 = key
                    if y in value:
                        vertex2 = key
                except:
                    if x == value:
                        vertex1 = key
                    if y == value:
                        vertex2 = key
            edges.append(str(vertex1)+str(vertex2))

        return edges
    

        
    def findRotation(self, list1, x):
        """Find half edge rotation"""
        for l in list1:
            if x in l:
                for i in range(len(l)):
                    if l[i] == x:
                        halfEdge = l[(i+1) % len(l)]
        return halfEdge

    def findEdge(self, list1, x):
        """Find edge permutation"""
        for l in list1:
            if x in l:
                if l[0] == x:
                    return l[1]
                else:
                    return l[0]

    #find walk - for one edge
    def findWalk(self, permutation, edges, o):
        """Find border walk given half edge"""
        #set original half edge
        startEdge = o
        cycleList = [o]
        currentEdge = self.findRotation(permutation, o)
        cycleList.append(currentEdge)
        currentEdge = self.findEdge(edges,currentEdge)
        cycleList.append(currentEdge)
        while currentEdge != o:
            currentEdge = self.findRotation(permutation, currentEdge)
            cycleList.append(currentEdge)
            currentEdge = self.findEdge(edges,currentEdge)
            cycleList.append(currentEdge)
        return cycleList


    def findAllWalks(self):
        ## need to check if graph is connected before finding boundary cycles
        """Find all border walks"""
        G = nx.Graph(self.conversion())
        assert nx.is_connected(G), "Graph is not connected"
            
        checked = []
        cycles = []
        for i in range(len(self.edge)):
            for j in range(2):
                if self.edge[i][j] not in checked:
                    walk = self.findWalk(self.vertex, self.edge, self.edge[i][j])

                    cycles.append(walk)
                    for x in range(0, len(walk),2):
                        checked.append(walk[x])

        for l in cycles:
            for k in cycles:
                if k != l:
                    if set(k) == set(l):
                        cycles.remove(k)

        return cycles
        
             


    def displayBoundaryCycles(self):
        """Displays the number of boundary cycles of each length"""
        cycles = []
        allCycles = []
        walks = self.findAllWalks()
        
        for i in walks:
            allCycles.append(int((len(i)-1)/2)) # walk is made up of 2 half edges for each vertex so need to divide by 2 and take away 1 as first half edge is counted twice
        
        for i in range(max(allCycles)+1):
            counter = 0
            for j in allCycles:
                if j == i:
                    counter +=1
            cycles.append(counter)
        
        for i in range(len(cycles)): #print out number of each cycle
            if cycles[i] != 0: #prevents printing out number of k-cycles if there is no k-cycle 
                print(f"Number of {i}-cycles is: {cycles[i]}")
        
        return 0
                
    
    def displayFaces(self):
        print(f"Number of faces is: {len(self.findAllWalks())}")
        
    
    def findGenus(self):
        return int(1 - 0.5*(self.noVertices() - self.noEdges() + len(self.findAllWalks())))
        


# Basic examples used when describing the methods

# In[2]:


#Running the number of edges and number of vertices method
e = [(1,2),(3,4,5),(6,7),(8,9,10),(11,12)]
v = [(2,3),(5,6),(7,8),(9,4),(10,11),(12,1)]
r = rotationSystem(e,v)

print("Number of edges are:", r.noEdges())
print("Number of vertices are:", r.noVertices())


# In[3]:


#Finding all the boundary walks in the graph
e = [(1,2),(3,4,5),(6,7),(8,9,10),(11,12)]
v = [(2,3),(5,6),(7,8),(9,4),(10,11),(12,1)]
r = rotationSystem(e,v)

r.findAllWalks()
r.displayBoundaryCycles()


# In[4]:


#Finding how many faces are in the graph
e = [(1,2),(3,4,5),(6,7),(8,9,10),(11,12)]
v = [(2,3),(5,6),(7,8),(9,4),(10,11),(12,1)]
r = rotationSystem(e,v)

print("Number of faces are:", r.displayFaces())


# In[5]:


e = [(1,2),(3,4,5),(6,7),(8,9,10),(11,12)]
v = [(2,3),(5,6),(7,8),(9,4),(10,11),(12,1)]
r = rotationSystem(e,v)

print("The genus of the graph is:", r.findGenus())


# Example 1 Code

# In[6]:


#rotation system on torus
v = [(1,6,4,5), (3,2)]
e = [(1,2),(3,4),(6,5)]
r = rotationSystem(v,e)


print("The genus of the graph is:", r.findGenus())
r.displayFaces()


# In[7]:


#rotation system on sphere
v = [(1,4,5,6),(3,2)]
e = [(1,2),(3,4),(6,5)]
r = rotationSystem(v,e)

print("The genus of the graph is:", r.findGenus())
r.displayFaces()


# Example 2 Code

# In[8]:


v = [(1,2,3,4),(34,37,36,35),(30,31,32,33,44),(28,27,29),(26,25,43,42),
     (39,40,41,38),(23,24,21,22),(20,19,18,17),(15,16,14,13),(5,6,7,8,9),
     (10,11,12)]
e = [(1,37),(35,3),(2,44),(33,34),(4,5),(6,36),(13,12),(10,9),(8,18),(11,19),
     (16,17),(7,14),(20,21),(15,22),(24,25),(23,40),(39,43),(26,27),(42,31),
     (38,32),(29,30),(28,41)]
r = rotationSystem(v,e)


# In[9]:


r.displayBoundaryCycles()


# In[10]:


r.findGenus()


# In[11]:


r.displayFaces()


# Example 3

# Example 3 Code

# In[13]:


v = [(1,2,3,4),(5,6,7,8),(9,10,11,12),(13,14,15,16),(17,18,19,20)]
e = [(1,5),(2,12),(3,14),(4,17),(6,9),(7,15),(8,18),(10,16),(11,19),(13,20)]
r = rotationSystem(v,e)
r.findGenus()


# In[14]:


r.displayFaces()


# Example 4

# In[15]:


v = [(1,4,3,2),(5,6,31,22,34),(7,10,9,8),(11,13,12,32),(14,18,17,16,15),(19,21,33,20)]
e= [(4,5),(6,7),(10,11),(13,14),(18,19),(21,1),(3,12),(2,17),(9,15),(8,20),(16,22),(31,32),(33,34)]
r = rotationSystem(v,e)
r.findGenus()


# In[16]:


r.displayFaces()


# In[18]:


r.displayBoundaryCycles()


# In[19]:


r.findAllWalks()


# In[ ]:




