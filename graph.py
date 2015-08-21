"""
Filename: graph.py
Name: SRINIVASAN NAMBI
ID:   800861816
email: snambi@uncc.edu
Project 2 - Shortest Paths in a Network
ITCS 6114 - Algorithms and Data Structures
"""
import argparse
import sys
import operator
from Queue import *

"""Implement a Priority Queue with a min binary heap. This ensures the running time of Dijkstra's algorithm is O((V+E)Log V)"""
class PriorityQueue(object):
    def __init__(self):
        self.vertex_list = []
        
    """Add element method called from Graph class to insert the vertices into min heap"""
    def addElements(self,vertices_list):
        for key,value in vertices_list.items():
            if value.upFlag == True:
                self.heapInsert(value)
                
    def heapInsert(self,value):
        self.vertex_list.append(value)
        self.shiftDown(0, len(self.vertex_list)-1)
        
    """Move the element to the right position in the min heap"""
    def shiftDown(self, start, end):
        newelement = self.vertex_list[end]
        while end  > start:
            index = (end-1)/ 2
            parent = self.vertex_list[index]
            if newelement < parent:
                self.vertex_list[end] = parent
                end = index
                continue
            break
        self.vertex_list[end] = newelement
        
    def extractMin(self):
        """Pop the smallest item off the Priority Queue"""
        lastelt = self.vertex_list.pop()    
        if self.vertex_list:
            returnitem = self.vertex_list[0]
            self.vertex_list[0] = lastelt
            """Call Min-heapify after popping up the smallest element from heap"""
            self.shiftUp(0)
        else:
            returnitem = lastelt
        return returnitem
    
    """Finds the vertex in the min heap and moves it up to place in correct position
        Called by the Dijkstra's algorithm. Running time is O(log n)"""
    def decreaseKey(self,vertexValue):
        keyindex = self.vertex_list.index(vertexValue)
        while keyindex >0 and self.vertex_list[(keyindex-1)/2]> self.vertex_list[keyindex]:
            temp = self.vertex_list[keyindex]
            self.vertex_list[keyindex] = self.vertex_list[(keyindex-1)/2]
            self.vertex_list[(keyindex-1)/2] = temp
            keyindex= (keyindex-1)/2

    """Called after popping up the smallest element from the min heap i.e the root element
        Restores the heap property .min-heapify algorithm"""
    def shiftUp(self, pos):
        endpos = len(self.vertex_list)
        startpos = pos
        newitem = self.vertex_list[pos]
        # Bubble up the smaller child until hitting a leaf.
        childpos = 2*pos + 1    
        while childpos < endpos:
            # Set childpos to index of smaller child.
            rightpos = childpos + 1
            if rightpos < endpos and not self.vertex_list[childpos] < self.vertex_list[rightpos]:
                childpos = rightpos
            # Move the smaller child up.
            self.vertex_list[pos] = self.vertex_list[childpos]
            pos = childpos
            childpos = 2*pos + 1
        """The leaf at pos is empty now.  Put newitem there, and bubble it up
        to its final resting place (by shifting its parents down)."""
        self.vertex_list[pos] = newitem
        self.shiftDown(startpos, pos)

"""Create a vertex class. This class holds the vertex information including name,UP/DOWN status,previous vertex
    and transmission time from the source vertex(used for Dijkstra's algorithm)"""
class Vertex(object):
    def __init__(self,name,upFlag):
        self.name = name
        self.upFlag = upFlag
        self.prevVertex = None
        self.transmitTime = float('inf')
    def __hash__(self):
        return hash(self.name)
    def __eq__(self, other):
        return (self.transmitTime) == (other.transmitTime)
    def __lt__(self, other):
        return (self.transmitTime) < (other.transmitTime)
    def __le__(self, other):
        return (self.transmitTime) <= (other.transmitTime)
    def __ge__(self, other):
        return (self.transmitTime) >= (other.transmitTime)
    def __gt__(self, other):
        return (self.transmitTime) > (other.transmitTime)
    def __ne__(self, other):
        return (self.transmitTime) != (other.transmitTime)

