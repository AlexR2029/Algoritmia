

import pygame
from tablero import Tablero
from ui import InterfazUsuario
import constantes


def main():

    pygame.init()
    
    numero_minas = int(constantes.FILAS * constantes.COLUMNAS * .2)
    ANCHO_VENTANA = constantes.COLUMNAS * constantes.TAMAÑO_CELDA
    ALTO_VENTANA = constantes.FILAS * constantes.TAMAÑO_CELDA + constantes.ALTO_PANEL_SUPERIOR

    # Crear ventana
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption(" Buscaminas ")
    reloj = pygame.time.Clock()
    tablero = Tablero(constantes.FILAS, constantes.COLUMNAS, constantes.TAMAÑO_CELDA, numero_minas)
    interfaz = InterfazUsuario(ANCHO_VENTANA, constantes.ALTO_PANEL_SUPERIOR)

    running = True
    juego_iniciado = False  
    COLOR_FONDO = (40, 40, 40)
    
    while running:
        # Procesar eventos
        for evento in pygame.event.get():
            # Cerrar ventana
            if evento.type == pygame.QUIT:
                running = False
            
            # Eventos del mouse
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x_mouse, y_mouse = pygame.mouse.get_pos()
                
                # Verificar click en botón de reinicio
                if interfaz.boton_reinicio_clickeado(x_mouse, y_mouse):
                    tablero.reiniciar()
                    interfaz.reiniciar_cronometro()
                    juego_iniciado = False
                    continue
                
                # Obtener celda clickeada
                celda_clickeada = tablero.obtener_celda_en_posicion(
                    x_mouse, y_mouse, constantes.ALTO_PANEL_SUPERIOR
                )
                
                if celda_clickeada is not None:
                    if evento.button == 1: 
                        if not juego_iniciado:
                            interfaz.iniciar_cronometro()
                            juego_iniciado = True
                        
                        tablero.revelar_celda(celda_clickeada)
                        
                        if tablero.juego_terminado:
                            interfaz.pausar_cronometro()
                    
                    elif evento.button == 3:
                        tablero.alternar_bandera(celda_clickeada)
        
        pantalla.fill(COLOR_FONDO)
        

        tablero.dibujar(pantalla, constantes.ALTO_PANEL_SUPERIOR)
        interfaz.dibujar_panel_superior(pantalla,numero_minas,tablero.obtener_banderas_colocadas(numero_minas),tablero.juego_terminado,tablero.victoria
        )
        
        pygame.display.flip()
        reloj.tick(60)
    
    pygame.quit()


if __name__ == "__main__":
    main()
