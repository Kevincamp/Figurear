import pygame, random
from p2t import *
import abc
import sys
import PIL
import sys
from pygame import Color
from time import clock
from PIL import Image
from pygame.gfxdraw import trigon, line
from sets import Set 
from math import sin, cos, atan2, sqrt, pi
# -----------
# Constantes
# -----------
 
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_WIDTH_4PLAY = 544
BLANCO = (255, 255, 255)
PLOMO = (121,128,129)
AZUL = (0,0,255)
NEGRO = (0,0,0)
ESTADO = "N"
SHAPE = []
black = Color(0,0,0)
red = Color(255, 0, 0)
green = Color(0, 255, 0)  


# ------------------------------
# Sprites utilizadas
# ------------------------------

class Tachuela(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 255, 255))
        pygame.draw.circle(self.image, AZUL, (25, 25), 3, 2)
        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.center = pygame.mouse.get_pos()



# ------------------------------
# Clases y Funciones utilizadas
# ------------------------------



def pathlength(points):
    d = 0
    for i,p_i in enumerate(points[:len(points)-1]):
        d += distance(p_i, points[i+1])
    return d
def distance(p1, p2): 
    return float(sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2))

def pos_to_point(position):
    x = position[0]
    y = position[1]
    return Point(x,y)


def text_objects(text, font):
     textSurface = font.render(text, True, [0,0,0])
     return textSurface, textSurface.get_rect()
     
     
def cargar_imagen ( fichero_imagen ):
    global imagenes
    imagen = imagenes.get ( fichero_imagen, None )
    if imagen is None:
        imagen = pygame.image.load(os.path.join("imagenes",fichero_imagen)).convert()
        imagenes[fichero_imagen] = imagen
        imagen.set_colorkey (  imagen.get_at((0,0)) , pygame.RLEACCEL )
    return imagen
    
    
def roundline(srf, color, start, end,radius=1):
    global SHAPE
    dx = int(end[0])- int(start[0])
    dy = int(end[1])-int(start[1])
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int( start[0]+float(i)/distance*dx)
        y = int( start[1]+float(i)/distance*dy)
        pygame.draw.circle(srf, color, [x, y], radius)
        SHAPE.append([float(x),float(y)])
        
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
    
 
def nuevoDibujo(screen):
    screen_for_play = screen
    screen.fill([255,255,255])
     
def btnDibujar(screen):
    global ESTADO
    global SHAPE
    finalPoints = []
    SHAPE = []
    draw_on = False
    color = (255, 128, 0)
    first_pos = None
    lastp_pos = None
    last_pos = (0, 0)
    radius = 3
    valida=0
    while ESTADO == "N":
        e = pygame.event.wait()
        if e.pos[0]>70:
            if e.type == pygame.MOUSEBUTTONDOWN:
                color = (random.randrange(256), random.randrange(256), random.randrange(256))
                pygame.draw.circle(screen, color, e.pos, radius)
                if e.pos[0]>70:
                  first_pos = e.pos
                  SHAPE.append(first_pos)
                  draw_on = True
            if e.type == pygame.MOUSEBUTTONUP:
                    draw_on = False
                    lastp_pos = e.pos
                    SHAPE.append(lastp_pos)
                    roundline(screen, color,first_pos,lastp_pos,radius)
                    SHAPE = resample(SHAPE,40)
                    ESTADO = "N1"
            if e.type == pygame.MOUSEMOTION:
                    if draw_on:
                        if e.pos[0]>70:
                            pygame.draw.circle(screen, color, e.pos, radius)
                            roundline(screen, color, e.pos, last_pos, radius)
                    last_pos = e.pos
            pygame.display.flip()
    for posi in SHAPE:
        poi=pos_to_point(posi)
        finalPoints.append(poi)
    triangulacion(screen,finalPoints)
    





def triangulacion(screen, polyline):
    global ESTADO
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
        done = True
    print "Se triangulariza el SHAPE"
    ESTADO = "D"


