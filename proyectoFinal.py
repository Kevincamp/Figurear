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
    
    altoBoton = SCREEN_HEIGHT/5
    #(posicion-x,posicion-y,tamano-ancho,tamano-alto)
    pygame.draw.rect(screen, [0,255,0] ,(SCREEN_WIDTH*0, SCREEN_HEIGHT, 60, altoBoton)) # boton Nuevo
    #pygame.draw.rect(screen, [255,255,0] ,(SCREEN_WIDTH*0,SCREEN_HEIGHT +altoBoton, 60,altoBoton))# boton Dibujar
    #pygame.draw.rect(screen, [0,255,245] ,(screen_width_Nuevo,screen_height_Nuevo+120,60,SCREEN_HEIGHT/5)) # boton Tachuela
    #pygame.draw.rect(screen, [0,86,245] ,(screen_width_Nuevo,screen_height_Nuevo+180,60,SCREEN_HEIGHT/5))# boton mover
    #pygame.draw.rect(screen, [100,100,245] ,(screen_width_Nuevo,screen_height_Nuevo+220,60,SCREEN_HEIGHT/5))# boton salir
    #pygame.display.flip()
    
    pygame.display.update()
    
    
    botonCerrar = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        
if __name__ == "__main__":
    main()