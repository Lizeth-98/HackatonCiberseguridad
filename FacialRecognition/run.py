import cv2
import numpy as np
import face_recognition
import pickle
import os

# Inicializar la cámara
camera = cv2.VideoCapture(0)

# Ruta para guardar las codificaciones de las caras
data_path = "face_data.pickle"
external_faces_path = "C:/Users/cs940/OneDrive/Documentos/Hackatones/Hackaton Cyberseguridad/FacialRecognition/external_faces"  # Directorio donde se guardan las imágenes externas

# Cargar caras conocidas si existen
if os.path.exists(data_path):
    with open(data_path, "rb") as f:
        known_face_encodings, known_face_names = pickle.load(f)
else:
    known_face_encodings = []
    known_face_names = []
    print("No se encontraron datos previos. Iniciando nuevo reconocimiento.")

# Cargar imágenes externas y generar sus codificaciones
def load_external_faces(external_faces_path):
    for filename in os.listdir(external_faces_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            img_path = os.path.join(external_faces_path, filename)
            image = face_recognition.load_image_file(img_path)
            face_encodings = face_recognition.face_encodings(image)

            if face_encodings:
                known_face_encodings.append(face_encodings[0])
                name = os.path.splitext(filename)[0]  # Usa el nombre del archivo como el nombre de la persona
                known_face_names.append(name)
                print(f"Se cargó la imagen de {name}.")

# Llamar a la función para cargar imágenes externas
if os.path.exists(external_faces_path):
    load_external_faces(external_faces_path)

while True:
    # Capturar un frame de la cámara
    ret, frame = camera.read()

    if not ret:
        print("Error al capturar la imagen.")
        break

    # Convertir la imagen de BGR a RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detectar las ubicaciones de las caras en el frame
    face_locations = face_recognition.face_locations(rgb_frame)

    # Solo procesar si se detectan caras
    if face_locations:
        try:
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        except Exception as e:
            print(f"Error al calcular face_encodings: {e}")
            continue  # Saltar al siguiente frame en caso de error

        # Recorrer las caras detectadas
        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Comparar con las caras conocidas
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Desconocido"  # Nombre por defecto si no hay coincidencias

            # Si hay coincidencias, usar el primer nombre conocido
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

                # Emitir una señal (aquí solo se imprime, pero podrías agregar algo más avanzado)
                print(f"¡{name} ha sido detectado!")

            else:
                # Si no hay coincidencias, solicitar al usuario que ingrese un nombre
                name = input("Ingrese el nombre de la nueva persona: ")
                known_face_encodings.append(face_encoding)
                known_face_names.append(name)

                # Guardar la nueva codificación en el archivo
                with open(data_path, "wb") as f:
                    pickle.dump((known_face_encodings, known_face_names), f)

            # Dibujar un rectángulo alrededor de la cara
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (120, 0, 185), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (120, 0, 185), 2)

    # Mostrar el frame en una ventana
    cv2.imshow("Video", frame)

    # Presionar 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar las ventanas
camera.release()
cv2.destroyAllWindows()

