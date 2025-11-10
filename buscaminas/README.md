# Buscaminas con Pygame

Juego completo de Buscaminas implementado en Python con pygame.

## Descripción del Proyecto

Este es un juego de Buscaminas clásico con interfaz gráfica completa que incluye:
- Tablero de 10×10 celdas con 15 minas
- Click izquierdo para revelar celdas
- Click derecho para colocar/quitar banderas
- Expansión automática de celdas vacías
- Contador de tiempo
- Contador de minas restantes
- Botón de reinicio
- Mensajes de victoria y derrota

## Cómo Jugar

# Controles
- **Click izquierdo**: Revela una celda
- **Click derecho**: Coloca o quita una bandera (para marcar donde crees que hay una mina)
- **Botón "Reiniciar"**: Comienza un nuevo juego

### Objetivo
Revelar todas las celdas que **NO** contienen minas, sin clickear en ninguna mina.

### Reglas
1. Los números indican cuántas minas hay en las 8 celdas adyacentes
2. Si revelas una celda vacía (sin minas adyacentes), se expanden automáticamente las celdas vecinas
3. Usa banderas para marcar celdas donde crees que hay minas
4. Ganas cuando revelas todas las celdas sin mina
5. Pierdes si revelas una celda con mina

## Estructura del Proyecto

```
buscaminas/
├── src/
│   ├── main.py      # Archivo principal con el loop del juego
│   ├── cell.py      # Clase Celda
│   ├── grid.py      # Clase Tablero
│   └── ui.py        # Clase InterfazUsuario
└── README.md        # Este archivo
```

## Explicación de Módulos y Funciones

### 1. `cell.py` - Módulo Celda

**Clase: `Celda`**
Representa una celda individual del tablero.

#### Propiedades principales:
- `fila`, `columna`: Posición en el tablero (0-9)
- `tamaño`: Tamaño en píxeles (45px)
- `es_mina`: Boolean que indica si contiene una mina
- `esta_revelada`: Boolean que indica si el jugador la destapó
- `tiene_bandera`: Boolean que indica si tiene una bandera
- `minas_adyacentes`: Número de minas en las 8 celdas vecinas (0-8)

#### Métodos principales:

**`__init__(self, fila, columna, tamaño)`**
- Inicializa una celda con su posición y tamaño
- Establece todos los estados en False y minas_adyacentes en 0
- Define los colores para cada estado visual

**`dibujar(self, pantalla, posicion_y_tablero=0)`**
- Dibuja la celda en la pantalla según su estado
- Si está revelada y tiene número, muestra el número con color específico
- Si está revelada y es mina, dibuja un círculo negro
- Si tiene bandera, dibuja un triángulo amarillo
- Si no está revelada, muestra color gris oscuro

**`contiene_punto(self, x, y, posicion_y_tablero=0)`**
- Verifica si un click del mouse cayó dentro de esta celda
- Retorna True si el punto (x, y) está dentro de los límites de la celda

**`alternar_bandera(self)`**
- Cambia el estado de la bandera (on/off)
- Solo funciona si la celda no está revelada

**`revelar(self)`**
- Marca la celda como revelada
- Retorna True si se reveló exitosamente, False si tiene bandera

---

### 2. `grid.py` - Módulo Tablero

**Clase: `Tablero`**
Gestiona todo el tablero del juego y la lógica principal.

#### Propiedades principales:
- `filas`, `columnas`: Dimensiones del tablero (10×10)
- `tamaño_celda`: Tamaño de cada celda en píxeles
- `numero_minas`: Cantidad de minas (15)
- `celdas`: Matriz 2D con objetos Celda
- `juego_terminado`: Boolean del estado del juego
- `victoria`: Boolean que indica si ganó
- `primera_jugada`: Boolean para generar minas después del primer click

#### Métodos principales:

**`__init__(self, filas, columnas, tamaño_celda, numero_minas)`**
- Crea la matriz de celdas vacías (sin minas aún)
- Inicializa los estados del juego

**`inicializar_minas(self, fila_segura, columna_segura)`**
- Coloca las minas aleatoriamente en el tablero
- **Importante**: Evita colocar mina en la primera celda clickeada y sus vecinas
- Esto garantiza que el primer click nunca sea una mina
- Después de colocar minas, calcula los números

**`_calcular_numeros(self)`**
- Recorre todas las celdas del tablero
- Para cada celda sin mina, cuenta cuántas minas hay en las 8 celdas vecinas
- Asigna ese número a `minas_adyacentes`

**`revelar_celda(self, celda)`**
- Lógica principal del juego al clickear una celda
- Si es la primera jugada, inicializa las minas evitando esa celda
- Revela la celda
- Si es mina: termina el juego (derrota) y revela todas las minas
- Si tiene 0 minas adyacentes: expande automáticamente
- Verifica si el jugador ganó

