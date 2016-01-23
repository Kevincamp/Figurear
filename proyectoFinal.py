import pygame, random
import abc
import sys
import PIL
from PIL import Image
# -----------
# Constantes
# -----------
 
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_WIDTH_4PLAY = 544
BLANCO = (255, 255, 255)
PLOMO = (121,128,129)
NEGRO = (0,0,0)
ESTADO = "N"





# ------------------------------
# Clases y Funciones utilizadas
# ------------------------------




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
    dx = int(end[0])- int(start[0])
    dy = int(end[1])-int(start[1])
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int( start[0]+float(i)/distance*dx)
        y = int( start[1]+float(i)/distance*dy)
        pygame.draw.circle(srf, color, [x, y], radius)
        #pointsFigure.append([float(x),float(y)])
        
 
def nuevoDibujo(screen):
    screen_for_play = screen
    screen.fill([255,255,255])
     
def btnDibujar(screen):
    global ESTADO
    draw_on = False
    color = (255, 128, 0)
    #first_pos = [SCREEN_WIDTH_4PLAY/2, SCREEN_HEIGHT/2]
    #lastp_pos = [0, 0]
    last_pos = (0, 0)
    radius = 3
    valida=0
    while ESTADO == "N":
        e = pygame.event.wait()
        if e.type == pygame.MOUSEBUTTONDOWN:
            #first_pos = e.pos
            color = (random.randrange(256), random.randrange(256), random.randrange(256))
            pygame.draw.circle(screen, color, e.pos, radius)
            draw_on = True
        if e.type == pygame.MOUSEBUTTONUP:
                draw_on = False
                #lastp_pos = e.pos
                #roundline(screen, color,first_pos,lastp_pos,radius)
                #lastp_pos = (0, 0)
                #ESTADO = "D"
        if e.type == pygame.MOUSEMOTION:
                if draw_on:
                    pygame.draw.circle(screen, color, e.pos, radius)
                    roundline(screen, color, e.pos, last_pos, radius)
                last_pos = e.pos
        pygame.display.flip()
 

    




# ------------------------------
# Funcion principal del juego
# ------------------------------





def main():
    global ESTADO
    ESTADO = "none"
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(PLOMO)
    pygame.display.set_caption("FIGUREAR")
    botonCerrar = False
    
    while True:
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
                    pygame.draw.rect(screen, [0,255,245] ,(0,192,60,96)) # Activo Boton Tachuela
                    btnDibujar(screen)
                    #ESTADO = "D"
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
                    ESTADO = "T"
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