import pygame, random
from p2t import *
from pygame import Color
from pygame.gfxdraw import trigon, line
from sets import Set 
from math import sin, cos, atan2, sqrt, pi

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

def pathlength(points):
    d = 0
    for i,p_i in enumerate(points[:len(points)-1]):
        d += distance(p_i, points[i+1])
    return d

    
def roundline(srf, color, start, end,radius=1):
    dx = int(end[0])- int(start[0])
    dy = int(end[1])-int(start[1])
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int( start[0]+float(i)/distance*dx)
        y = int( start[1]+float(i)/distance*dy)
        pygame.draw.circle(srf, color, [x, y], radius)
        pointsFigure.append([float(x),float(y)])

def resample(points, n):
    I = pathlength(points) / float(n-1)
    D = 0
    newPoints = [points[0]]
    i = 1
    while i<len(points):
        p_i = points[i]
        d = distance(points[i-1], p_i)
        if (D + d) >= I:
            qx = points[i-1][0] + ((I-D) / d) * (p_i[0] - points[i-1][0])
            qy = points[i-1][1] + ((I-D) / d) * (p_i[1] - points[i-1][1])
            newPoints.append([qx,qy])
            points.insert(i, [qx,qy])
            D = 0
        else: D = D + d
        i+=1
    return newPoints
    
def loadpoint(pointsFigure):
    points=[]
    for point in pointsFigure:
        points.append(Point(float(point[0]), float(point[1])))
    return points

def distance(p1, p2): 
    return float(sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2))

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


def pos_to_point(position):
    x = position[0]
    y = position[1]
    return Point(x,y)
        

try:
    black = Color(0,0,0)
    red = Color(255, 0, 0)
    green = Color(0, 255, 0)    
    valida=0
    pointsFigure = []
    finalPoints = []
    while valida==0:
        e = pygame.event.wait()
        if e.type == pygame.QUIT:
            raise StopIteration
        if e.type == pygame.MOUSEBUTTONDOWN:
            
            screen.fill((0,0,0))
            first_pos = e.pos
            pointsFigure.append(first_pos)
            color = (random.randrange(256), random.randrange(256), random.randrange(256))
            pygame.draw.circle(screen, color, e.pos, radius)
            draw_on = True
        if e.type == pygame.MOUSEBUTTONUP:
                draw_on = False
                lastp_pos = e.pos
                pointsFigure.append(lastp_pos)
                roundline(screen,color,first_pos,lastp_pos,radius)
                pointsFigure = resample(pointsFigure,40)
                #print_points(pointsFigure)
                lastp_pos = (0, 0)
                valida=1
        if e.type == pygame.MOUSEMOTION:
                if draw_on:
                    c+=1
                    pygame.draw.circle(screen, color, e.pos, radius)
                    roundline(screen, color, e.pos, last_pos, radius)
                    #pointsFigure.append(e.pos)
                last_pos = e.pos
        pygame.display.flip()
    archivo = open('prueba.dat','w')
    for posi in pointsFigure:
        poi=pos_to_point(posi)
        finalPoints.append(poi)
        archivo.write(str(format(poi.x,'.5f')) + ' ' + str(format(poi.y,'.5f')) + '\n')
    archivo.close()
    triangulacion(finalPoints)
        
except StopIteration:
    pass

pygame.quit()