

import pygame


class Celda:

    
    def __init__(self, fila, columna, tamaño):
        
        # Inicializa una celda del tablero.
        
        self.fila = fila
        self.columna = columna
        self.tamaño = tamaño
        
        # Estados de la celda
        self.es_mina = False
        self.esta_revelada = False
        self.tiene_bandera = False
        self.minas_adyacentes = 0
        
        # Colores para dibujar
        self.COLOR_SIN_REVELAR = (100, 100, 100)  
        self.COLOR_REVELADA = (200, 200, 200)    
        self.COLOR_MINA = (255, 50, 50)           
        self.COLOR_BANDERA = (255, 255, 0)        
        self.COLOR_BORDE = (255, 255, 255)       
        self.COLOR_TEXTO = (0, 0, 0)              
        
        # Colores para números según cantidad de minas adyacentes
        self.COLORES_NUMEROS = {
            1: (0, 0, 255),      
            2: (0, 128, 0),      
            3: (255, 0, 0),      
            4: (0, 0, 128),      
            5: (128, 0, 0),      
            6: (0, 128, 128),    
            7: (0, 0, 0),        
            8: (128, 128, 128),  
        }
    
    def dibujar(self, pantalla, posicion_y_tablero=0):
        # Dibuja la celda en la pantalla según su estado.
      
        x = self.columna * self.tamaño
        y = self.fila * self.tamaño + posicion_y_tablero
    
        rect = pygame.Rect(x, y, self.tamaño, self.tamaño)
        
        if self.esta_revelada:
            if self.es_mina:
                color = self.COLOR_MINA
            else:
                color = self.COLOR_REVELADA
        else:
            color = self.COLOR_SIN_REVELAR
        
        # Dibujar celda
        pygame.draw.rect(pantalla, color, rect)
        pygame.draw.rect(pantalla, self.COLOR_BORDE, rect, 2)  
        

        if self.esta_revelada and not self.es_mina and self.minas_adyacentes > 0:
            # Mostrar número de minas adyacentes
            fuente = pygame.font.Font(None, 36)
            color_numero = self.COLORES_NUMEROS.get(self.minas_adyacentes, self.COLOR_TEXTO)
            texto = fuente.render(str(self.minas_adyacentes), True, color_numero)
            texto_rect = texto.get_rect(center=rect.center)
            pantalla.blit(texto, texto_rect)
        
        elif self.esta_revelada and self.es_mina:
            centro = rect.center
            pygame.draw.circle(pantalla, (0, 0, 0), centro, self.tamaño // 4)
        
        elif self.tiene_bandera and not self.esta_revelada:
            centro_x, centro_y = rect.center
            puntos = [
                (centro_x - self.tamaño // 4, centro_y - self.tamaño // 4),
                (centro_x + self.tamaño // 4, centro_y),
                (centro_x - self.tamaño // 4, centro_y + self.tamaño // 4)
            ]
            pygame.draw.polygon(pantalla, self.COLOR_BANDERA, puntos)
    
    def contiene_punto(self, x, y, posicion_y_tablero=0):
        # Verifica si el mouse está dentro de esta celda.
        celda_x = self.columna * self.tamaño
        celda_y = self.fila * self.tamaño + posicion_y_tablero
        
        return (celda_x <= x < celda_x + self.tamaño and 
                celda_y <= y < celda_y + self.tamaño)
    
    def alternar_bandera(self):
        # Coloca o quita una bandera en la celda (solo si no está revelada).
        if not self.esta_revelada:
            self.tiene_bandera = not self.tiene_bandera
    
    def revelar(self):
        # Revela la celda (si no tiene bandera).
        if not self.tiene_bandera and not self.esta_revelada:
            self.esta_revelada = True
            return True
        return False
