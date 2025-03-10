# IA.
Ejercio uno red neuronal 

Modelar una red neuronal que pueda jugar al 5 en lineas sin garvedad  en un tablero de 20 * 20 

1. Definir el tipo de red neuronal y sus partes:
para este ejercicio se usara una red neuronal comvulocional ya que pues se parece mucho a una
imagen el tablero de 20*20 , tambien pues busca de mejor manera patrones 
1.1 Cada una de sus partes :
- Los datos de entrada 
- Capas convulucionales 
- Capas densas 
- Capa de salida 
- Optimizacion y aprendisaje 

2.Define los patrones a utilizar 
- patrones de Victoria 
- patrones de Bloqueo 
- patrones de Estrategia 
- patrones de control de los espacios vacios 

3. Definir la funcion de activiacion para este problemas
- Capas convulucionales y ocultas : ya que quiero que el juego pueda elegir una jugada detectando los espacios vacios 
- Softmax : tambien ya que daria elegir un movimeinto de los 400 que tiene 

4. Define le numero maximo de entradas 
- 1 es la ficha del jugador actual 
- (-1) es la ficha del oponente 
- 0 representa una casilla vacia 

y son 400 casos en el tablero las entradas quedarian de la siguiente manera 
[-1,0-1,....1,0,-1]

5.¿ Que valores de salida se podrian esperar de la red ?
Descripción:
La red predice directamente la mejor casilla para jugar.
Se usan dos neuronas en la salida
Una para la coordenada X (fila en el tablero).
Otra para la coordenada Y (columna en el tablero).

 Valores esperados

Salida esperada:
(x, y), donde x, y ∈ [0, 19] (porque el tablero es de 20x20).

Ejemplo de salida:
(12, 5) significa que la IA jugará en la fila 12, columna 5.

6. ¿ Cuales son los valores maximo que puede tener el bias ?

El bias en una red neuronal es un término que permite a la red ajustar 
sus activaciones y manejar entradas que sean cero. Su valor máximo depende de tres factores

Si la red usa ReLU (Rectified Linear Unit), el bias teóricamente no tiene un límite máximo, pero 
en la práctica valores superiores a 5 pueden provocar gradientes explosivos y dificultar el entrenamiento.

Si la red usa Softmax, los valores del bias generalmente deben estar en el rango de -10 a 10. Un 
bias mayor podría hacer que una casilla del tablero tenga una probabilidad dominante, mientras 
que un bias demasiado pequeño haría que todas las casillas tengan probabilidades similares, 
dificultando la toma de decisiones.
