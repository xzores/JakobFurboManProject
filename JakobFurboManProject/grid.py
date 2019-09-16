from vec import *
from pprint import pprint

class Grid:
    pass

class Block:

    selectedState = "wall"

    def __init__(self, grid : Grid, x : int, y : int):
        self.state = "empty"
        self.calState = "none"
        self.mygrid = grid
        self.x = x
        self.y = y
        self.gcost = -1
        self.hcost = -1
        self.fcost = -1
        self.parrent = vec2i(-1,-1)

    def showCost(self):
        i : int = int(self.fcost * 10)
        self.button.configure(text = str(i))

        if(i < 0):
            self.button.configure(text = "")
 
    def doColor(self):
        if(self.state == "wall"):
            self.button.configure(bg = "black")
        elif(self.state == "empty"):
            self.button.configure(bg = "white")

        if(self.calState == "none"):
            pass
        elif(self.calState == "current"):
            self.button.configure(bg = "yellow")
        elif(self.calState == "closed"):
            self.button.configure(bg = "lightred")
        elif(self.calState == "open"):
            self.button.configure(bg = "lightgreen")

        if(self.state == "spawn"):
            self.button.configure(bg = "red")
        elif(self.state == "end"):
            self.button.configure(bg = "green")

        if(self.calState == "path"):
            self.button.configure(bg = "blue")


    def onClick(self):
        self.state = self.selectedState

        if(self.state == "spawn"):
            self.mygrid.setStartPoint(vec2i(self.x, self.y))
            self.state = "spawn"

        if(self.state == "end"):
            self.mygrid.setEndPoint(vec2i(self.x, self.y))
            self.state = "end"
    
        self.doColor()


