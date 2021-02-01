import pygame, sys 
import copy

pygame.init()

screenSize = [640,480]
unitSize = 20
gridSize = 16 #always squared 
grid = []
blue = [0,0,120]
red = [120,0,0]
lightRed = [240,0,0]
black = [0,0,0]
bgColor = [0,100,20]
screen = pygame.display.set_mode(screenSize)
leftBound = screenSize[0]/2 - unitSize * gridSize/2
upperBound = screenSize[1]/2 - unitSize * gridSize/2
screen.fill(bgColor)


def filterIndex(num,max):
    if num < 0 : return 0
    if num > max : return max
    return num

def resetGrid():
    global grid
    grid = []
    for i in range(gridSize):
        row = []
        for j in range(gridSize):
            recta = pygame.rect.Rect(leftBound+j*unitSize,upperBound+i*unitSize,unitSize,unitSize)
            row.append([recta,bgColor])
        grid.append(row)
    
rect = pygame.rect.Rect(leftBound, upperBound, unitSize,unitSize)

def drawGrid(): 
    global leftBound
    global screen
    global grid
    global rect
    for row in grid:
        for rects in row:
             pygame.draw.rect(screen,rects[1],rects[0])
    print(rect)
    pygame.draw.rect(screen, red, rect)

    for i in range(gridSize+1): 
        pygame.draw.line(screen,black, [leftBound,upperBound+i*unitSize],[leftBound+unitSize*gridSize,upperBound+i*unitSize],1)
        pygame.draw.line(screen,black, [leftBound+i*unitSize,upperBound],[leftBound+i*unitSize,upperBound+unitSize*gridSize],1)

    pygame.display.flip()

isPressed = False
change = False

def findPositionMouse(mousePos):
    if (mousePos[0] < leftBound or mousePos[0] > leftBound + gridSize*unitSize) or (mousePos[1] < upperBound or mousePos[1] > upperBound + gridSize*unitSize) :
        return None
    x = mousePos[0] -leftBound 
    y = mousePos[1] - upperBound

    x = int(x / unitSize) *unitSize + leftBound 
    y = int(y / unitSize) *unitSize + upperBound
    print([x,y])
    return [x,y] 


def findPosition(rect):
    
    x = rect.x - leftBound
    y = rect.y - upperBound

    x = int(x / unitSize)
    y = int(y / unitSize)

    return [x,y] 

def setDiagonal(oldRect):
    global grid  
    global change
    rectPos = findPosition(oldRect)

    if(rectPos[0]> 1 and rectPos[1] < gridSize -1):
        grid[rectPos[1]][rectPos[0]][1] = red
        grid[rectPos[1]+1][rectPos[0]-1][1] = red


def setRect(rect):
    global grid
    global coordinates
    global change
    coordinates = findPositionMouse(pygame.mouse.get_pos())
    if coordinates != None:
        if(rect.x != coordinates[0] or rect.y != coordinates[1]):
            change = True
            
        rect.x = coordinates[0]
        rect.y = coordinates[1]
    return rect

def setDiamond(oldRect):
    global grid
    rectPos = findPosition(oldRect)

     

    if(rectPos[0] > 0 ):
        grid[rectPos[1]][rectPos[0]-1][1] = red
    if(rectPos[0] < gridSize-1):
         grid[rectPos[1]][rectPos[0]+1][1] = red
    if(rectPos[1] < gridSize-1):
        grid[rectPos[1]+1][rectPos[0]][1] = red
    if(rectPos[1] > 0):
        grid[rectPos[1]-1][rectPos[0]][1] = red

def setLineHori(oldRect):
    global grid 
    rectPos  = findPosition(oldRect)

    grid[rectPos[1]][rectPos[0]+1][1] = red
    grid[rectPos[1]][rectPos[0]][1] = red
    grid[rectPos[1]][rectPos[0]-1][1] = red

def grow():
    global grid
    gridBuffer = copy.deepcopy(grid)
    print("Called")
    for i in range(len(grid)):
        
        for j in range(len(grid[i])):
            
            if gridBuffer[i][j][1] == red or grid[i][j][1] == lightRed :
                if(grid[filterIndex(i-1,gridSize-1)][j][1] != red):
                    gridBuffer[filterIndex(i-1,gridSize-1)][j][1] = lightRed
                if grid[filterIndex(i+1,gridSize-1)][j][1] != red:
                    gridBuffer[filterIndex(i+1,gridSize-1)][j][1] = lightRed
                if grid[i][filterIndex(j-1,gridSize-1)][1] != red:
                    gridBuffer[i][filterIndex(j-1,gridSize-1)][1] = lightRed
                if grid[i][filterIndex(j-1,gridSize+1)][1] != red: 
                    gridBuffer[i][filterIndex(j+1,gridSize-1)][1] = lightRed
                
    grid = gridBuffer


resetGrid()
drawGrid()
pygame.draw.rect(screen, red, rect)
currentShape = 0

def eventQueue():
    global rect
    global isPressed
    global change
    global currentShape
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit() 
        if event.type == pygame.KEYDOWN and not isPressed:
            if(event.dict['key'] == 273 and rect.top != upperBound):
                
                rect = rect.move(0,-unitSize)

            elif(event.dict['key'] == 274 and rect.bottom != upperBound+gridSize*unitSize):
                rect = rect.move(0,unitSize)
            elif(event.dict['key'] == 276 and rect.left != leftBound):
                rect = rect.move(-unitSize,0)
            elif(event.dict['key'] == 275 and rect.right != leftBound+gridSize*unitSize):
                rect = rect.move(unitSize,0)
            elif(event.dict['key'] == 32):
                #resetGrid()
                grow()
                change = True
            elif(event.dict['key'] == 257):
                currentShape = 1
            elif(event.dict['key'] == 258):
                currentShape = 0

    if(pygame.mouse.get_pressed()[0]):
        if(currentShape == 0):
            setDiagonal(rect)
        elif(currentShape == 1):
            setDiamond(rect)
        change = True
    
    
# game loop 


while 1:
    change = False
    
    eventQueue();    
    rect = setRect(rect)
    if(change):
        
        drawGrid()
        
    pygame.display.flip()