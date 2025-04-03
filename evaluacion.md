Nombre : Ricardo Cornejo Cervantes  Cal:           

Modelar una red neuronal que pueda identificar emociones a traves de los valores obtenidos de los landmarks que genera mediapipe

- Definir el tipo de red neuronal y describe cada una de sus partes 

Seria una red neuronal multicapa ya que se necesita que en una cap se reciban los datos de entrada que en su caso serian los puntos caracteristicos o las landmarks y depues en la siguinete cpa seguir con las opreaciones para poder determinar la emocion que es y asi en la ultima cpa poder entregra en la ultima capa de salida la emocion a la que se tiene 

- Definir los patrones a utilizar 

Estos serian los patrones que serian los puntos en el rostro que son las landmarks o los puntos especificos para poder tener patrones 

- Definir el numero de funcion de activacion que es necesaria para este problema 

Usamos:

ReLU en las capas ocultas: ya que es una de las ulilizadas con numeros positivos y es la mas comun es este aspecto que consideor que es la mejor para poder resolver este problema 

Softmax en la salida: pues para la salida ya que es comunmente usada en la capa final o la de salida 

En total: una función por capa .

- Definir el numero maximo de entradas 

468 son las landmarks o puntos caracteristicos 
Serian si usamos [x,y , z]son 3 esto serian 468 X 3 = 1,404
entradas 

- ¿Que valores a la salida de la red se podrian esperar?

pues tendria que esperar un vector donde la salida pues es un aproximando a una emocion y pues al momento de la que tenga mas valor la eligiria y esa seria la salida de la red neuronal 

- ¿Cuales son los valores maximos que puede tener el bias?

Estos pueden ser algunos de lo valore y no tiene un numero fijo maximo puede tomar numeros positivos o negativos como lo necesite aprender 