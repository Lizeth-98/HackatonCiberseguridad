# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 17:00:06 2024

@author: cs940
"""

import face_recognition
import numpy as np

class FaceManager:
    def __init__(self):
        self.face_encodings_db = []
        self.face_ids = []
        self.next_id = 0

    def load_data(self, data):
        """Cargar los datos de la base de datos previamente guardada."""
        self.face_encodings_db, self.face_ids, self.next_id = data

    def save_data(self):
        """Devolver los datos actuales para ser guardados."""
        return (self.face_encodings_db, self.face_ids, self.next_id)

    def get_face_id(self, face_encoding):
        """Compara la encoding del rostro con la base de datos. Si es nuevo, le asigna un ID único."""
        if len(self.face_encodings_db) == 0:
            # Si no hay rostros conocidos, agregar el primero y asignarle un ID
            self.face_encodings_db.append(face_encoding)
            self.face_ids.append(self.next_id)
            self.next_id += 1
            return self.face_ids[-1]
        
        # Comparar el rostro con los rostros conocidos
        matches = face_recognition.compare_faces(self.face_encodings_db, face_encoding)
        face_distances = face_recognition.face_distance(self.face_encodings_db, face_encoding)
        
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            return self.face_ids[best_match_index]
        else:
            # Si es un nuevo rostro, agregarlo a la base de datos
            self.face_encodings_db.append(face_encoding)
            self.face_ids.append(self.next_id)
            self.next_id += 1
            return self.face_ids[-1]
