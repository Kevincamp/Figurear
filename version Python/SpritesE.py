import pygame
import random
from math import *
import sys
import pygame.gfxdraw

# Definimos algunos colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_WIDTH_4PLAY = 544
PLOMO = (121,128,129)
AZUL = (0,0,255)
ESTADO = "N"
bloque_lista =[]
lista_puntos = []
puntos_malla =[]
puntos_remuestreados =[]
tachuelas=[]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


#-Clase para cada pixel dibujado
class Bloque(pygame.sprite.Sprite):

    # Constructor. Pasa el color al bloque,
    # y su posicion x e y
    def __init__(self, color, largo, alto):
        # Llama al constructor de la clase padre (Sprite)
        pygame.sprite.Sprite.__init__(self)

        # Crea una imagen del bloque y lo rellena de color.
        # Esto podria ser tambien una imagen cargada desde el disco duro.
        self.image = pygame.Surface([largo, alto])
        self.image.fill(color)

        # Obtenemos el objeto rectangulo que posee las dimensiones de la imagen
        # Actualizamos la posicion de ese objeto estableciendo los valores para
        # rect.x y rect.y
        self.rect = self.image.get_rect()
    def get_rect(self):
        return self.image.get_rect()




def roundline(srf, color, start, end,radius=1):
    global bloque_lista
    global screen
    dx = int(end[0])- int(start[0])
    dy = int(end[1])-int(start[1])
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int( start[0]+float(i)/distance*dx)
        y = int( start[1]+float(i)/distance*dy)
        bloque = Bloque(color, 5,5)
        bloque.rect.x = x
        bloque.rect.y = y
        # Aniadimos el  bloque a la lista de objetos
        bloque_lista.append(bloque)
        screen.blit(bloque.image,( bloque.rect.x,bloque.rect.y))

def distance(p1, p2):
    return float(sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2))


def pathlength(points):
    d = 0
    for i , p in enumerate(points[:len(points)-1]):
        p_i = p.get_rect()
        p_i2= points[i+1] .get_rect()
        p1 =[p_i.x , p_i.y]
        p2 =[p_i2.x , p_i2.y]
        d += distance(p1, p2)
    return d


def resample(points, n,color):
    global screen
    global puntos_remuestreados
    I = pathlength(points) / float(n-1)
    D = 0
    i = 1
    while i<len(points):

        p_i = points[i].get_rect()
        p_i2 = points[i-1].get_rect()
        p1 =[p_i.x , p_i.y]
        p2 =[p_i2.x , p_i2.y]
        d = distance(p2, p1)
        if (D + d) >= I and d !=0:
            qx = p2[0] + ((I-D) / d) * (p1[0] - p2[0])
            qy = p2[1] + ((I-D) / d) * (p1[1] - p2[1])
            bloque = Bloque(color, 5,5)
            bloque.rect.x = qx
            bloque.rect.y = qy
            # Aniadimos el  bloque a la lista de objetos
            puntos_remuestreados.append(bloque)
            screen.blit(bloque.image,( bloque.rect.x,bloque.rect.y))
            D = 0
        else: D = D + d
        i+=1



def nuevoDibujo(screen):
    screen_for_play = screen
    screen.fill([255,255,255])




#-------------------------------------------------------------
def menorDistancia(pos):
    global bloque_lista
    mDistancia =100000000000
    i=0
    nuev_pos=()
    while i<len(bloque_lista):
        posGrafico= [bloque_lista[i].rect.x , bloque_lista[i].rect.y]
        d = distance(pos,posGrafico)
        if d < mDistancia :
            mDistancia=d
            nuev_pos=posGrafico

        i=i+1
    return nuev_pos

def menorDistanciaC(pos):
    global bloque_lista
    mDistancia =100000000000
    indice=0
    i = True
    j=0
    nuev_pos=()
    while i:
        posGrafico= [bloque_lista[j].rect.x , bloque_lista[j].rect.y]
        indice=indice+1
        if pos == posGrafico:
            i=False
        j=j+1
    i=0
    while i<len(bloque_lista):
        posGrafico= [bloque_lista[i].rect.x , bloque_lista[i].rect.y]
        po2= [bloque_lista[indice].rect.x , bloque_lista[indice].rect.y]
        d = distance(po2,posGrafico)
        if d <=20 and d >=14:
            nuev_pos=posGrafico
        i=i+1
    return nuev_pos





