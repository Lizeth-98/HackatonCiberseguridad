# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 12:35:16 2024

@author: tovim_ii0d4hu
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier

# Paso 1: Leer los datos del archivo Excel
data = pd.read_excel('C:/Users/cs940/OneDrive/Documentos/Hackatones/Hackaton Cyberseguridad/10,000 datos de entrenamiento bien.xlsx')

# Paso 2: Preprocesar los datos
# Eliminar la columna 'datetime' del dataset ya que no se utilizará para la predicción
data = data.drop('datetime', axis=1)

# Convertir la columna objetivo (crime_type) a valores numéricos
le = LabelEncoder()
data['crime_type'] = le.fit_transform(data['crime_type'])

# Separar las características de la columna objetivo
X = data.drop('crime_type', axis=1)  # Todas las columnas menos 'crime_type'
y = data['crime_type']  # Solo la columna 'crime_type'

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Escalar los datos (normalización)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Paso 3: Entrenar un modelo de Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Paso 4: Predecir el tipo de crimen en el conjunto de prueba
y_pred = model.predict(X_test)

# Mostrar un reporte de clasificación
print(classification_report(y_test, y_pred, target_names=le.classes_))

# Hacer predicciones sobre eventos futuros (asegúrate de que los datos tengan el mismo formato que los de entrenamiento)
nuevos_eventos = [[19.432608, -99.133209]]  # Solo latitud y longitud

# Convertir nuevos eventos en un DataFrame con los mismos nombres de características que X_train
nuevos_eventos_df = pd.DataFrame(nuevos_eventos, columns=X.columns)

# Verificar el número de características
if len(nuevos_eventos[0]) == X_train.shape[1]:
    nuevos_eventos_escalados = scaler.transform(nuevos_eventos_df)
    nuevas_predicciones = model.predict(nuevos_eventos_escalados)
    # Imprimir las predicciones en su formato original (tipo de crimen)
    print("Predicción de nuevos eventos:", le.inverse_transform(nuevas_predicciones))
else:
    print(f"El número de características de los nuevos eventos ({len(nuevos_eventos[0])}) no coincide con el número de características de los datos de entrenamiento ({X_train.shape[1]}).")
