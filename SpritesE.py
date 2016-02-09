
 
import pygame
import random
from math import sin, cos, atan2, sqrt, pi
 
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
puntos_remuestreados =[]
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
        bloque = Bloque(color, 10,10)
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
            bloque = Bloque(color, 10,10)
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


def btnDibujar():
    global ESTADO
    global bloque_lista
    global screen
    global puntos_remuestreados
    # Esta es una lista de 'sprites.' Cada bloque en el programa es
    # aniadido a la lista. La lista es gestionada por una clase llamada 'Group.'
    # Esta es una lista de cada uno de los sprites. Asi como del resto de bloques y el bloque protagonista..
    color = (random.randrange(256), random.randrange(256), random.randrange(256))
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
                print "dio clic y lo mantiene"
                draw_on = True
                #pygame.draw.circle(screen, color, e.pos, radius)
                bloque = Bloque(color, 10,10)
                first_pos = e.pos
                last_pos = e.pos
               # Establecemos una ubicacion aleatoria para el bloque
                pos = pygame.mouse.get_pos()
                # Extraemos la x e y de la lista, 
                bloque.rect.x = pos[0]
                bloque.rect.y = pos[1]
                screen.blit(bloque.image,( bloque.rect.x,bloque.rect.y))
                # Aniadimos el  bloque a la lista de objetos
                bloque_lista.append(bloque)
                print bloque_lista[0].rect.x, bloque_lista[0].rect.y
                    
            if e.type == pygame.MOUSEBUTTONUP:
                print "solto el clic"
                bloque = Bloque(color, 10,10)
                # Establecemos una ubicacion aleatoria para el bloque
                pos = pygame.mouse.get_pos()
                # Extraemos la x e y de la lista, 
                bloque.rect.x = pos[0]
                bloque.rect.y = pos[1]
                # Aniadimos el  bloque a la lista de objetos
                bloque_lista.append(bloque)
                screen.blit(bloque.image,( bloque.rect.x,bloque.rect.y))
                draw_on = False
                lastp_pos = e.pos
                roundline(screen, color,first_pos,lastp_pos,radius)
                #resample(bloque_lista,40,color)
                print bloque_lista[len(bloque_lista)-1].rect.x, bloque_lista[len(bloque_lista)-1].rect.y
                print len(bloque_lista)
                i=0
                x=0
                y=0
                while i<len(bloque_lista):
                    print bloque_lista[i].rect.x , bloque_lista[i].rect.y
                    x = x +bloque_lista[i].rect.x
                    y = y + bloque_lista[i].rect.y
                    i=i+1
                posx = x/len(bloque_lista)
                posy = y/len(bloque_lista)
                B = Bloque(color, 3,3)
                # Extraemos la x e y de la lista, 
                B.rect.x = posx
                B.rect.y = posy
                # Aniadimos el  bloque a la lista de objetos
                screen.blit(B.image,( B.rect.x,B.rect.y))
                print x , y
                ESTADO = "N1"

            if e.type == pygame.MOUSEMOTION :
                if draw_on:
                    print "dibujando"
                    bloque = Bloque(color, 10,10)
                        # Establecemos una ubicacion aleatoria para el bloque
                    if e.pos[0]>70:
                        pos = pygame.mouse.get_pos()
                        roundline(screen, color, e.pos, last_pos, radius)
                    last_pos = e.pos
                    pygame.display.flip()
    

            

        
 
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
      
    while True:
        #print ESTADO 
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
                    btnDibujar()                    
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
            
        pygame.display.update()




       

#-----------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
    

 
  
     