def PuntoEnPoligono(pos):
    global bloque_lista
    x= pos[0]
    y= pos[1]
    i = 0
    j = len(bloque_lista) - 1
    salida = False
    for i in range(len(bloque_lista)):
        posix = bloque_lista[i].rect.x
        posiy = bloque_lista[i].rect.y
        posjx = bloque_lista[j].rect.x
        posjy = bloque_lista[j].rect.y
        if (posiy < y and posjy >= y) or (posjy < y and posiy >= y):
            if posix + (y - posiy) / (posjy - posiy) * (posjx - posix) < x:
                salida = not salida
        j = i
    return salida

    #--------------------------------------------------------

def puntoEntreVertices(a,b):
    global bloque_lista
    i=0
    x=0
    y=0
    while i<len(bloque_lista):
        posx=bloque_lista[i].rect.x
        posy=bloque_lista[i].rect.y
        p=[posx,posy]
        if isBetween(a,b,p) :   #isBetween(a,b,c)  o    rectaEntrePuntos(a,b,p)
            return [1,p]
        i=i+1
    return [0,[0,0]]






def seisVertices(posx,posy,color):
    global screen
    global puntos_malla
    global lista_puntos
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    posicion_actual=(posx,posy)

    Puntos = [(-8,-14),(-16,0),(-8,14),(8,14),(16,0),(8,-14)]
    NuevoPuntos = []
    for valor in Puntos:
        #nueva_posicion=((posx+valor[0],posy+valor[1]))
        NuevoPuntos.append((posx+valor[0],posy+valor[1]))
        #pygame.draw.aaline(screen, color, posicion_actual, nueva_posicion, 1)
    # Realizar los demas triangulos a partir de los 6 vertices cn un tamanio de 20
    B1 = Bloque(color, 2,2)
    # Extraemos la x e y de la lista,
    B1.rect.x = posx
    B1.rect.y = posy
    # Aniadimos el  bloque a la lista de objetos
    screen.blit(B1.image,( B1.rect.x,B1.rect.y))
    while len(NuevoPuntos) != 0:
        punto = NuevoPuntos.pop(0)
        if punto not in puntos_malla and PuntoEnPoligono(punto):
            """for valor in Puntos:
                if punto[0]+valor[0]>60 and punto[0]+valor[0]<SCREEN_WIDTH and punto[1]+valor[1]>0 and punto[1]+valor[1]<SCREEN_HEIGHT and PuntoEnPoligono((punto[0]+valor[0],punto[1]+valor[1])):
                    pygame.draw.aaline(screen, color, (punto[0],punto[1]), (punto[0]+valor[0],punto[1]+valor[1]), 1)
                    pygame.gfxdraw.aatrigon(Surface, x1, y1, x2, y2, x3, y3, color):
                    NuevoPuntos.append((punto[0]+valor[0],punto[1]+valor[1]))
                else:
                  pos=menorDistancia(punto)
                  pygame.draw.aaline(screen, color, (punto[0],punto[1]), pos, 1)"""

            indic=0
            while indic < len(Puntos):
              valor = Puntos[indic]
              if indic+1< len(Puntos):
                valor2 = Puntos[indic+1]
                if punto[0]+valor[0]>60 and punto[0]+valor[0]<SCREEN_WIDTH and punto[1]+valor[1]>0 and punto[1]+valor[1]<SCREEN_HEIGHT and PuntoEnPoligono((punto[0]+valor[0],punto[1]+valor[1])):
                    NuevoPuntos.append((punto[0]+valor[0],punto[1]+valor[1]))
                    if punto[0]+valor2[0]>60 and punto[0]+valor2[0]<SCREEN_WIDTH and punto[1]+valor2[1]>0 and punto[1]+valor2[1]<SCREEN_HEIGHT and PuntoEnPoligono((punto[0]+valor2[0],punto[1]+valor2[1])):
                        #pygame.draw.aaline(screen, color, (punto[0],punto[1]), (punto[0]+valor[0],punto[1]+valor[1]), 1)
                        pygame.gfxdraw.aatrigon(screen, punto[0], punto[1], punto[0]+valor[0], punto[1]+valor[1], punto[0]+valor2[0], punto[1]+valor2[1], color)

                    else:
                        pos=menorDistancia(punto)
                        pygame.gfxdraw.aatrigon(screen, punto[0], punto[1], punto[0]+valor[0], punto[1]+valor[1], pos[0], pos[1], color)
                        #pygame.gfxdraw.aatrigon(screen, x1, y1, x2, y2, x3, y3, color):

                else:
                    #pygame.draw.aaline(screen, color, (punto[0],punto[1]), pos, 1)
                    if punto[0]+valor2[0]>60 and punto[0]+valor2[0]<SCREEN_WIDTH and punto[1]+valor2[1]>0 and punto[1]+valor2[1]<SCREEN_HEIGHT and PuntoEnPoligono((punto[0]+valor2[0],punto[1]+valor2[1])):
                        pos=menorDistancia(punto)
                        #pygame.draw.aaline(screen, color, (punto[0],punto[1]), (punto[0]+valor[0],punto[1]+valor[1]), 1)
                        pygame.gfxdraw.aatrigon(screen, punto[0], punto[1], punto[0]+valor2[0], punto[1]+valor2[1], pos[0], pos[1], color)

                    else:
                        pos=menorDistancia(punto)
                        pos1=menorDistanciaC(pos)
                        if distance(punto,pos)<= 22  and distance(punto, pos1)<= 22 and distance(pos,pos1)<=22:
                            pygame.gfxdraw.aatrigon(screen, punto[0], punto[1], pos[0], pos[1], pos1[0], pos1[1], color)
                        #pygame.gfxdraw.aatrigon(screen, x1, y1, x2, y2, x3, y3, color):
              indic=indic+1

            puntos_malla.append(punto)
            BverticeDer = Bloque(color, 2,2)
            BverticeDer.rect.x = punto[0]
            BverticeDer.rect.y = punto[1]
            screen.blit(BverticeDer.image,( BverticeDer.rect.x,BverticeDer.rect.y))
            pygame.display.flip()