"""Create an edge class. This class holds the edge details including start vertex,end vertex,transmission time of an edge, UP/DOWN status of edge"""
class Edge(object):
    def __init__(self,fromVertex,toVertex,transmit_time,upFlag):
        self.fromVertex = fromVertex
        self.toVertex = toVertex
        self.transmit_time = float(transmit_time)
        self.upFlag = upFlag
    def __hash__(self):
        return hash((self.fromVertex,self.toVertex))
    def __eq__(self, other):
        return (self.fromVertex,self.toVertex,self.transmit_time,self.upFlag) == (other.fromVertex,other.toVertex,other.transmit_time,other.upFlag)
    
"""Create a graph class to store the list of vertices and edges.Adjacency list of each vertex is maintained
    All the queries/ operations on the graph are performed in this class"""
class Graph(object):
    def __init__(self):
        self.vertices = {}
        self.edges = {}
        self.adjList = {}
        
    #Adds a new Vertex to the graph
    def addvertex(self,vertexName,vertex):
        self.vertices[vertexName] = vertex
        
    #Adds a new Edge to the graph
    def addEdge(self,edgeKey,Edge):
        self.edges[edgeKey] = Edge

    """Checks if the vertices are already there. If not adds them to the graph and creates a single directed edge from source to destination
        Updates the existing Transmission time if an edge exists. Updates the adjacency list accordingly"""
    def addUpdateEdge(self,headVertex,tailVertex,transmitTime):
        if not self.vertices.has_key(headVertex):
            self.addvertex(headVertex,Vertex(headVertex,True))
        if not self.vertices.has_key(tailVertex):
            self.addvertex(tailVertex,Vertex(tailVertex,True))
        if self.edges.has_key((headVertex,tailVertex)):
            self.edges[(headVertex,tailVertex)].transmit_time = float(transmitTime)
        else:
            self.addEdge((headVertex,tailVertex),Edge(headVertex,tailVertex,transmitTime,True))
            self.addAdjacentVertices(headVertex,tailVertex)
            self.addAdjacentVertices(tailVertex,None)

    #Marks an existing edge as DOWN
    def edgeDown(self,headVertex,tailVertex):
        self.edges[(headVertex,tailVertex)].upFlag = False

    #Marks an existing edge as UP
    def edgeUp(self,headVertex,tailVertex):
        self.edges[(headVertex,tailVertex)].upFlag = True

    #Marks an existing Vertex as UP
    def vertexUp(self,vertex):
        self.vertices[vertex].upFlag = True

    #MArks an existing Vertex as DOWN
    def vertexDown(self,vertex):
        self.vertices[vertex].upFlag = False

    #Updating the Adjacency List
    def addAdjacentVertices(self,vertex1,vertex2):
        if not vertex2 == None:
            self.adjList.setdefault(vertex1,[]).append(vertex2)
        else:
            self.adjList.setdefault(vertex1,[])

    #Delete an exisitng edge and update the Adjacency List        
    def deleteEdge(self,vertex1,vertex2):
        del self.edges[(vertex1,vertex2)]
        self.adjList[vertex1].remove(vertex2)

    #Print the reachable vertices using Breadth First Search    
    def reachable(self):
        for vertex in (sorted(self.vertices.keys())):
            if self.vertices[vertex].upFlag == True:
                self.printReachablevertices(vertex)
                
    def printReachablevertices(self,vertex):
        """Uses the Breadth first search algoithm to print the reachable vertices. Running time is O(V+E) for each vertex/EDGE that is UP.
           Worst Case Running time for overall graph is O(V*(V + E)) assuming all Vertices and Edges are UP since the loop runs for each vertex"""
        color = {}
        reachable_list = {}
        filtered_dict = {key: val for key,val in self.vertices.items() if (key != vertex and val.upFlag == True)}
        for rvertex in self.vertices.keys():
            color[rvertex] = "white"
        color[vertex] = "gray"
        q = Queue()
        q.put(vertex)
        while not q.empty():
            u = q.get()
            for v in sorted(self.adjList[u]):
                if color[v] == "white" and self.vertices[v].upFlag == True and self.edges[(u,v)].upFlag == True:
                    color[v] == "gray"
                    q.put(v)
                    reachable_list[v] =v
            color[u] = "black"
        print vertex
        for vertex_list in sorted(reachable_list.keys()):
            print " ", vertex_list
            
    """Computes the shortest path using Dijkstra's shortest path algorithm"""
    def path(self,source,destination):
        #Using a priority Queue
        pq = PriorityQueue()
        for vertex in self.vertices.keys():
            self.vertices[vertex].prevVertex = None
            self.vertices[vertex].transmitTime = float('inf')
        self.vertices[source].transmitTime = 0.0
        traverse = []
        filtered_dict = {key: val for key,val in self.vertices.items() if val.upFlag == True}
        pq.addElements(filtered_dict)
        while pq.vertex_list:
            u = pq.extractMin()
            for v in self.adjList[u.name]:
                if self.vertices[v].upFlag == True and self.edges[(u.name,v)].upFlag == True:
                    if self.vertices[v].transmitTime > (self.vertices[u.name].transmitTime + self.edges[(u.name,v)].transmit_time) :
                        self.vertices[v].transmitTime = self.vertices[u.name].transmitTime + self.edges[(u.name,v)].transmit_time
                        self.vertices[v].prevVertex = u
                        pq.decreaseKey(self.vertices[v])
        node = self.vertices[destination]
        """Traverse the nodes and print them in the proper order"""
        while node.prevVertex is not None:
            traverse.append(node.name)
            node = node.prevVertex
        traverse.append(node.name)
        traverse.reverse()
        print " ".join([str(vert) for vert in traverse]),self.vertices[destination].transmitTime
        
    """print the vertices in the graph for the print query"""
    def printGraph(self):
        for vertices in (sorted(self.vertices.keys())):
            print (self.vertices[vertices].name), "DOWN" if (self.vertices[vertices].upFlag == False) else ""
            for adj_vertices in sorted(self.adjList[vertices]):
              print " ", adj_vertices,self.edges[(vertices,adj_vertices)].transmit_time, "DOWN" if (self.edges[(vertices,adj_vertices)].upFlag == False) else ""

