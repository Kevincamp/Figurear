import pygame, random
from p2t import *

#import numpy as np
#import matplotlib
#from mpl_toolkits.mplot3d import Axes3D
#import matplotlib.tri as mtri

screen = pygame.display.set_mode((800,600))

c = 0
draw_on = False
first_pos = [0, 0]
lastp_pos = [0, 0]
last_pos = [0, 0]
color = (255, 255, 255)
radius = 3
pointsFigure = []

def pos_to_point(position):
    x = position[0]
    y = position[1]
    return Point(x,y)
    
def roundline(srf, color, start, end, saveInList,radius=1):
    dx = int(end[0])- int(start[0])
    dy = int(end[1])-int(start[1])
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int( start[0]+float(i)/distance*dx)
        y = int( start[1]+float(i)/distance*dy)
        pygame.draw.circle(srf, color, [x, y], radius)
        if(saveInList):
            pointsFigure.append(Point(float(x),float(y)))

def loadpoint(pointsFigure):
    points=[]
    for point in pointsFigure:
        points.append(Point(float(point[0]), float(point[1])))
    return points

def triangulacion(polyline):
    import sys
    from time import clock
    # initialize clock
    t0 = clock()
    ##
    ## Step 1: Initialize
    ## NOTE: polyline must be a simple polygon. The polyline's points
    ## constitute constrained edges. No repeat points!!!
    ##
    print("Init CDT")
    cdt = CDT(polyline)
    ##
    ## Step 2: Triangulate
    ##
    print("Triangulate")
    try:
        triangles = cdt.triangulate()
    except e:
        print("Except")
    
    print "Elapsed time (ms) = " + str(clock()*1000.0)
    # The Main Event Loop
    done = False
    while not done:
        # Draw triangles
        for t in triangles:
            x1 = int(t.a.x)
            y1 = int(t.a.y)
            x2 = int(t.b.x)
            y2 = int(t.b.y)
            x3 = int(t.c.x)
            y3 = int(t.c.y)
            trigon(screen, x1, y1, x2, y2, x3, y3, red)
        #Update the scree
        pygame.display.update()

def print_points(points):
    # points - lista de puntos
    for point in points:
        #x = point[0]
        #y = point[1]
        print ("\np. x = " + str(point.x) + " , y = " + str(point.y))
        

try:
    while True:
        e = pygame.event.wait()
        if e.type == pygame.QUIT:
            raise StopIteration
        if e.type == pygame.MOUSEBUTTONDOWN:
            screen.fill((0,0,0))
            first_pos = e.pos
            if c==0:
                pointsFigure.append(pos_to_point(first_pos))
            color = (random.randrange(256), random.randrange(256), random.randrange(256))
            pygame.draw.circle(screen, color, e.pos, radius)
            draw_on = True
        if e.type == pygame.MOUSEBUTTONUP:
            draw_on = False
            lastp_pos = e.pos
            roundline(screen,color,first_pos,lastp_pos, True,radius)
            lastp_pos = (0, 0)
            print_points(pointsFigure)
            #triangulacion(pointsFigure)
        if e.type == pygame.MOUSEMOTION:
            if draw_on:
                c+=1
                pygame.draw.circle(screen, color, e.pos, radius)
                roundline(screen, color, e.pos, last_pos, True, radius)
                #pointsFigure.append(pos_to_point(e.pos))
            last_pos = e.pos
        
        pygame.display.flip()
except StopIteration:
    pass

pygame.quit()