def encontrar_centroide(color):
    global bloque_lista
    global screen
    global puntos_malla
    i=0
    x=0
    y=0
    while i<len(bloque_lista):
        x = x +bloque_lista[i].rect.x
        y = y + bloque_lista[i].rect.y
        i=i+1
    posx = int(x/len(bloque_lista))
    posy = int(y/len(bloque_lista))
    print("encontro centroide")
    seisVertices(posx,posy,color)
    print("encontro los primeros vertices")
    j=0
    while j < len(puntos_malla):
        p_i=puntos_malla[j]
        p=p_i[0]
        if p_i[1]==0:
            seisVertices(p[0],p[1],color)
        j=j+1
    print("listo kalisto")

def setaerVariables():
    global lista_puntos
    global ESTADO
    global bloque_lista
    global puntos_remuestreados
    global tachuelas
    lista_puntos[:] = []
    ESTADO="none"
    bloque_lista[:] = []
    puntos_remuestreados[:] = []
    tachuelas[:] = []


def btnDibujar():
    global lista_puntos
    global ESTADO
    global bloque_lista
    global screen
    global puntos_remuestreados
    # Esta es una lista de 'sprites.' Cada bloque en el programa es
    # aniadido a la lista. La lista es gestionada por una clase llamada 'Group.'
    # Esta es una lista de cada uno de los sprites. Asi como del resto de bloques y el bloque protagonista..
    #color = (random.randrange(256), random.randrange(256), random.randrange(256))
    color = (8,46,84)
    draw_on = False
    termino = False
    radius = 3
    first_pos = None
    lastp_pos = None
    last_pos = (0, 0)
    #  Se usa para establecer cuan rapido se actualiza la pantalla
    reloj = pygame.time.Clock()
    while ESTADO == "N":
        # Limitamos a 20 fotogramas por segundo
        reloj.tick(60)
        e = pygame.event.wait()
        if e.pos[0]>70:
            if e.type == pygame.MOUSEBUTTONDOWN:
                print("dio clic y lo mantiene")
                draw_on = True
                #pygame.draw.circle(screen, color, e.pos, radius)
                bloque = Bloque(color, 5,5)
                first_pos = e.pos
                last_pos = e.pos
               # Establecemos una ubicacion aleatoria para el bloque
                pos = pygame.mouse.get_pos()
                lista_puntos.append(e.pos)
                # Extraemos la x e y de la lista,
                bloque.rect.x = pos[0]
                bloque.rect.y = pos[1]
                screen.blit(bloque.image,( bloque.rect.x,bloque.rect.y))
                # Aniadimos el  bloque a la lista de objetos
                bloque_lista.append(bloque)
                print(bloque_lista[0].rect.x, bloque_lista[0].rect.y)

            if e.type == pygame.MOUSEBUTTONUP:
                print("solto el clic")
                bloque = Bloque(color, 5,5)
                # Establecemos una ubicacion aleatoria para el bloque
                pos = pygame.mouse.get_pos()
                # Extraemos la x e y de la lista,
                bloque.rect.x = pos[0]
                bloque.rect.y = pos[1]
                lista_puntos.append(e.pos)
                # Aniadimos el  bloque a la lista de objetos
                bloque_lista.append(bloque)
                screen.blit(bloque.image,( bloque.rect.x,bloque.rect.y))
                draw_on = False
                lastp_pos = e.pos
                roundline(screen, color,first_pos,lastp_pos,radius)
                #resample(bloque_lista,40,color)
                pygame.display.flip()
                encontrar_centroide(color)
                ESTADO = "D"

            if e.type == pygame.MOUSEMOTION :
                if draw_on:
                    print("dibujando")
                    bloque = Bloque(color, 5,5)
                        # Establecemos una ubicacion aleatoria para el bloque
                    if e.pos[0]>70:
                        pos = pygame.mouse.get_pos()
                        roundline(screen, color, e.pos, last_pos, radius)
                    last_pos = e.pos
                    pygame.display.flip()