def colocandoTachuela(screen):
    global ESTADO
    draw_on = False
    radiusCircle = 10
    tachuela1 = (0,0)
    tachuela2 = (0,0)
    seleccion = 0
    
    #while ESTADO == "D":
    background = pygame.Surface(screen.get_size())
    background.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    
    circle = Tachuela()
    
    #hide mouse
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                
        #screen.blit
        #allSprites.update()
        allSprites.draw(screen)
        
        pygame.display.flip()
        #e = pygame.event.wait()
        #if e.pos[0]>70:
        #    if e.type == pygame.MOUSEBUTTONDOWN:
        #        pygame.draw.circle(screen, AZUL, e.pos, radiusCircle,5)
        #        if e.pos[0]>70:
        #          first_pos = e.pos
        #          SHAPE.append(first_pos)
        #          draw_on = False
        #    if e.type == pygame.MOUSEBUTTONUP:
        #        print "Alza Boton"
        #        ESTADO = "T"
        #    if e.type == pygame.MOUSEMOTION:
        #        print "Mouse Motion"
        #    pygame.display.flip()
        #    #ESTADO = "T"
                
# ------------------------------
# Funcion principal del juego
# ------------------------------



def main():
    global ESTADO
    global SHAPE
    
    ESTADO = "none"
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(PLOMO)
    pygame.display.set_caption("FIGUREAR")
    botonCerrar = False
      
    while True:
        print ESTADO 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        
        
        if ESTADO == "none":
            pygame.draw.rect(screen, [0,255,0] ,(0, 0, 60, 96))
            pygame.draw.rect(screen, [255,255,0] ,(0,384, 60,96))
            pygame.draw.rect(screen, [255,0,0] ,(0,384,60,96))
            screen.fill(NEGRO)
            
        
        # **************************************************************************************** Boton Nuevo
        if (0< mouse[0] <60) and (0< mouse[1] <96):
            if click[0] == 1:
                nuevoDibujo(screen)
                pygame.draw.rect(screen, [255,255,0] ,(0,96, 60,96)) # Activo Boton dibujar
                ESTADO = "N"
        else:
            pygame.draw.rect(screen, [0,255,0] ,(0, 0, 60, 96))
        
        
        
        # **************************************************************************************** Boton Dibujar
        if ESTADO == "N":
            if (0<mouse[0]<60) and (96<mouse[1]<192):
                if click[0] == 1:
                    btnDibujar(screen)                    
                    if (ESTADO == "D"):
                        pygame.draw.rect(screen, [0,255,245] ,(0,192,60,96)) # Activo Boton Tachuela
            else:
                pygame.draw.rect(screen, [255,255,0] ,(0,96, 60,96))
        else:
            pygame.draw.rect(screen,PLOMO, (0,96, 60,96))
            
        
        # **************************************************************************************** Boton Tachuela
        if ESTADO == "D":
            if (0<mouse[0]<60) and (192<mouse[1]<288):
                if click[0] == 1:
                    pygame.draw.rect(screen,PLOMO, (0,96, 60,96)) # Desactivo Boton Dibujar
                    pygame.draw.rect(screen, [255,164,032],(0,288,60,96)) # Activo Boton Mover
                    colocandoTachuela(screen)
            else:
                pygame.draw.rect(screen, [0,255,245] ,(0,192,60,96))
        else:
            pygame.draw.rect(screen, PLOMO, (0,192,60,96))
        
        # ****************************************************************************************  Boton Mover
        if ESTADO == "T":
            if (0< mouse[0]< 60) and (288<mouse[1]<384):
                if click[0] == 1:
                    pygame.draw.rect(screen, PLOMO, (0,192,60,96)) # Desactivo Boton Tachuela
                    ESTADO = "M"
            else:
                pygame.draw.rect(screen, [255,164,032],(0,288,60,96))
        else:
            pygame.draw.rect(screen, PLOMO,(0,288,60,96))
                    
            
        # **************************************************************************************** Boton Salir
        if ( 0< mouse[0]< 60) and (384 < mouse[1] < SCREEN_HEIGHT):
            if click[0] == 1:
                sys.exit()
        else:
            pygame.draw.rect(screen, [255,0,0] ,(0,384,60,96))
            
        #btn_nuevo = pygame.image.load("imagenes/nuevo.png").convert_alpha()
        #btn_dibujar = pygame.image.load("imagenes/dibujar.png").convert_alpha()
        #btn_tachuela = pygame.image.load("imagenes/tachuela.png").convert_alpha()
        #btn_mover = pygame.image.load("imagenes/mover.png").convert_alpha()
        #btn_salir = pygame.image.load("imagenes/salir.png").convert_alpha()
        #screen.blit(btn_nuevo,(10,30))
        #screen.blit(btn_dibujar,(10,96+30))
        #screen.blit(btn_tachuela,(10,192+30))
        #screen.blit(btn_mover,(10,288+30))
        #screen.blit(btn_salir,(10,384+30))
        pygame.display.update()
        
        
        
if __name__ == "__main__":
    main()