"""
Módulo Celda (Cell)
===================
Representa una celda individual del tablero de Buscaminas.

Propiedades:
- fila, columna: posición en el tablero
- es_mina: si la celda contiene una mina
- esta_revelada: si el jugador ha destapado la celda
- tiene_bandera: si el jugador ha marcado la celda con una bandera
- minas_adyacentes: número de minas en las 8 celdas vecinas
"""

import pygame


class Celda:
    """
    Clase que representa una celda individual del tablero.
    
    Cada celda puede estar en varios estados:
    - Sin revelar (gris oscuro)
    - Revelada vacía (gris claro con número)
    - Revelada con mina (roja con bomba)
    - Con bandera (amarilla con marca)
    """
    
    def __init__(self, fila, columna, tamaño):
        """
        Inicializa una celda del tablero.
        
        Args:
            fila (int): posición vertical (0-9)
            columna (int): posición horizontal (0-9)
            tamaño (int): tamaño en píxeles de la celda (lado del cuadrado)
        """
        self.fila = fila
        self.columna = columna
        self.tamaño = tamaño
        
        # Estados de la celda
        self.es_mina = False
        self.esta_revelada = False
        self.tiene_bandera = False
        self.minas_adyacentes = 0
        
        # Colores para dibujar
        self.COLOR_SIN_REVELAR = (100, 100, 100)  # Gris oscuro
        self.COLOR_REVELADA = (200, 200, 200)     # Gris claro
        self.COLOR_MINA = (255, 50, 50)           # Rojo
        self.COLOR_BANDERA = (255, 255, 0)        # Amarillo
        self.COLOR_BORDE = (255, 255, 255)        # Blanco
        self.COLOR_TEXTO = (0, 0, 0)              # Negro
        
        # Colores para números según cantidad de minas adyacentes
        self.COLORES_NUMEROS = {
            1: (0, 0, 255),      # Azul
            2: (0, 128, 0),      # Verde
            3: (255, 0, 0),      # Rojo
            4: (0, 0, 128),      # Azul oscuro
            5: (128, 0, 0),      # Marrón
            6: (0, 128, 128),    # Cian
            7: (0, 0, 0),        # Negro
            8: (128, 128, 128),  # Gris
        }
    
    def dibujar(self, pantalla, posicion_y_tablero=0):
        """
        Dibuja la celda en la pantalla según su estado.
        
        Args:
            pantalla: superficie de pygame donde dibujar
            posicion_y_tablero (int): desplazamiento vertical del tablero en píxeles
        """
        # Calcular posición en píxeles
        x = self.columna * self.tamaño
        y = self.fila * self.tamaño + posicion_y_tablero
        
        # Rectángulo de la celda
        rect = pygame.Rect(x, y, self.tamaño, self.tamaño)
        
        # Determinar color de fondo según estado
        if self.esta_revelada:
            if self.es_mina:
                color = self.COLOR_MINA
            else:
                color = self.COLOR_REVELADA
        else:
            color = self.COLOR_SIN_REVELAR
        
        # Dibujar celda
        pygame.draw.rect(pantalla, color, rect)
        pygame.draw.rect(pantalla, self.COLOR_BORDE, rect, 2)  # Borde
        
        # Dibujar contenido según estado
        if self.esta_revelada and not self.es_mina and self.minas_adyacentes > 0:
            # Mostrar número de minas adyacentes
            fuente = pygame.font.Font(None, 36)
            color_numero = self.COLORES_NUMEROS.get(self.minas_adyacentes, self.COLOR_TEXTO)
            texto = fuente.render(str(self.minas_adyacentes), True, color_numero)
            texto_rect = texto.get_rect(center=rect.center)
            pantalla.blit(texto, texto_rect)
        
        elif self.esta_revelada and self.es_mina:
            # Dibujar mina (círculo negro)
            centro = rect.center
            pygame.draw.circle(pantalla, (0, 0, 0), centro, self.tamaño // 4)
        
        elif self.tiene_bandera and not self.esta_revelada:
            # Dibujar bandera (triángulo amarillo)
            centro_x, centro_y = rect.center
            puntos = [
                (centro_x - self.tamaño // 4, centro_y - self.tamaño // 4),
                (centro_x + self.tamaño // 4, centro_y),
                (centro_x - self.tamaño // 4, centro_y + self.tamaño // 4)
            ]
            pygame.draw.polygon(pantalla, self.COLOR_BANDERA, puntos)
    
    def contiene_punto(self, x, y, posicion_y_tablero=0):
        """
        Verifica si un punto (click del mouse) está dentro de esta celda.
        
        Args:
            x (int): coordenada x del click
            y (int): coordenada y del click
            posicion_y_tablero (int): desplazamiento vertical del tablero
            
        Returns:
            bool: True si el punto está dentro de la celda
        """
        celda_x = self.columna * self.tamaño
        celda_y = self.fila * self.tamaño + posicion_y_tablero
        
        return (celda_x <= x < celda_x + self.tamaño and 
                celda_y <= y < celda_y + self.tamaño)
    
    def alternar_bandera(self):
        """
        Coloca o quita una bandera en la celda (solo si no está revelada).
        """
        if not self.esta_revelada:
            self.tiene_bandera = not self.tiene_bandera
    
    def revelar(self):
        """
        Revela la celda (la destapa para mostrar su contenido).
        Solo se puede revelar si no tiene bandera.
        
        Returns:
            bool: True si se reveló exitosamente, False si tiene bandera o ya estaba revelada
        """
        if not self.tiene_bandera and not self.esta_revelada:
            self.esta_revelada = True
            return True
        return False
