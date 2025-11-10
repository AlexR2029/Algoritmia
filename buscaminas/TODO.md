# Proyecto Buscaminas - Completado

## Estado del Proyecto
**Estado**: COMPLETADO Y FUNCIONANDO

## Archivos Creados

### Módulos del Juego (src/)
-  `cell.py` - Clase Celda (representa cada casilla individual)
-  `grid.py` - Clase Tablero (gestiona la lógica del juego)
-  `ui.py` - Clase InterfazUsuario (panel superior, botones, mensajes)
-  `main.py` - Loop principal del juego

### Documentación
-  `README.md` - Documentación completa con explicación de cada función

## 🎯 Características Implementadas

### Lógica del Juego
-  Generación aleatoria de minas (evita primer click)
-  Cálculo de números de minas adyacentes
-  Expansión automática de celdas vacías (algoritmo BFS)
-  Detección de victoria (todas las celdas sin mina reveladas)
-  Detección de derrota (click en mina)
-  Sistema de banderas (click derecho)
-  Reinicio de juego

### Interfaz Gráfica
-  Panel superior con información
-  Botón de reinicio con efecto hover
-  Contador de minas restantes
-  Cronómetro del juego
-  Mensajes de victoria/derrota con overlay
-  Colores diferenciados para números (1-8)
-  Símbolos visuales (banderas, minas)

### Controles
-  Click izquierdo: revelar celda
-  Click derecho: colocar/quitar bandera
-  Botón reiniciar: nuevo juego

##  Configuración Actual
- Tablero: 10×10 celdas
- Minas: 15
- Tamaño de celda: 45 píxeles
- Ventana: 450×570 píxeles

##  Nombres en Español
Todas las variables, clases, funciones y comentarios están en español:
- `Celda` (en lugar de Cell)
- `Tablero` (en lugar de Grid)
- `InterfazUsuario` (en lugar de UI)
- `es_mina`, `esta_revelada`, `tiene_bandera`
- `fila`, `columna`, `tamaño_celda`
- `juego_terminado`, `victoria`
- etc.

##  Cómo Ejecutar
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el juego
cd src
python main.py
```

##  Documentación
Ver `README.md` para:
- Explicación detallada de cada módulo
- Descripción de todas las funciones
- Algoritmos implementados (BFS, generación de minas, etc.)
- Códigos de colores
- Configuración de dificultad

##  Estructura del Código
```
Celda (cell.py)
├── Propiedades: fila, columna, es_mina, esta_revelada, etc.
├── dibujar() - Renderiza la celda según su estado
├── revelar() - Marca como revelada
├── alternar_bandera() - Coloca/quita bandera
└── contiene_punto() - Detecta clicks

Tablero (grid.py)
├── Propiedades: celdas[][], juego_terminado, victoria
├── inicializar_minas() - Genera minas evitando primer click
├── _calcular_numeros() - Calcula números adyacentes
├── revelar_celda() - Lógica principal del juego
├── _expandir_celdas_vacias() - Algoritmo BFS
├── _verificar_victoria() - Detecta si ganó
├── alternar_bandera() - Marca celdas
└── reiniciar() - Nuevo juego

InterfazUsuario (ui.py)
├── Propiedades: tiempo_inicio, boton_rect
├── dibujar_panel_superior() - Panel con info
├── iniciar_cronometro() - Empieza tiempo
├── pausar_cronometro() - Detiene al terminar
├── _dibujar_mensaje_victoria() - Overlay de victoria
└── _dibujar_mensaje_derrota() - Overlay de derrota

main.py
└── main() - Loop principal con eventos y renderizado
```

##  Características Especiales
1. **Primer click seguro**: Nunca genera minas en el primer click ni sus vecinas
2. **Expansión inteligente**: Usa BFS para revelar áreas vacías automáticamente
3. **Interfaz completa**: Panel de información, cronómetro, contador de minas
4. **Mensajes visuales**: Overlays semi-transparentes para victoria/derrota
5. **Código documentado**: Docstrings en español para cada función

##  Conceptos de Programación Aplicados
- Programación Orientada a Objetos (POO)
- Separación de responsabilidades (Modelo-Vista)
- Algoritmos de búsqueda (BFS)
- Manejo de eventos (pygame)
- Matrices 2D (tablero de celdas)
- Estados del juego (jugando, ganó, perdió)

---

**Proyecto completado**: El juego está 100% funcional y listo para jugar! 