**`_expandir_celdas_vacias(self, fila, columna)`**
- Algoritmo de búsqueda en amplitud (BFS)
- Cuando revelas una celda con 0 minas adyacentes, automáticamente revela las vecinas
- Si una vecina también tiene 0, sigue expandiendo recursivamente
- Se detiene al encontrar celdas con números o bordes del tablero

**`_revelar_todas_las_minas(self)`**
- Se ejecuta cuando pierdes
- Revela todas las minas del tablero para que veas dónde estaban

**`_verificar_victoria(self)`**
- Recorre todas las celdas
- Si todas las celdas sin mina están reveladas, el jugador ganó
- Marca `victoria = True` y `juego_terminado = True`

**`alternar_bandera(self, celda)`**
- Llama al método de la celda para colocar/quitar bandera
- Solo funciona si el juego no ha terminado

**`obtener_banderas_colocadas(self)`**
- Cuenta cuántas banderas colocó el jugador
- Se usa para mostrar "minas restantes" en la UI

**`reiniciar(self)`**
- Reinicia todos los estados del juego
- Crea un tablero completamente nuevo sin minas

**`dibujar(self, pantalla, posicion_y_tablero=0)`**
- Dibuja todas las celdas del tablero
- Llama al método `dibujar` de cada celda

**`obtener_celda_en_posicion(self, x, y, posicion_y_tablero=0)`**
- Encuentra qué celda fue clickeada según las coordenadas del mouse
- Retorna la celda o None si el click fue fuera del tablero

---

### 3. `ui.py` - Módulo Interfaz de Usuario

**Clase: `InterfazUsuario`**
Gestiona todos los elementos visuales de la interfaz.

#### Propiedades principales:
- `ancho_pantalla`: Ancho de la ventana
- `alto_panel`: Altura del panel superior (120px)
- `boton_rect`: Rectángulo del botón de reinicio
- `tiempo_inicio`: Momento en que empezó el juego
- `tiempo_pausado`: Tiempo cuando el juego terminó

#### Métodos principales:

**`__init__(self, ancho_pantalla, alto_panel_superior=120)`**
- Inicializa la interfaz
- Define colores y fuentes
- Crea el rectángulo del botón de reinicio centrado

**`iniciar_cronometro(self)`**
- Guarda el tiempo actual (en milisegundos)
- Se llama cuando el jugador hace el primer click

**`pausar_cronometro(self)`**
- Guarda el tiempo transcurrido cuando el juego termina
- Evita que el cronómetro siga corriendo después de ganar/perder

**`obtener_tiempo_transcurrido(self)`**
- Calcula los segundos desde que comenzó el juego
- Si el juego terminó, retorna el tiempo pausado
- Si está en curso, calcula la diferencia con el tiempo actual

**`reiniciar_cronometro(self)`**
- Pone el cronómetro a cero
- Se llama al reiniciar el juego

**`dibujar_panel_superior(self, pantalla, numero_minas, banderas_colocadas, juego_terminado, victoria)`**
- Dibuja el panel superior completo:
  - Fondo gris oscuro
  - Botón de reinicio (con efecto hover)
  - Contador de minas restantes (izquierda)
  - Cronómetro (derecha)
  - Mensaje de victoria o derrota (si terminó)

**`_dibujar_boton_reinicio(self, pantalla)`**
- Dibuja el botón "Reiniciar"
- Cambia de color cuando el mouse está encima (hover)

**`_dibujar_mensaje_victoria(self, pantalla, tiempo)`**
- Dibuja overlay semi-transparente
- Muestra "¡VICTORIA! " en verde
- Muestra el tiempo que tardaste

**`_dibujar_mensaje_derrota(self, pantalla)`**
- Dibuja overlay semi-transparente
- Muestra "¡BOOM! Has perdido" en rojo

**`boton_reinicio_clickeado(self, x, y)`**
- Verifica si el click del mouse fue dentro del botón de reinicio
- Retorna True/False

**`obtener_altura_panel(self)`**
- Retorna la altura del panel superior
- Se usa para calcular posiciones del tablero

---

### 4. main.py - Archivo Principal

**Función: main() 
Loop principal del juego que orquesta todo.

#### Estructura del loop:

**1. Inicialización**
```python
pygame.init()
```
- Inicializa todos los módulos de pygame

**2. Configuración**
```python
FILAS = 10
COLUMNAS = 10
TAMAÑO_CELDA = 45
NUMERO_MINAS = 15
```
- Define el tamaño del tablero y número de minas

**3. Creación de objetos**
```python
tablero = Tablero(FILAS, COLUMNAS, TAMAÑO_CELDA, NUMERO_MINAS)
interfaz = InterfazUsuario(ANCHO_VENTANA, ALTO_PANEL_SUPERIOR)
```
- Crea instancias del tablero y la interfaz

**4. Loop de eventos**
```python
while jugando:
    for evento in pygame.event.get():
```
- Procesa todos los eventos de pygame

**5. Manejo de clicks**
- **Click en botón de reinicio**: Reinicia el juego
- **Click izquierdo en celda**: Revela la celda
  - En el primer click, inicia el cronómetro
  - Si termina el juego, pausa el cronómetro
