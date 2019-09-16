from vec import *
from window import * 
from grid import * 

def placeButtonsForGrid(g : Grid, w : Window):
    
    width = 1000 / g.width
    length = 1000 / g.length

    for x in range(0,g.width):
        for y in range(0,g.length):
            node = g.grid[x][y]
            node.button = w.makeButton(x * width, y * length, x * width + width, y * length + length)
            node.button.configure(command = g.grid[x][y].onClick)

    for x in range(0,g.width):
        node = g.grid[x][0]
        node.state = "wall"

    for x in range(0,g.width):
        node = g.grid[x][g.length-1]
        node.state = "wall"

    for y in range(0,g.length):
        node = g.grid[0][y]
        node.state = "wall"

    for y in range(0,g.length):
        node = g.grid[g.width-1][y]
        node.state = "wall"
        

def pressKey(key, grid : Grid):

    print(key)

    if(key.char == '1'):
        Block.selectedState = "empty"
    elif(key.char == '2'):
        Block.selectedState = "wall"
    elif(key.char == '3'):
        Block.selectedState = "spawn"
    elif(key.char == '4'):
        Block.selectedState = "end"
    elif(key.char == '\r'):
        grid.calcAllNodes()
    elif(key.char == ' '):
        grid.AStar()


def wallSelect():
    Block.selectedState = "wall"

def startSelect():
    Block.selectedState = "spawn"

def endSelect():
    Block.selectedState = "end"

def emptySelect():
    Block.selectedState = "empty"


def main():
    g = Grid(20,20)

    w = Window(600,700)
    w.callKeyPress = lambda k : pressKey(k, g)

    w.wallBotton.configure(command = wallSelect)
    w.startBotton.configure(command = startSelect)
    w.endBotton.configure(command = endSelect)
    w.emptyBotton.configure(command = emptySelect)

    placeButtonsForGrid(g, w)

    g.setStartPoint(vec2i(7,10))
    g.setEndPoint(vec2i(17,10))
    g.reset();

    w.run()


main()