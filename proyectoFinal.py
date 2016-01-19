import pygame
import abc
import sys
import PIL
from PIL import Image
# -----------
# Constantes
# -----------
 
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

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
 
# ------------------------------
# Funcion principal del juego
# ------------------------------

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill([255,255,255])
    pygame.display.set_caption("FIGUREAR")
    
    botonCerrar = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # Boton Nuevo
        if (0< mouse[0] <60) and (0< mouse[1] <96):
            # Boton Nuevo over
            pygame.draw.rect(screen, [79,255,5] ,(0, 0, 60, 96)) 
            # Accion Boton Nuevo
            if click[0] == 1:
                print "Nuevo"
        else:
            # Boton Nuevo
            pygame.draw.rect(screen, [0,255,0] ,(0, 0, 60, 96)) # boton Nuevo
        
        # Boton Dibujar
        if (0<mouse[0]<60) and (96<mouse[1]<192):
            # Boton Dibujar over
            pygame.draw.rect(screen,[255,240,10], (0,96, 60,96))
            # Accion clic de Dibujar
            if click[0] == 1:
                print "Dibujar"
        else:
            # Boton Dibujar
            pygame.draw.rect(screen, [255,255,0] ,(0,96, 60,96))# boton Dibujar
        
        # Boton Tachuela
        if (0<mouse[0]<60) and (192<mouse[1]<288):
            # Boton Tachuela over
            pygame.draw.rect(screen, [0,230,245], (0,192,60,96))
            # Accion clic de Tachuela
            if click[0] == 1:
                print "Tachuela"
        else:
            # Boton Tachuela
            pygame.draw.rect(screen, [0,255,245] ,(0,192,60,96)) # boton Tachuela
        
        # Boton Mover
        if (0< mouse[0]< 60) and (288<mouse[1]<384):
            # Boton Mover over
            pygame.draw.rect(screen, [150,86,245] ,(0,288,60,96))
            # Accion Boton Mover
            if click[0] == 1:
                print "Mover"
        else:
            # Boton Mover
            pygame.draw.rect(screen, [0,86,245] ,(0,288,60,96))# boton mover
            
        # Boton Salir
        if ( 0< mouse[0]< 60) and (384 < mouse[1] < SCREEN_HEIGHT):
            # Boton Salir over
            pygame.draw.rect(screen, [255,100,100] ,(0,384,60,96))
            # Accion Boton Salir
            if click[0] == 1:
                print "Salir"
        else:
            pygame.draw.rect(screen, [255,0,0] ,(0,384,60,96))# boton salir
        
        btn_nuevo = pygame.image.load("imagenes/nuevo.png").convert_alpha()
        btn_dibujar = pygame.image.load("imagenes/dibujar.png").convert_alpha()
        btn_tachuela = pygame.image.load("imagenes/tachuela.png").convert_alpha()
        btn_mover = pygame.image.load("imagenes/mover.png").convert_alpha()
        btn_salir = pygame.image.load("imagenes/salir.png").convert_alpha()
        screen.blit(btn_nuevo,(10,30))
        screen.blit(btn_dibujar,(10,96+30))
        screen.blit(btn_tachuela,(10,192+30))
        screen.blit(btn_mover,(10,288+30))
        screen.blit(btn_salir,(10,384+30))
        
        pygame.display.update()
        
        
        
if __name__ == "__main__":
    main()