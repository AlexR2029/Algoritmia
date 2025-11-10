"""
Archivo Principal
====
Loop principal del juego con manejo de eventos y lógica de interacción.

Controles:
- Click izquierdo: revelar celda
- Click derecho: colocar/quitar bandera
- Botón "Reiniciar": empezar nuevo juego

Objetivo:
Revelar todas las celdas sin minas, evitando clickear en las minas.
"""

import pygame
from grid import Tablero
from ui import InterfazUsuario
import constantes


def main():
    """
    Función principal que ejecuta el juego Buscaminas.
    
    Inicializa pygame, crea el tablero y la interfaz, y ejecuta el loop principal
    manejando eventos del mouse y actualizando la pantalla.
    """
    # Configuración de pygame
    pygame.init()
    
    # Configuración del tablero

    numero_minas = int(constantes.FILAS * constantes.COLUMNAS * .2)  # Aproximadamente 1/5 del tablero son minas
    
    # Calcular dimensiones de la ventana
    ANCHO_VENTANA = constantes.COLUMNAS * constantes.TAMAÑO_CELDA
    

    ALTO_VENTANA = constantes.FILAS * constantes.TAMAÑO_CELDA + constantes.ALTO_PANEL_SUPERIOR

    # Crear ventana
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption(" Buscaminas ")
    reloj = pygame.time.Clock()
    
    # Crear objetos del juego
    tablero = Tablero(constantes.FILAS, constantes.COLUMNAS, constantes.TAMAÑO_CELDA, numero_minas)
    interfaz = InterfazUsuario(ANCHO_VENTANA, constantes.ALTO_PANEL_SUPERIOR)
    
    # Estado del juego
    running = True
    juego_iniciado = False  # Para iniciar el cronómetro en el primer click
    
    # Color de fondo
    COLOR_FONDO = (40, 40, 40)
    
    # Loop principal del juego
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
                    # Reiniciar juego
                    tablero.reiniciar()
                    interfaz.reiniciar_cronometro()
                    juego_iniciado = False
                    continue
                
                # Obtener celda clickeada (restar altura del panel superior)
                celda_clickeada = tablero.obtener_celda_en_posicion(
                    x_mouse, y_mouse, constantes.ALTO_PANEL_SUPERIOR
                )
                
                if celda_clickeada is not None:
                    # Click izquierdo: revelar celda
                    if evento.button == 1:  # Botón izquierdo
                        # Iniciar cronómetro en el primer click
                        if not juego_iniciado:
                            interfaz.iniciar_cronometro()
                            juego_iniciado = True
                        
                        # Revelar celda
                        tablero.revelar_celda(celda_clickeada)
                        
                        # Si el juego terminó, pausar cronómetro
                        if tablero.juego_terminado:
                            interfaz.pausar_cronometro()
                    
                    # Click derecho: colocar/quitar bandera
                    elif evento.button == 3:  # Botón derecho
                        tablero.alternar_bandera(celda_clickeada)
        
        # Dibujar todo
        pantalla.fill(COLOR_FONDO)
        

        tablero.dibujar(pantalla, constantes.ALTO_PANEL_SUPERIOR)
        # Dibujar panel superior
        interfaz.dibujar_panel_superior(
            pantalla,
            numero_minas,
            tablero.obtener_banderas_colocadas(numero_minas),
            tablero.juego_terminado,
            tablero.victoria
        )
        
        # Dibujar tablero
        
        
        # Actualizar pantalla
        pygame.display.flip()
        
        # Limitar FPS
        reloj.tick(60)
    
    # Cerrar pygame
    pygame.quit()


if __name__ == "__main__":
    main()
