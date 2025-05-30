import pygame
import random
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier

pygame.init()






w, h = 800, 400
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego ML - Esquivar y Retornar")






BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)





salto = False
salto_altura = 15
gravedad = 1
en_suelo = True
menu_activo = True
modo_auto = False
modo_modelo = None




datos_salto = []          
datos_movimiento = []      


modelo_salto_arbol = None
modelo_movimiento_arbol = None
modelo_salto_nn = None
modelo_movimiento_nn = None
modelo_salto_knn = None
modelo_movimiento_knn = None


accion_actual = 0           
tiempo_accion = 0           
UMBRAL_TIEMPO = 10         
UMBRAL_PELIGRO = 50         


POSICION_ORIGEN = 50                                   
jugador = pygame.Rect(POSICION_ORIGEN, h - 100, 32, 48)  
bala_horizontal = pygame.Rect(w - 50, h - 90, 16, 16)  
bala_vertical = pygame.Rect(30 + 24, 60, 16, 16)       
nave_superior = pygame.Rect(30, 20, 64, 64)               
nave = pygame.Rect(w - 100, h - 100, 64, 64)              

# Velocidades de las balas
velocidad_bala = -6
velocidad_bala_vertical = 6
bala_disparada = False

current_frame = 0
frame_speed = 10
frame_count = 0

fondo_x1 = 0
fondo_x2 = w


fuente = pygame.font.SysFont('Arial', 24)


jugador_frames = [
    pygame.image.load('assets\\sprites\\mono_frame_1.png'),
    pygame.image.load('assets\\sprites\\mono_frame_2.png'),
    pygame.image.load('assets\\sprites\\mono_frame_3.png'),
    pygame.image.load('assets\\sprites\\mono_frame_4.png')
]
bala_img = pygame.image.load('assets\\sprites\\purple_ball.png')
fondo_img = pygame.image.load('assets\\game\\fondo2.png')
nave_img = pygame.image.load('assets\\game\\ufo.png')
fondo_img = pygame.transform.scale(fondo_img, (w, h))

# --- --------------FUNCIONES DE JUEGO------------------------- ---

def disparar_bala_horizontal():
    """Dispara la bala horizontal con velocidad aleatoria si no está disparada."""
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-8, -4)
        bala_disparada = True

def reset_bala_horizontal():
    """Reubica la bala horizontal a la posición inicial y marca que no está disparada."""
    global bala_disparada
    bala_horizontal.x = w - 50
    bala_disparada = False

def reset_bala_vertical():
    """Reubica la bala vertical justo debajo de la nave superior."""
    bala_vertical.x = 30 + 24
    bala_vertical.y = nave_superior.bottom

def manejar_salto():
    """Controla el salto del jugador, aplicando gravedad.
    Si la bala vertical se encuentra justo debajo y cerca en X,
    se añade un desplazamiento hacia adelante para evitarla."""
    global salto, salto_altura, en_suelo
    if salto:
        
        jugador.y -= salto_altura
        
        # Si la bala vertical está debajo y cerca en X, mover hacia adelante
        if bala_vertical.y > jugador.y + jugador.height and abs(bala_vertical.x - jugador.x) < 50:
            jugador.x += 5  # Ajusta el valor según convenga
        
        salto_altura -= gravedad
        if jugador.y >= h - 100:
            jugador.y = h - 100
            salto = False
            salto_altura = 15
            en_suelo = True

def entrenar_modelos():
    """Entrena todos los modelos disponibles con los datos actuales de salto y movimiento."""
    global modelo_salto_arbol, modelo_movimiento_arbol
    global modelo_salto_nn, modelo_movimiento_nn
    global modelo_salto_knn, modelo_movimiento_knn

    # Entrenar modelos para salto si hay datos
    if datos_salto:
        X = [(v, d) for v, d, s in datos_salto]
        y = [s for v, d, s in datos_salto]
        modelo_salto_arbol = DecisionTreeClassifier().fit(X, y)
        modelo_salto_nn = MLPClassifier(max_iter=500).fit(X, y)
        modelo_salto_knn = KNeighborsClassifier(n_neighbors=3).fit(X, y)
        print(f"saltos entrenados con {len(X)} datos.")
    else:
        modelo_salto_arbol = None
        modelo_salto_nn = None
        modelo_salto_knn = None

    # Entrenar modelos para movimiento si hay datos
    if datos_movimiento:
        X_mov = [[dx, jug_x, bala_x] for (dx, jug_x, bala_x), accion in datos_movimiento]
        y_mov = [accion for (_, _, _), accion in datos_movimiento]
        modelo_movimiento_arbol = DecisionTreeClassifier().fit(X_mov, y_mov)
        modelo_movimiento_nn = MLPClassifier(max_iter=500).fit(X_mov, y_mov)
        modelo_movimiento_knn = KNeighborsClassifier(n_neighbors=3).fit(X_mov, y_mov)
        print(f"movimientos derecha o izquierda entrenados con {len(X_mov)} datos.")
    else:
        modelo_movimiento_arbol = None
        modelo_movimiento_nn = None
        modelo_movimiento_knn = None

