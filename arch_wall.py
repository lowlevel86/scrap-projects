#!/bin/python3

# Parametric modeling of an arched wall
# Programmed by: Crailin Mogged
# Date: 02-28-2025

import matplotlib.pyplot as plt
from math import *

def createArchWall(rad, archCnt, blockCnt): # blockCnt -- number of blocks in an arch
    x = []
    y = []

    for j in range(archCnt):
        radO = rad - j # outer radius
        radI = rad - (j+1) # inner radius

        angle = pi * 0.5 * (blockCnt//2) / blockCnt
        xPvO = radO * cos(angle) # outer radius pivot or corner of the square
        yPvO = radO * sin(angle)
        xPvI = radI * cos(angle) # inner radius pivot or corner of the square
        yPvI = radI * sin(angle)

        for i in range(blockCnt):
            angleA = pi * 0.5 * i / blockCnt
            angleB = pi * 0.5 * (i+1) / blockCnt
            x1 = radO * cos(angleA) # outer shell
            y1 = radO * sin(angleA)
            x2 = radO * cos(angleB)
            y2 = radO * sin(angleB)
            
            x3 = radI * cos(angleA) # inner shell
            y3 = radI * sin(angleA)
            x4 = radI * cos(angleB)
            y4 = radI * sin(angleB)
            
            x.append([x1, x2, x4, x3]) # quad polygon
            y.append([y1, y2, y4, y3])
        

    # create the transition arch

    radO = rad - archCnt # outer radius
    radI = rad - (archCnt+1) # inner radius

    angle = pi * 0.5 * (blockCnt//2) / blockCnt
    xPvO = radO * cos(angle) # outer radius pivot or corner of the square
    yPvO = radO * sin(angle)
    xPvI = radI * cos(angle) # inner radius pivot or corner of the square
    yPvI = radI * sin(angle)

    x2 = radO * cos(angle) # outer shell
    y2 = radO * sin(angle)

    angle = pi * 0.5 * (blockCnt//2+1) / blockCnt
    x4 = radO * cos(angle)
    y4 = radO * sin(angle)
    xCorner = x4 # outer radius pivot or corner of the square

    angle = pi * 0.5 * (blockCnt//2-1) / blockCnt
    x1 = radO * cos(angle) # outer shell
    y1 = radO * sin(angle)
    yCorner = y1 # outer radius pivot or corner of the square

    x3 = xCorner
    y3 = yCorner

    x.append([x1, x2, x4, x3]) # corner quad polygon
    y.append([y1, y2, y4, y3])

    for i in range(blockCnt//2-1):
        angleA = pi * 0.5 * i / blockCnt
        angleB = pi * 0.5 * (i+1) / blockCnt
        x1 = radO * cos(angleA) # outer shell
        y1 = radO * sin(angleA)
        x2 = radO * cos(angleB)
        y2 = radO * sin(angleB)
        
        y4 = y2; y3 = y1 # create grid
        x3 = xCorner; x4 = xCorner
        x.append([x1, x2, x4, x3]) # quad polygon
        y.append([y1, y2, y4, y3])

    for j in range(blockCnt//2+1, blockCnt):
        angleA = pi * 0.5 * j / blockCnt
        angleB = pi * 0.5 * (j+1) / blockCnt
        x1 = radO * cos(angleA) # outer shell
        y1 = radO * sin(angleA)
        x2 = radO * cos(angleB)
        y2 = radO * sin(angleB)
        
        x4 = x2; x3 = x1 # create grid
        y3 = yCorner; y4 = yCorner
        x.append([x1, x2, x4, x3]) # quad polygon
        y.append([y1, y2, y4, y3])


    # create the grid area
    for i in range(blockCnt//2-1):
        angleA = pi * 0.5 * i / blockCnt
        angleB = pi * 0.5 * (i+1) / blockCnt
        y1 = radO * sin(angleA)
        y3 = radO * sin(angleB)
        
        y2 = y1; y4 = y3

        for j in range(blockCnt//2+1, blockCnt):
            angleA = pi * 0.5 * j / blockCnt
            angleB = pi * 0.5 * (j+1) / blockCnt
            x3 = radO * cos(angleA) # outer shell
            x4 = radO * cos(angleB)
            
            x1 = x3; x2 = x4
            
            x.append([x1, x2, x4, x3]) # quad polygon
            y.append([y1, y2, y4, y3])

    return x, y


def linkPolyPts(x, y): # connect vertices that are the same
    ptLink = []
    linked = [[False for _ in sublist] for sublist in x]

    for i in range(len(x)):
        for j in range(len(x[i])):
            if linked[i][j]:
                continue
            xP1 = x[i][j]
            yP1 = y[i][j]
            ptLink.append([i, j])
            linked[i][j] = True
            
            for k in range(len(x)):
                for l in range(len(x[i])):
                    if linked[k][l]:
                        continue
                    xP2 = x[k][l]
                    yP2 = y[k][l]
                    
                    if xP1 > xP2-0.001 and yP1 > yP2-0.001:
                        if xP1 < xP2+0.001 and yP1 < yP2+0.001:
                            ptLink[len(ptLink)-1].append(k)
                            ptLink[len(ptLink)-1].append(l)
                            linked[k][l] = True

    return ptLink


def assignPt(x, y, link, xLoc, yLoc):
    for i in range(0, len(link), 2):
        poly = link[i+0]
        coor = link[i+1]
        x[poly][coor] = xLoc
        y[poly][coor] = yLoc


def getPt(x, y, link):
    poly = link[0]
    coor = link[1]
    return x[poly][coor], y[poly][coor]


def getConnPts(x, y, link): # find all vertices that connect to a vertex
    xPts = []; yPts = []
    for i in range(0, len(link), 2):
        poly = link[i+0]
        coor = link[i+1]
        
        if coor == 0:
            xPts.append(x[poly][1])
            yPts.append(y[poly][1])
            xPts.append(x[poly][3])
            yPts.append(y[poly][3])
        
        if coor == 1:
            xPts.append(x[poly][0])
            yPts.append(y[poly][0])
            xPts.append(x[poly][2])
            yPts.append(y[poly][2])
            
        if coor == 2:
            xPts.append(x[poly][1])
            yPts.append(y[poly][1])
            xPts.append(x[poly][3])
            yPts.append(y[poly][3])
            
        if coor == 3:
            xPts.append(x[poly][0])
            yPts.append(y[poly][0])
            xPts.append(x[poly][2])
            yPts.append(y[poly][2])
        
    return xPts, yPts


def getArea(x, y): # find the area of a polygon
    sumA = 0; sumB = 0
    last = len(x)-1
    
    for i in range(last):
        sumA += x[i]*y[i+1]
        sumB += y[i]*x[i+1]
    sumA += x[last]*y[0]
    sumB += y[last]*x[0]
    
    return 0.5 * abs(sumA - sumB)


# finds the area of a polygon created by connected edges
def getIntersectPolyArea(xInter, yInter, xEdges, yEdges):
    xPts = [xEdges[0]]
    yPts = [yEdges[0]]
    xNext = xEdges[0+1]
    yNext = yEdges[0+1]
    unused_edge = [True] * len(xEdges)
    
    for j in range(len(xEdges)//2-1):
        # get next edge
        for i in range(2, len(xEdges)):
            if unused_edge[i]:
                if xEdges[i] == xNext and yEdges[i] == yNext:
                    xPts.append(xEdges[i]) # append next point
                    yPts.append(yEdges[i])
                    if i&1:
                        xNext = xEdges[i-1]
                        yNext = yEdges[i-1]
                        unused_edge[i-1] = False
                    else:
                        xNext = xEdges[i+1]
                        yNext = yEdges[i+1]
                        unused_edge[i+1] = False
                    
                if xNext == xEdges[0] and yNext == yEdges[0]:# until first poly vertex found
                    return getArea(xPts, yPts)
    
    if len(xPts) <= 2:
        xPts.append(xNext) # append next point
        yPts.append(yNext)
        xPts.append(xInter)
        yPts.append(yInter)
        return getArea(xPts, yPts)

    print("Wrong input for getIntersectPolyArea()")
    exit()


def sigmoid(x, thres, steepness): # lower value is more steep
    return (x - thres) / (steepness + abs(x - thres)) * 0.5 + 0.5


# area aware smooth function influenced by area and weights
def smooth(x, y, ptLink, iteratCnt, xWeight, yWeight, areaThres, boundary): # lower value creates a sharper separation boundary
    for j in range(iteratCnt):
        for i in range(len(ptLink)):
            
            xPt, yPt = getPt(x, y, ptLink[i])
            
            xPts, yPts = getConnPts(x, y, ptLink[i])
            area = getIntersectPolyArea(xPt, yPt, xPts, yPts)
            
            if len(xPts) == 2:
                area *= 4
            
            if len(xPts) == 4:
                area *= 2
            
            xAvg = sum(xPts) / len(xPts)
            yAvg = sum(yPts) / len(yPts)
            
            # the smaller the area of the polygon (formed by the intersecting edges)
            # the less the vertex will move
            delta = sigmoid(area, areaThres, boundary)
            xNew = (xAvg - xPt)*delta*xWeight[i] + xPt
            yNew = (yAvg - yPt)*delta*yWeight[i] + yPt
            
            assignPt(x, y, ptLink[i], xNew, yNew)


##################################################################
# main
##################################################################

# create arched wall
x, y = createArchWall(16, 3, 42)

# connect vertices that are the same
ptLink = linkPolyPts(x, y)

# create weights for the vertices to keep some from moving
xWeight = [1.0] * len(ptLink)
yWeight = [1.0] * len(ptLink)

for i in range(len(ptLink)):
    xPt, yPt = getPt(x, y, ptLink[i])

    # pin down the arch
    if sqrt(xPt*xPt + yPt*yPt) > 15-0.001:
        xWeight[i] = 0.0
        yWeight[i] = 0.0

    # pin down the edges along the axis in a
    # way that allows side to side movement
    if xPt < 0.001:
        xWeight[i] = 0.0

    if yPt < 0.001:
        yWeight[i] = 0.0

# smooth out the mesh topology to allow evenly proportioned blocks
smooth(x, y, ptLink, 350, xWeight, yWeight, 0.55, 0.008)


# display the arched wall
plt.figure(figsize=(6, 6))

for i in range(len(x)):
    xPoly = x[i]; xPoly.append(x[i][0])
    yPoly = y[i]; yPoly.append(y[i][0])
    plt.plot(xPoly, yPoly, 'b-', linewidth=0.5)

plt.scatter(x, y, color='red', marker='o', s=1.5)
plt.title('Arch Wall')
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True)
plt.show()

