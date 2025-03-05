# IA.
Ejercio uno red neuronal 

Modelar una red neuronal que pueda jugar al 5 en lineas sin garvedad  en un tablero de 20 * 20 

1. Definir el tipo de red neuronal y sus partes:
para este ejercicio se usara una red neuronal comvulocional ya que pues se parece mucho a una imagen el tablero de 20*20 , tambien pues busca de mejor manera patrones 
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

5.