def prediccion_salto():
    """Devuelve True o False si el modelo predice que debe saltar."""
    if modo_modelo == 'arbol' and modelo_salto_arbol:
        dx = abs(jugador.x - bala_horizontal.x)
        return modelo_salto_arbol.predict([(velocidad_bala, dx)])[0] == 1
    elif modo_modelo == 'nn' and modelo_salto_nn:
        dx = abs(jugador.x - bala_horizontal.x)
        return modelo_salto_nn.predict([(velocidad_bala, dx)])[0] == 1
    elif modo_modelo == 'knn' and modelo_salto_knn:
        dx = abs(jugador.x - bala_horizontal.x)
        return modelo_salto_knn.predict([(velocidad_bala, dx)])[0] == 1
    return False

def prediccion_movimiento():
    """Devuelve la acción de movimiento predicha por el modelo (0,1,2)."""
    if modo_modelo == 'arbol' and modelo_movimiento_arbol:
        dx = abs(jugador.x - bala_vertical.x)
        return modelo_movimiento_arbol.predict([[dx, jugador.x, bala_vertical.x]])[0]
    elif modo_modelo == 'nn' and modelo_movimiento_nn:
        dx = abs(jugador.x - bala_vertical.x)
        return modelo_movimiento_nn.predict([[dx, jugador.x, bala_vertical.x]])[0]
    elif modo_modelo == 'knn' and modelo_movimiento_knn:
        dx = abs(jugador.x - bala_vertical.x)
        return modelo_movimiento_knn.predict([[dx, jugador.x, bala_vertical.x]])[0]
    return 0

def guardar_datos_salto():
    """Guarda el dato actual de salto para entrenamiento futuro."""
    dx = abs(jugador.x - bala_horizontal.x)
    salto_hecho = 1 if salto else 0
    datos_salto.append((velocidad_bala, dx, salto_hecho))

def guardar_datos_movimiento(accion):
    """Guarda el dato actual de movimiento para entrenamiento futuro."""
    dx = abs(jugador.x - bala_vertical.x)
    datos_movimiento.append(((dx, jugador.x, bala_vertical.x), accion))
def mostrar_menu():
    """Muestra el menú con cada opción en una línea separada y espera la selección del usuario."""
    global menu_activo, modo_auto, modo_modelo
    pantalla.fill(NEGRO)

    opciones = [
        "Presiona M: Manual",
        "A: Árbol",
        "N: Red Neuronal",
        "K: KNN",
        "Q: Salir"
    ]

    # Calcular posición vertical para centrar el menú
    y_offset = h // 2 - (len(opciones) * 30) // 2

    for opcion in opciones:
        texto = fuente.render(opcion, True, BLANCO)
        pantalla.blit(texto, (w // 8, y_offset))
        y_offset += 30  # Ajusta el espacio entre líneas
    
    pygame.display.flip()

    while menu_activo:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_m:
                    modo_auto = False
                    modo_modelo = None
                    # Reiniciar datos para nuevo entrenamiento
                    datos_salto.clear()
                    datos_movimiento.clear()
                    menu_activo = False
                    print("Modo manual y datos de entrenamiento borrados.")
                elif e.key == pygame.K_a:
                    modo_auto = True
                    modo_modelo = 'arbol'
                    entrenar_modelos()
                    menu_activo = False
                elif e.key == pygame.K_n:
                    modo_auto = True
                    modo_modelo = 'nn'
                    entrenar_modelos()
                    menu_activo = False
                elif e.key == pygame.K_k:
                    modo_auto = True
                    modo_modelo = 'knn'
                    entrenar_modelos()
                    menu_activo = False
                elif e.key == pygame.K_q:
                    pygame.quit()
                    exit()

def reiniciar_juego():
    """Reinicia el estado del juego y muestra el menú."""
    global salto, en_suelo, bala_disparada, menu_activo, fondo_x1, fondo_x2, accion_actual, tiempo_accion
    jugador.x, jugador.y = POSICION_ORIGEN, h - 100
    reset_bala_horizontal()
    reset_bala_vertical()
    salto = False
    en_suelo = True
    bala_disparada = False
    fondo_x1 = 0
    fondo_x2 = w
    accion_actual = 0
    tiempo_accion = 0
    menu_activo = True
    mostrar_menu()

def update():
    """Actualiza todo lo visual y el estado de las balas y jugador en cada frame."""
    global current_frame, frame_count, fondo_x1, fondo_x2

   
    fondo_x1 -= 1
    fondo_x2 -= 1
    if fondo_x1 <= -w:
        fondo_x1 = w
    if fondo_x2 <= -w:
        fondo_x2 = w
    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))

  
    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0

    
    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))
    pantalla.blit(nave_img, (nave.x, nave.y))
    pantalla.blit(nave_img, (nave_superior.x, nave_superior.y))

 
    if bala_disparada:
        bala_horizontal.x += velocidad_bala
        if bala_horizontal.x < 0:
            reset_bala_horizontal()

    
    bala_vertical.y += velocidad_bala_vertical
    if bala_vertical.y > h:
        reset_bala_vertical()

    
    pantalla.blit(bala_img, (bala_horizontal.x, bala_horizontal.y))
    pantalla.blit(bala_img, (bala_vertical.x, bala_vertical.y))

    
    if jugador.colliderect(bala_horizontal) or jugador.colliderect(bala_vertical):
        print("!Chocaste con la bala!")
        reiniciar_juego()

