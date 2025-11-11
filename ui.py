import pygame


class InterfazUsuario:

    
    def __init__(self, ancho_pantalla, alto_panel_superior=120):
    
        # Inicializa la interfaz de usuario.

        self.ancho_pantalla = ancho_pantalla
        self.alto_panel = alto_panel_superior
        
        # Colores
        self.COLOR_FONDO_PANEL = (60, 60, 60)        
        self.COLOR_TEXTO = (255, 255, 255)           
        self.COLOR_BOTON = (100, 200, 100)           
        self.COLOR_BOTON_HOVER = (120, 220, 120)    
        self.COLOR_VICTORIA = (50, 200, 50)          
        self.COLOR_DERROTA = (200, 50, 50)           
        
        # Fuentes
        self.fuente_grande = pygame.font.Font(None, 48)
        self.fuente_mediana = pygame.font.Font(None, 36)
        self.fuente_pequeña = pygame.font.Font(None, 28)
        
        # Botón de reinicio
        self.boton_ancho = 150
        self.boton_alto = 50
        self.boton_x = (ancho_pantalla - self.boton_ancho) // 2
        self.boton_y = 15
        self.boton_rect = pygame.Rect(self.boton_x, self.boton_y, 
                                      self.boton_ancho, self.boton_alto)
        # Cronómetro
        self.tiempo_inicio = None
        self.tiempo_pausado = 0
    
    def iniciar_cronometro(self):
        self.tiempo_inicio = pygame.time.get_ticks()
        self.tiempo_pausado = 0
    
    def pausar_cronometro(self):
        if self.tiempo_inicio is not None:
            self.tiempo_pausado = pygame.time.get_ticks() - self.tiempo_inicio
    
    def obtener_tiempo_transcurrido(self):
        # Obtiene el tiempo transcurrido en segundos.
        if self.tiempo_inicio is None:
            return 0
        
        if self.tiempo_pausado > 0:
            return self.tiempo_pausado // 1000
        
        return (pygame.time.get_ticks() - self.tiempo_inicio) // 1000
    
    def reiniciar_cronometro(self):
        self.tiempo_inicio = None
        self.tiempo_pausado = 0
    
    def dibujar_panel_superior(self, pantalla, numero_minas, banderas_colocadas, 
                              juego_terminado, victoria):

        # Dibuja el panel superior con toda la información del juego.
        
        pygame.draw.rect(pantalla, self.COLOR_FONDO_PANEL, 
                        (0, 0, self.ancho_pantalla, self.alto_panel))
        
        self._dibujar_boton_reinicio(pantalla)
        
        # Información de minas restantes
        minas_restantes = numero_minas - banderas_colocadas
        texto_minas = self.fuente_mediana.render(
            f" Minas: {minas_restantes}", True, self.COLOR_TEXTO
        )
        pantalla.blit(texto_minas, (10, 75))
        
        # Tiempo transcurrido
        tiempo = self.obtener_tiempo_transcurrido()
        texto_tiempo = self.fuente_mediana.render(
            f"Tiempo: {tiempo}s", True, self.COLOR_TEXTO
        )
        pantalla.blit(texto_tiempo, (self.ancho_pantalla - 200, 75))
        
        # Mensaje de estado si el juego terminó
        if juego_terminado:
            if victoria:
                self._dibujar_mensaje_victoria(pantalla, tiempo)
            else:
                self._dibujar_mensaje_derrota(pantalla)
    
    def _dibujar_boton_reinicio(self, pantalla):
        
        # Dibuja el botón de reinicio en el panel superior.
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.boton_rect.collidepoint(mouse_x, mouse_y):
            color = self.COLOR_BOTON_HOVER
        else:
            color = self.COLOR_BOTON
        
        pygame.draw.rect(pantalla, color, self.boton_rect, border_radius=10)
        pygame.draw.rect(pantalla, self.COLOR_TEXTO, self.boton_rect, 3, border_radius=10)
        
        texto = self.fuente_mediana.render("Reiniciar", True, self.COLOR_TEXTO)
        texto_rect = texto.get_rect(center=self.boton_rect.center)
        pantalla.blit(texto, texto_rect)
    
    def _dibujar_mensaje_victoria(self, pantalla, tiempo):
    
        # Dibuja mensaje de victoria en el centro de la pantalla.
        
        overlay = pygame.Surface((self.ancho_pantalla, 150))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        overlay_y = (pantalla.get_height() - 150) // 2
        pantalla.blit(overlay, (0, overlay_y))
    
        texto_victoria = self.fuente_grande.render(
            " ¡VICTORIA! ", True, self.COLOR_VICTORIA
        )
        texto_rect = texto_victoria.get_rect(
            center=(self.ancho_pantalla // 2, overlay_y + 50)
        )
        pantalla.blit(texto_victoria, texto_rect)
        
        texto_tiempo = self.fuente_mediana.render(
            f"Tiempo: {tiempo} segundos", True, self.COLOR_TEXTO
        )
        tiempo_rect = texto_tiempo.get_rect(
            center=(self.ancho_pantalla // 2, overlay_y + 100)
        )
        pantalla.blit(texto_tiempo, tiempo_rect)
    
    def _dibujar_mensaje_derrota(self, pantalla):
        overlay = pygame.Surface((self.ancho_pantalla, 100))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        
        overlay_y = (pantalla.get_height() - 100) // 2
        pantalla.blit(overlay, (0, overlay_y))
        
        texto_derrota = self.fuente_grande.render(
            "¡BOOM! Has perdido", True, self.COLOR_DERROTA
        )
        texto_rect = texto_derrota.get_rect(
            center=(self.ancho_pantalla // 2, overlay_y + 50)
        )
        pantalla.blit(texto_derrota, texto_rect)
    
    def boton_reinicio_clickeado(self, x, y):
        return self.boton_rect.collidepoint(x, y)
    
    def obtener_altura_panel(self):
        return self.alto_panel