#Main function call for the program
def main():
    #Pass the input filename as argument to the program
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Enter the input file to build the graph")
    args = parser.parse_args()

    inputFilename = args.filename
    
    #Creating a graph
    graph = Graph()
    #Read the contents of input file
    with open(inputFilename,'r') as f:
        for line in f:
            vertex1 = Vertex(line.split()[0],True)
            vertex2 = Vertex(line.split()[1],True)
            #Add the vertices and edges to the graph
            graph.addvertex(vertex1.name,vertex1)
            graph.addvertex(vertex2.name,vertex2)
            edge1 = Edge(line.split()[0],line.split()[1],line.split()[2],True)
            edge2 = Edge(line.split()[1],line.split()[0],line.split()[2],True)
            graph.addEdge((vertex1.name,vertex2.name),edge1)
            graph.addEdge((vertex2.name,vertex1.name),edge2)
            graph.addAdjacentVertices(vertex1.name,vertex2.name)
            graph.addAdjacentVertices(vertex2.name,vertex1.name)
            
    #Reading from standard input
    while True:
        line = sys.stdin.readline()
        try:
            if line.strip():
                queries = line.split()
                if queries[0] == "addedge":
                    graph.addUpdateEdge(queries[1],queries[2],queries[3])
                elif queries[0] == "deleteedge":
                    graph.deleteEdge(queries[1],queries[2])
                elif queries[0] == "edgedown":
                    graph.edgeDown(queries[1],queries[2])
                elif queries[0] == "edgeup":
                    graph.edgeUp(queries[1],queries[2])
                elif queries[0] == "vertexdown":
                    graph.vertexDown(queries[1])
                elif queries[0] == "vertexup":
                    graph.vertexUp(queries[1])
                elif queries[0] == "print":
                    graph.printGraph()
                elif queries[0] == "reachable":
                    graph.reachable()
                elif queries[0] == "path":
                    graph.path(queries[1],queries[2])
                elif queries[0] == "quit":
                    quit()
                else:
                    print "Please provide a valid query to the graph"
        except SystemExit:
            quit()    
        except:
            print "Improper Query. Please provide a valid query. Queries are case sensitive"
            continue
if __name__ == '__main__':
    main()