class Grid:

    def __init__(self, width: int, length: int, start : vec2i = vec2i(), end : vec2i = vec2i(0,1)):
        self.width = width
        self.length = length
        self.grid = [[0 for x in range(width)] for y in range(length)] 
        
        for x in range(0,width):
            for y in range(0,length):
                self.grid[x][y] = Block(self, x, y)

        self.start = vec2i()
        self.end = vec2i()
        self.open = []
        self.openCost = []
        self.closed = []
        self.found = False
        self.pos : vec2i = self.start

    def calcAllNodes(self, showCost : bool = True):
        for x in range(0,self.width):
            for y in range(0,self.length):
                self.calcPoint(vec2i(x,y), showCost)

    def calcPoint(self, point : vec2i, parrent : Block, showCost : bool = True):

        if(point.x >= self.width or point.y >= self.length or point.x < 0 or point.y < 0):
            return -1

        node = self.grid[point.x][point.y]

        if(node.state == "wall"):
            node.fcost = -1
            node.showCost()
            return -1

        prevCost = node.fcost

        gxdiff = abs(node.x - parrent.x);
        gydiff = abs(node.y - parrent.y);

        hxdiff = abs(node.x - self.end.x);
        hydiff = abs(node.y - self.end.y);

        #the 
        ga = abs(gxdiff - gydiff);
        ha = abs(hxdiff - hydiff);

        #on the x,y axis
        gb = (gxdiff + gydiff) - ga
        hb = (hxdiff + hydiff) - ha

        node.gcost = ga * 14 + gb * 10 + parrent.gcost
        node.hcost = ha * 14 + hb * 10
        node.fcost = node.gcost + node.hcost

        if(prevCost > 0 and prevCost < node.fcost):
            node.fcost = prevCost

        if(showCost == True):
            node.showCost()

        return node.fcost

   
    def LightUpPath(self, pathEnd : vec2i):
        done : bool = False

        print("light up path")
        cur = pathEnd;

        while not done:
            self.grid[cur.x][cur.y].calState = "path"
            cur = self.grid[cur.x][cur.y].parrent
            if(cur == self.grid[self.start.x][self.start.y]):
                done = True
            
        
        for x in range(0,self.width):
            for y in range(0,self.length):
                    self.grid[x][y].doColor()


    def getNeighbours(self, point : vec2i):
        return [point + vec2i(-1,-1), point + vec2i(0,-1), point + vec2i(1,-1), point + vec2i(-1,0), point + vec2i(1,0), point + vec2i(-1,1), point + vec2i(0,1), point + vec2i(1,1)]


    def AStar(self):
        
        if(self.found):
            return

        if(len(self.open) == 0):
            self.open = [self.start]
            self.openCost = [self.calcPoint(self.start, self.grid[self.start.x][self.start.y])]
            self.closed = []
            self.pos = self.start
            self.grid[self.pos.x][self.pos.y].calState = "current"

        if(not self.found):
            if(self.pos == self.end):
                #we allready have a path
                return


            openCost = []
            opengCost = []

            for c in self.open:
                openCost.append(self.grid[c.x][c.y].fcost)

            #sort by fcost
            openCost.sort()

            lowestCost = openCost[0]

            kandidates = []

            for c in self.open:
                if(self.grid[c.x][c.y].fcost == lowestCost):
                    kandidates.append(c)

            #sort by gcost
            for gc in kandidates:
                opengCost.append(self.grid[gc.x][gc.y].gcost);

            opengCost.sort()

            lowestGCost = opengCost[0]

            for n in kandidates:
                if(self.grid[n.x][n.y].gcost == lowestGCost):
                    self.pos = n

            lastPos = self.pos

            for n in self.open:
                if(self.grid[n.x][n.y].fcost == lowestCost):
                    self.pos = n

            #just for debugging
            if(self.pos == lastPos):
                print("error pos did not change")

            pprint(self.open)
            print("removeing : " + str(self.pos.x) + "," + str(self.pos.y))
            self.open.remove(self.pos)
            self.closed.append(self.pos)
            self.grid[self.pos.x][self.pos.y].calState = "closed"
            self.grid[self.pos.x][self.pos.y].calState = "current"

            #we found a path
            if(self.pos == self.end):
                self.found = True
                self.LightUpPath(self.pos)
                return
            
            currentNode = self.grid[self.pos.x][self.pos.y]

            neighbours = self.getNeighbours(self.pos)

            for n in neighbours:

                self.calcPoint(n, currentNode)
                node = self.grid[n.x][n.y]

                if(node.fcost < 0):
                    continue

                if(not self.isClosed(n)):
                    #it is not closed
                    if((node.fcost < currentNode.fcost or not self.isOpen(n)) and node.fcost > 0):
                        
                        if(node.parrent == vec2i(-1,-1)):
                            node.parrent = currentNode
                        if(currentNode.fcost < node.parrent.fcost):
                            node.parrent = currentNode

                        if(not self.isOpen(n) and not self.isClosed(n)):
                            self.open.append(n)
                            print("adding to open :" + str(n.x) + ":" + str(n.y))
                            node.calState = "open"

        for x in range(0,self.width):
            for y in range(0,self.length):
                    self.grid[x][y].doColor()

    

    def isOpen(self, pos : vec2i):

        f : bool = False

        for n in self.open:
            if(n == pos):
                f = True

        return f             

    def isClosed(self, pos : vec2i):
        f : bool = False

        for n in self.closed:
            if(n == pos):
                f = True
                
        return f      

                
    def reset(self):

        self.found = False
        self.open = []
        for x in range(0,self.width):
            for y in range(0,self.length):
                node = self.grid[x][y]
                node.fcost = -1
                node.gcost = -1
                node.hcost = -1
                node.parrent = vec2i(-1,-1)
                self.grid[x][y].calState = "none"

        self.reCalcColor()

    def reCalcColor(self):
        for x in range(0,self.width):
            for y in range(0,self.length):
                self.grid[x][y].doColor()
                self.grid[x][y].showCost()

    def setEndPoint(self, pos : vec2i):
        self.reset()
        for x in range(0,self.width):
            for y in range(0,self.length):
                if(self.grid[x][y].state == "end"):
                    self.grid[x][y].state = "empty"

        self.end = pos
        self.grid[self.end.x][self.end.y].state = "end";
        self.reCalcColor();

    def setStartPoint(self, pos : vec2i):
        self.reset()
        for x in range(0,self.width):
            for y in range(0,self.length):
                self.grid[x][y].doColor()
                if(self.grid[x][y].state == "spawn"):
                    self.grid[x][y].state = "empty"

        self.start = pos
        self.grid[self.start.x][self.start.y].state = "spawn";
        self.reCalcColor();
