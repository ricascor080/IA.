import cv2
import mediapipe as mp
import numpy as np
import json
import os

# Inicializar MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=2, 
                                  min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

# Landmarks usados
selected_points = [33, 133, 362, 263, 61, 291]

# Cargar personas guardadas si existen
personas_guardadas = []
if os.path.exists("puntos_guardados.json"):
    with open("puntos_guardados.json", "r") as f:
        personas_guardadas = json.load(f)

def distancia(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def identificar_persona(distancias_actuales):
    tolerancia = 10  # Ajusta según tu caso
    for persona in personas_guardadas:
        dist = persona["distancias"]
        dif_ojos_izq = abs(distancias_actuales["ojo_izquierdo"] - dist.get("ojo_izquierdo", 0))
        dif_ojos_der = abs(distancias_actuales["ojo_derecho"] - dist.get("ojo_derecho", 0))
        dif_boca     = abs(distancias_actuales["boca"] - dist.get("boca", 0))

        if dif_ojos_izq <= tolerancia and dif_ojos_der <= tolerancia and dif_boca <= tolerancia:
            return f"Persona {persona['persona_id']}"
    return "Desconocido"

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            puntos = {}
            for idx in selected_points:
                x = int(face_landmarks.landmark[idx].x * frame.shape[1])
                y = int(face_landmarks.landmark[idx].y * frame.shape[0])
                puntos[str(idx)] = {'x': x, 'y': y}
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            # Calcular distancias
            distancias = {}
            if all(k in puntos for k in ['33', '133']):
                p1 = (puntos['33']['x'], puntos['33']['y'])
                p2 = (puntos['133']['x'], puntos['133']['y'])
                distancias["ojo_izquierdo"] = int(distancia(p1, p2))
                cv2.line(frame, p1, p2, (0, 255, 0), 2)

            if all(k in puntos for k in ['362', '263']):
                p1 = (puntos['362']['x'], puntos['362']['y'])
                p2 = (puntos['263']['x'], puntos['263']['y'])
                distancias["ojo_derecho"] = int(distancia(p1, p2))
                cv2.line(frame, p1, p2, (0, 200, 255), 2)

            if all(k in puntos for k in ['61', '291']):
                p1 = (puntos['61']['x'], puntos['61']['y'])
                p2 = (puntos['291']['x'], puntos['291']['y'])
                distancias["boca"] = int(distancia(p1, p2))
                cv2.line(frame, p1, p2, (255, 0, 0), 2)

            # Identificar persona
            if len(distancias) == 3:
                nombre_persona = identificar_persona(distancias)
                cv2.putText(frame, nombre_persona, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.putText(frame, "Presiona 's' para guardar | 'q' para salir", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    cv2.imshow('Reconocimiento Facial Simple', frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

    elif key == ord('s'):
        if 'distancias' in locals() and 'puntos' in locals():
            nueva_persona = {
                "persona_id": len(personas_guardadas) + 1,
                "landmarks": puntos,
                "distancias": distancias
            }
            personas_guardadas.append(nueva_persona)
            with open("puntos_guardados.json", "w") as f:
                json.dump(personas_guardadas, f, indent=4)
            print("✅ Persona guardada como:", nueva_persona["persona_id"])

cap.release()
cv2.destroyAllWindows()
