
import random
from celda import Celda


class Tablero:
   
    
    def __init__(self, filas, columnas, tamaño_celda, numero_minas):
        
        # Inicializa el tablero del juego.

        self.filas = filas
        self.columnas = columnas
        self.tamaño_celda = tamaño_celda
        self.numero_minas = numero_minas
        
        # Estados del juego
        self.juego_terminado = False
        self.victoria = False
        self.primera_jugada = True 
        
        
        self.celdas = []
        for fila in range(filas):
            fila_celdas = []
            for columna in range(columnas):
                celda = Celda(fila, columna, tamaño_celda)
                fila_celdas.append(celda)
            self.celdas.append(fila_celdas)
    
    def inicializar_minas(self, fila_segura, columna_segura):
        # Coloca las minas aleatoriamente en el tablero.
        # Evita colocar una mina en la celda del primer click y sus vecinas.
    
    
        posiciones_seguras = set()
        for df in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                f, c = fila_segura + df, columna_segura + dc
                if 0 <= f < self.filas and 0 <= c < self.columnas:
                    posiciones_seguras.add((f, c))
        
        posiciones_disponibles = []
        for f in range(self.filas):
            for c in range(self.columnas):
                if (f, c) not in posiciones_seguras:
                    posiciones_disponibles.append((f, c))
        
        posiciones_minas = random.sample(posiciones_disponibles, 
                                        min(self.numero_minas, len(posiciones_disponibles)))
        
        # Colocar las minas
        for fila, columna in posiciones_minas:
            self.celdas[fila][columna].es_mina = True
        
        # Calcular números de minas adyacentes para todas las celdas
        self._calcular_numeros()
    
    def _calcular_numeros(self):
    
        # Calcula el número de minas adyacentes para cada celda.

        for fila in range(self.filas):
            for columna in range(self.columnas):
                if not self.celdas[fila][columna].es_mina:
                    contador = 0
                    for df in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if df == 0 and dc == 0:
                                continue
                            
                            f_vecina = fila + df
                            c_vecina = columna + dc
                            
                            if (0 <= f_vecina < self.filas and 
                                0 <= c_vecina < self.columnas):
                                if self.celdas[f_vecina][c_vecina].es_mina:
                                    contador += 1
                    
                    self.celdas[fila][columna].minas_adyacentes = contador
    
    def obtener_celda_en_posicion(self, x, y, posicion_y_tablero=0):
        #  Obtiene la celda que se hizo click.
        for fila in self.celdas:
            for celda in fila:
                if celda.contiene_punto(x, y, posicion_y_tablero):
                    return celda
        return None
    
    def revelar_celda(self, celda):
        
        if self.juego_terminado or celda.esta_revelada or celda.tiene_bandera:
            return
        
        # Si es la primera jugada, inicializar minas evitando esta celda
        if self.primera_jugada:
            self.inicializar_minas(celda.fila, celda.columna)
            self.primera_jugada = False
        
        
        celda.revelar()
        
        if celda.es_mina:
            self.juego_terminado = True
            self.victoria = False
            self._revelar_todas_las_minas()
            return
        
        # Si la celda no tiene minas adyacentes, descubre las celdas vecinas.
        if celda.minas_adyacentes == 0:
            self._expandir_celdas_vacias(celda.fila, celda.columna)
        
        self._verificar_victoria()
    
    def _expandir_celdas_vacias(self, fila, columna):
        # Expande automáticamente revelando celdas vecinas cuando se revela una celda vacía.
        
        cola = [(fila, columna)]
        visitadas = set()
        visitadas.add((fila, columna))
        
        while cola:
            f_actual, c_actual = cola.pop(0)
            
            for df in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if df == 0 and dc == 0:
                        continue
                    
                    f_vecina = f_actual + df
                    c_vecina = c_actual + dc
                    
                    # Verificar límites y si ya fue visitada
                    if (0 <= f_vecina < self.filas and 
                        0 <= c_vecina < self.columnas and
                        (f_vecina, c_vecina) not in visitadas):
                        
                        visitadas.add((f_vecina, c_vecina))
                        celda_vecina = self.celdas[f_vecina][c_vecina]
                        
                        if not celda_vecina.es_mina and not celda_vecina.tiene_bandera:
                            celda_vecina.revelar()
                            
                            # Si también está vacía, agregar a la cola para expandir
                            if celda_vecina.minas_adyacentes == 0:
                                cola.append((f_vecina, c_vecina))
    
    def _revelar_todas_las_minas(self):
        
        #Revela todas las minas del tablero.
        #Se ejecuta cuando el jugador pierde.
        
        for fila in self.celdas:
            for celda in fila:
                if celda.es_mina:
                    celda.esta_revelada = True
    
    def _verificar_victoria(self):
       
       # Verifica si el jugador ganó el juego.

        for fila in self.celdas:
            for celda in fila:
                # Si hay una celda sin mina que no está revelada, el juego continúa
                if not celda.es_mina and not celda.esta_revelada:
                    return
        
        # Si llegamos aquí, todas las celdas sin mina están reveladas
        self.juego_terminado = True
        self.victoria = True
    
    def alternar_bandera(self, celda):

        # Coloca o quita una bandera en una celda (click derecho).
        
        if not self.juego_terminado:
            celda.alternar_bandera()
    
    def obtener_banderas_colocadas(self, numero_minas):
    
        # Cuenta cuántas banderas ha colocado el jugador.
        contador = 0
        for fila in self.celdas:
            for celda in fila:
                if celda.tiene_bandera:
                    contador += 1
        
        return min(contador, numero_minas)
    
    def reiniciar(self):
        # Reinicia el tablero para una nueva partida.
        self.juego_terminado = False
        self.victoria = False
        self.primera_jugada = True
        
        self.celdas = []
        for fila in range(self.filas):
            fila_celdas = []
            for columna in range(self.columnas):
                celda = Celda(fila, columna, self.tamaño_celda)
                fila_celdas.append(celda)
            self.celdas.append(fila_celdas)
    
    def dibujar(self, pantalla, posicion_y_tablero=0):
        
        for fila in self.celdas:
            for celda in fila:
                celda.dibujar(pantalla, posicion_y_tablero)
