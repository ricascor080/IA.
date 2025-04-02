1. Objetivo General

El propósito de este proyecto es analizar imágenes o video en tiempo real para determinar si hay presencia de vida humana (específicamente rostros), utilizando la biblioteca MediaPipe. A partir de la detección facial, se modelan puntos clave para reconocer gestos o expresiones que confirmen que se trata de una persona viva y no una imagen estática. y asi mismo una persona detectar las emociones ya que se pueda ver si esta feliz o si esta trizte y pueda ser comparado y ver las emociones 

2. Detecion de quien habla 
Aun que MediaPipe no reconoce audio pues lo que puede usar es la detecion de la boca de como se mueve ya que pues puede estra checando si la boca esta en movimiento 

+ Repitiendo las cordenadas verticales de los labios 

+ Los puntos de referencia para los labios serian 13 y 14 
 y los combinamos con el punto 152 de la mandibula 

¿Lo que se necesita ?
+ La distancia de entre los labios en varios fotogramas seguidos 
+ ver si esa distancia cambias y si es asi pues es ver el ritmo de habla
+ y como usar las tecnicas como FFT para ver si hay un patron ciclico 


3. Análisis de Gestos Faciales

A partir de los puntos clave (landmarks) es posible reconocer expresiones como:

Parpadeo	159, 145 (o.j.)
	
Sonrisa	61, 291, 13, 14 (boca)	

Boca abierta	13, 14, 17, 0

Fruncir Frío	70, 63

4. Reconocimiento de Emociones

----------------Feliz---------------------------------

+ Indicadores:
Comisuras de la boca elevadas (puntos de referencia 61 y 291)
Apertura ligera de la boca (13 y 14)
Ojos ligeramente más cerrados (159-145)

+ Puntos de referencia usados:

61, 291→ comisuras de los labios
13, 14→ centro del labio superior e inferior
159, 145→ párpado superior e inferior (ojo izq.)

-----------------Trizte ------------------------

+ Indicadores:
 
Comisuras caídas (61 y 291)
Labios hacia abajo, sin curvatura
Cejas bajas y ligeramente inclinadas al centro (70, 105)

+ Puntos de referencia usados:

61, 291→ comisuras
70, 63, 105→ ceja izquierda
13, 14→ apertura de la boca (puede estar cerrada)

--------------Temor-------------------

+ Indicadores:

Ojos muy abiertos (diferencia grande entre 159-145)
Cejas levantadas (63, 105)
Boca abierta parcialmente (13 y 14)

+ Puntos de referencia usados:

159, 145, 386, 374→ ojos
13, 14→ boca
70, 63, 105→ ceja izq.
336, 296→ ceja der.