def menorDistanciaTachuelas(pos):
    global puntos_malla
    mDistancia =100000000000
    i=0
    nuev_pos=()
    while i<len(puntos_malla):
        posGrafico= [puntos_malla[i][0] , puntos_malla[i][1]]
        d = distance(pos,posGrafico)
        if d < mDistancia :
            mDistancia=d
            nuev_pos=posGrafico

        i=i+1
    return nuev_pos


def colocandoTachuela():
    global tachuelas
    global ESTADO
    global puntos_malla
    global screen
    print("colocando tachuela")
    while ESTADO == "D":
        e = pygame.event.wait()
        #print(mouse , click[0])
        if e.type == pygame.MOUSEBUTTONUP :
            pos = pygame.mouse.get_pos()
            if PuntoEnPoligono(pos):
                tachuela = menorDistanciaTachuelas(pos)
                pygame.draw.circle(screen, (102,0,0), tachuela, 8)
                tachuelas.append(tachuela)
                #bloque = Bloque([255,0,0], 15,15)
                #bloque.rect.x = pos[0]
                #bloque.rect.y = pos[1]
                #screen.blit(bloque.image,( bloque.rect.x,bloque.rect.y))
                pygame.display.flip()
                ESTADO = "T"
                print("esta tachuela en la figura")