- **Click derecho en celda**: Alterna bandera

**6. Renderizado**
```
pantalla.fill(COLOR_FONDO)
interfaz.dibujar_panel_superior(...)
tablero.dibujar(...)
pygame.display.flip()
```
- Limpia la pantalla
- Dibuja el panel superior
- Dibuja el tablero
- Actualiza la pantalla

**7. Control de FPS**
```
reloj.tick(60)
```
- Limita el juego a 60 frames por segundo

---

## Lógica del Juego

### Flujo principal:

1. **Inicio del juego**
   - Se crea un tablero vacío (sin minas aún)
   - El jugador ve todas las celdas grises sin revelar

2. **Primer click**
   - Se generan 15 minas en posiciones aleatorias
   - **Nunca se coloca mina en la celda clickeada ni en sus 8 vecinas**
   - Se calculan los números de todas las celdas
   - Se revela la celda clickeada
   - Se inicia el cronómetro

3. **Expansión automática**
   - Si revelas una celda con 0 minas adyacentes, se expande automáticamente
   - Usa algoritmo BFS (búsqueda en amplitud) para revelar vecinas
   - Se detiene al encontrar celdas con números

4. **Colocar banderas**
   - Click derecho marca/desmarca celdas
   - Las banderas evitan revelar accidentalmente una celda
   - Se actualizan las "minas restantes" (minas totales - banderas colocadas)

5. **Victoria**
   - Se alcanza cuando todas las celdas sin mina están reveladas
   - No es necesario colocar banderas en todas las minas
   - Se muestra mensaje con el tiempo

6. **Derrota**
   - Ocurre al revelar una celda con mina
   - Se revelan todas las minas del tablero
   - Se muestra mensaje de derrota

7. **Reiniciar**
   - Click en botón "Reiniciar" o terminar el juego
   - Se crea un tablero completamente nuevo
   - El cronómetro se pone a cero

---

## Códigos de Colores

### Números de minas adyacentes:
- **1**: Azul
- **2**: Verde
- **3**: Rojo
- **4**: Azul oscuro
- **5**: Marrón
- **6**: Cian
- **7**: Negro
- **8**: Gris

### Estados de celdas:
- **Sin revelar**: Gris oscuro (100, 100, 100)
- **Revelada**: Gris claro (200, 200, 200)
- **Mina**: Rojo (255, 50, 50)
- **Bandera**: Triángulo amarillo (255, 255, 0)

---

## Cómo Ejecutar

### Requisitos
```bash
pip install pygame
```

### Ejecutar el juego
```bash
cd src
python main.py
```

O desde la raíz del proyecto:
```bash
python src/main.py
```

---

## Algoritmos Importantes

### 1. Generación de Minas (con zona segura)
```
1. Obtener coordenadas del primer click (fila_segura, columna_segura)
2. Crear lista de posiciones seguras: celda clickeada + 8 vecinas
3. Crear lista de posiciones disponibles: todas menos las seguras
4. Seleccionar aleatoriamente N posiciones de las disponibles
5. Marcar esas celdas como minas
```

### 2. Cálculo de Números
```
Para cada celda (fila, columna):
    Si no es mina:
        contador = 0
        Para cada vecina en las 8 direcciones:
            Si vecina es mina:
                contador += 1
        celda.minas_adyacentes = contador
```

### 3. Expansión Automática (BFS)
```
cola = [celda_inicial]
visitadas = {celda_inicial}

Mientras cola no esté vacía:
    celda_actual = cola.pop()
    
    Para cada vecina de celda_actual:
        Si vecina no visitada y no es mina y no tiene bandera:
            Marcar como visitada
            Revelar vecina
            
            Si vecina.minas_adyacentes == 0:
                Agregar vecina a la cola
```

### 4. Detección de Victoria
```
Para cada celda en el tablero:
    Si celda no es mina Y celda no está revelada:
        Retornar False  # Aún no ganó

Si retorna True,  # Ganó
```

---

## Configuración Recomendada

Para cambiar la dificultad, modifica estos valores en `main.py`:

### Fácil
```
FILAS = 8
COLUMNAS = 8
NUMERO_MINAS = 10
```

### Medio (actual)
```
FILAS = 10
COLUMNAS = 10
NUMERO_MINAS = 15
```

### Difícil
```
FILAS = 16
COLUMNAS = 16
NUMERO_MINAS = 40
```

### Experto
```
FILAS = 16
COLUMNAS = 30
NUMERO_MINAS = 99
```

**Nota**: Si cambias el tamaño del tablero, ajusta también `TAMAÑO_CELDA` para que quepa en la pantalla.

---

## Características Técnicas

- **Lenguaje**: Python 3.7+
- **Biblioteca gráfica**: Pygame 2.0+
- **Arquitectura**: Orientada a objetos
- **Patrón**: Modelo-Vista (separación de lógica y presentación)
- **Algoritmos**: BFS para expansión, generación aleatoria con zonas seguras

---


 
