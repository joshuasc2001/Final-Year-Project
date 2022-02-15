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
        """Find all border walks"""
        checked = []
        cycles = []
        for i in range(len(self.edge)):
            for j in range(2):
                if self.edge[i][j] not in checked:
                    walk = self.findWalk(self.vertex, self.edge, self.edge[i][j])
                    
                    cycles.append(walk)
                    for x in range(0, len(walk),2):
                        checked.append(walk[x])
                    # print(checked)
        for l in cycles:
            for k in cycles:
                if k != l:
                    if set(k) == set(l):
                        cycles.remove(k)
                        
        return cycles

    def noCycles(self):
        """Returns a list with the number of each cycle"""
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
        
        return cycles
                
    #may change to replace 0,1,2,3,4,...-cycles to their actual names
    def displayCycles(self):
        """Displays the number of cycles """
        for i in range(len(self.noCycles())): #print out number of each cycle
            if self.noCycles()[i] != 0: #prevents printing out number of k-cycles if there is no k-cycle 
                print(f"Number of {i}-cycles is: {self.noCycles()[i]}")
    
    def noFaces(self):
        return len(self.findAllWalks())
        
    def displayFaces(self):
        print(f"Number of faces is: {self.noFaces()}")

    def findGenus(self):
        return (1 - 0.5*(self.noVertices() - self.noEdges() + self.noFaces()))
        
        