# Inicializamos Pygame
def main():
    global ESTADO
    global screen
    ESTADO = "none"
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(PLOMO)
    pygame.display.set_caption("FIGUREAR")
    botonCerrar = False
    salirN = pygame.image.load("salirN.png").convert_alpha()
    salirA = pygame.image.load("salirA.png").convert_alpha()
    dibujarN = pygame.image.load("dibujarN.png").convert_alpha()
    dibujarA = pygame.image.load("dibujarA.png").convert_alpha()
    dibujarP = pygame.image.load("dibujarP.png").convert_alpha()
    moverN = pygame.image.load("moverN.png").convert_alpha()
    moverA = pygame.image.load("moverA.png").convert_alpha()
    moverP = pygame.image.load("moverP.png").convert_alpha()
    nuevoN = pygame.image.load("nuevoN.png").convert_alpha()
    nuevoA = pygame.image.load("nuevoA.png").convert_alpha()
    tachuelaA = pygame.image.load("tachuelaA.png").convert_alpha()
    tachuelaN = pygame.image.load("tachuelaN.png").convert_alpha()
    tachuelaP = pygame.image.load("tachuelaP.png").convert_alpha()





    while True:
        #print ESTADO
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()




        if ESTADO == "none":
            #pygame.draw.rect(screen, [0,255,0] ,(0, 0, 60, 96))
            #pygame.draw.rect(screen, [255,255,0] ,(0,384, 60,96))
            #pygame.draw.rect(screen, [255,0,0] ,(0,384,60,96))
            screen.fill(NEGRO)
            screen.blit(nuevoA,(5,13))
            screen.blit(dibujarN,(0,103))
            screen.blit(tachuelaN,(0,199))
            screen.blit(moverN,(0,295))
            screen.blit(salirA,(0,397))
            pygame.display.flip()


        # **************************************************************************************** Boton Nuevo
        if (0< mouse[0] <60) and (0< mouse[1] <96): #nuevo
            if click[0] == 1:
                nuevoDibujo(screen)
                #pygame.draw.rect(screen, [255,255,0] ,(0,96, 60,96)) # Activo Boton dibujar
                screen.blit(dibujarA,(0,103))
                screen.blit(nuevoA,(5,13))
                screen.blit(tachuelaN,(0,199))
                screen.blit(moverN,(0,295))
                screen.blit(salirA,(0,397))
                pygame.display.flip()
                setaerVariables()
                ESTADO = "N"
        """"else:
            #pygame.draw.rect(screen, [0,255,0] ,(0, 0, 60, 96))
            screen.blit(nuevoA,(0,13))
            screen.blit(dibujarN,(0,103))
            pygame.display.flip()"""""




        # **************************************************************************************** Boton Dibujar
        if ESTADO == "N":
            if (0<mouse[0]<60) and (96<mouse[1]<192):  #dibujar
                if click[0] == 1:
                    screen.blit(dibujarP,(0,103))
                    pygame.display.flip()
                    btnDibujar()
                    if (ESTADO == "D"):
                        #pygame.draw.rect(screen, [0,255,245] ,(0,192,60,96)) # Activo Boton Tachuela
                        screen.blit(tachuelaA,(0,199))
                        screen.blit(dibujarN,(0,103))
                        screen.blit(nuevoA,(5,13))
                        screen.blit(moverN,(0,295))
                        screen.blit(salirA,(0,397))
                        pygame.display.flip()

            """else:
                #pygame.draw.rect(screen, [255,255,0] ,(0,96, 60,96))
                screen.blit(dibujarA,(0,103))
                pygame.display.flip()"""
        else:
            #pygame.draw.rect(screen,PLOMO, (0,96, 60,96))
            #screen.blit(dibujarN,(0,103))
            pygame.display.flip()


        # **************************************************************************************** Boton Tachuela
        if ESTADO == "D" or ESTADO == "T" : #tachuela
            if (0<mouse[0]<60) and (192<mouse[1]<288):
                if click[0] == 1:
                    ESTADO = "D"
                    #pygame.draw.rect(screen,PLOMO, (0,96, 60,96)) # Desactivo Boton Dibujar
                    #pygame.draw.rect(screen, [255,164,032],(0,288,60,96)) # Activo Boton Mover
                    #screen.blit(dibujarA,(0,103))
                    screen.blit(moverA,(0,295))
                    screen.blit(tachuelaP,(0,199))
                    screen.blit(nuevoA,(5,13))
                    screen.blit(dibujarN,(0,103))
                    screen.blit(salirA,(0,397))
                    pygame.display.flip()
                    #ESTADO = "T"  # hasta realizar el de boton tachuela
                    colocandoTachuela()
                    screen.blit(tachuelaA,(0,199))
                    pygame.display.flip()
            """else:
                #pygame.draw.rect(screen, [0,255,245] ,(0,192,60,96))
                screen.blit(tachuelaA,(0,199))
                pygame.display.flip()"""
        else:
            #pygame.draw.rect(screen, PLOMO, (0,192,60,96))
            #screen.blit(tachuelaN,(0,199))
            pygame.display.flip()

        # ****************************************************************************************  Boton Mover
        if ESTADO == "T": #mover
            if (0< mouse[0]< 60) and (288<mouse[1]<384):

                if click[0] == 1:
                    #pygame.draw.rect(screen, PLOMO, (0,192,60,96)) # Desactivo Boton Tachuela
                    screen.blit(tachuelaN,(0,199))
                    screen.blit(moverN,(0,295))
                    screen.blit(nuevoA,(5,13))
                    screen.blit(dibujarN,(0,103))
                    screen.blit(salirA,(0,397))
                    pygame.display.flip()
                    ESTADO = "D"
            """else:
                #pygame.draw.rect(screen, [255,164,032],(0,288,60,96))
                screen.blit(tachuelaA,(0,199))
                pygame.display.flip()"""
        else:
            #pygame.draw.rect(screen, PLOMO,(0,288,60,96))
            #screen.blit(moverN,(0,295))
            pygame.display.flip()


        # **************************************************************************************** Boton Salir
        if ( 0< mouse[0]< 60) and (384 < mouse[1] < SCREEN_HEIGHT):
            if click[0] == 1:
                sys.exit()
        else:
            #pygame.draw.rect(screen, [255,0,0] ,(0,384,60,96))
            screen.blit(salirA,(0,397))
            pygame.display.flip()

        pygame.display.update()







#-----------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