def main():
    """Bucle principal del juego, maneja eventos y lógica."""
    global salto, en_suelo, accion_actual, tiempo_accion
    reloj = pygame.time.Clock()
    mostrar_menu()
    correr = True
    reset_bala_horizontal()
    reset_bala_vertical()

    while correr:
        movimiento = 0

       
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_LCTRL and en_suelo:
             salto = True
             en_suelo = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            jugador.x = max(0, jugador.x - 5)
            movimiento = 1
        elif keys[pygame.K_RIGHT]:
            jugador.x = min(w - jugador.width, jugador.x + 5)
            movimiento = 2
        else:
            movimiento = 0

        
        if salto:
            manejar_salto()

        
        destino = bala_vertical.x - jugador.width // 2
        regresar_caminando = (
            bala_vertical.y > jugador.y + jugador.height and
            abs(jugador.x - destino) > 3
        )

        if modo_auto:
            
            bala_vertical_cerca_x = abs(jugador.x - bala_vertical.x) < 40  
            bala_vertical_cerca_y = (bala_vertical.y < jugador.y + jugador.height) and (bala_vertical.y > jugador.y - 60)
            if en_suelo and prediccion_salto() and jugador.x > 10 and not (bala_vertical_cerca_x and bala_vertical_cerca_y):
                salto = True
                en_suelo = False

            # Lógica para regresar caminando a la posición origen luego de esquivar
            if regresar_caminando:
                if jugador.x < destino:
                    jugador.x += 10 #6 es un valor ajustable para la velocidad de regreso
                elif jugador.x > destino:
                    jugador.x -= 15#6 es un valor ajustable para la velocidad de regreso
            else:
                # Control de cooldown para acciones laterales
                mov_pred = prediccion_movimiento()
                if mov_pred != accion_actual:
                    if tiempo_accion >= UMBRAL_TIEMPO:
                        accion_actual = mov_pred
                        tiempo_accion = 0
                    else:
                        tiempo_accion += 1
                else:
                    tiempo_accion = 0

                dx = bala_vertical.x - jugador.x
                if accion_actual == 1 and jugador.x > 0 and abs(dx) < UMBRAL_PELIGRO:
                    jugador.x -= 5
                elif accion_actual == 2 and jugador.x < w - jugador.width and abs(dx) < UMBRAL_PELIGRO:
                    jugador.x += 5
        else:
            if regresar_caminando:
                if jugador.x < destino:
                    jugador.x += 10 # Ajusta la velocidad de regreso
                elif jugador.x > destino:
                    jugador.x -= 15 # Ajusta la velocidad de regreso
            else:
                guardar_datos_salto()
                if movimiento != 0:
                    guardar_datos_movimiento(movimiento)

        
        if not bala_disparada:
            disparar_bala_horizontal()

    
        update()
        pygame.display.flip()
        reloj.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()