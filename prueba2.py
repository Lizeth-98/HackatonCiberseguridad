import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Definir puntos de interés en la colonia con una disposición no lineal
puntos_interes = {
    'Punto1': (21.8853, -102.2905),
    'Punto2': (21.8858, -102.2922),
    'Punto3': (21.8845, -102.2915),
    'Punto4': (21.8865, -102.2932),
    'Punto5': (21.8838, -102.2890),
    'Parque': (21.8873, -102.2921),
    'EstacionC': (21.8840, -102.2940)
}

# Crear matriz de distancias
def calcular_distancia(coord1, coord2):
    return np.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

# Generar matriz de distancias
n = len(puntos_interes)
matriz_distancias = np.zeros((n, n))
puntos_lista = list(puntos_interes.values())
for i in range(n):
    for j in range(n):
        matriz_distancias[i][j] = calcular_distancia(puntos_lista[i], puntos_lista[j])

# Definir variables de entrada y salida para lógica difusa
distancia = ctrl.Antecedent(np.arange(0, 101, 1), 'distancia')
tiempo = ctrl.Antecedent(np.arange(0, 61, 1), 'tiempo')
consumo = ctrl.Antecedent(np.arange(0, 51, 1), 'consumo')
calidad_ruta = ctrl.Consequent(np.arange(0, 101, 1), 'calidad_ruta')

# Definir conjuntos difusos
distancia['corta'] = fuzz.trimf(distancia.universe, [0, 0, 50])
distancia['media'] = fuzz.trimf(distancia.universe, [25, 50, 75])
distancia['larga'] = fuzz.trimf(distancia.universe, [50, 100, 100])

tiempo['corto'] = fuzz.trimf(tiempo.universe, [0, 0, 30])
tiempo['medio'] = fuzz.trimf(tiempo.universe, [15, 30, 45])
tiempo['largo'] = fuzz.trimf(tiempo.universe, [30, 60, 60])

consumo['bajo'] = fuzz.trimf(consumo.universe, [0, 0, 25])
consumo['medio'] = fuzz.trimf(consumo.universe, [10, 25, 40])
consumo['alto'] = fuzz.trimf(consumo.universe, [25, 50, 50])

calidad_ruta['muy_buena'] = fuzz.trimf(calidad_ruta.universe, [0, 0, 50])
calidad_ruta['buena'] = fuzz.trimf(calidad_ruta.universe, [25, 50, 75])
calidad_ruta['aceptable'] = fuzz.trimf(calidad_ruta.universe, [50, 75, 100])
calidad_ruta['mala'] = fuzz.trimf(calidad_ruta.universe, [50, 100, 100])

# Definir reglas de inferencia
regla1 = ctrl.Rule(distancia['corta'] & tiempo['corto'] & consumo['bajo'], calidad_ruta['muy_buena'])
regla2 = ctrl.Rule(distancia['media'] & tiempo['medio'] & consumo['medio'], calidad_ruta['buena'])
regla3 = ctrl.Rule(distancia['larga'] | tiempo['largo'] | consumo['alto'], calidad_ruta['mala'])

# Crear el sistema de control difuso
sistema_calidad = ctrl.ControlSystem([regla1, regla2, regla3])
simulador = ctrl.ControlSystemSimulation(sistema_calidad)

# Funciones para calcular distancia, tiempo y consumo de energía
def calcular_distancia_total(ruta, matriz_distancias):
    distancia = 0
    for i in range(len(ruta) - 1):
        distancia += matriz_distancias[ruta[i]][ruta[i + 1]]
    distancia += matriz_distancias[ruta[-1]][ruta[0]]
    return distancia

def calcular_tiempo_total(distancia_total, velocidad_dron):
    return distancia_total / velocidad_dron

def calcular_consumo_energia(distancia_total, peso_dron):
    return distancia_total * (peso_dron * 0.1)

# Definir rutas y evaluar la mejor con un límite de distancia
rutas = [
    [0, 1, 2, 4, 6],
    [0, 2, 5, 3, 6],
    [0, 4, 3, 1, 6],
    [0, 5, 2, 4, 6],
    [0, 1, 5, 3, 6],
    [0, 3, 1, 5, 6],
    [0, 4, 5, 2, 6],
    [0, 3, 4, 1, 6]
]

mejor_calidad = -1
mejor_ruta = None
distancia_maxima = 1.5  # Distancia máxima en km para el dron

# Parámetros del dron
velocidad_dron = 5  # m/s
peso_dron = 1.5  # kg

for ruta in rutas:
    # Calcular distancia, tiempo y consumo para cada ruta
    distancia_total = calcular_distancia_total(ruta, matriz_distancias)
    
    # Saltar si la ruta supera la distancia máxima
    if distancia_total > distancia_maxima:
        continue
    
    tiempo_total = calcular_tiempo_total(distancia_total, velocidad_dron)
    consumo_total = calcular_consumo_energia(distancia_total, peso_dron)

    # Asignar valores al simulador
    simulador.input['distancia'] = distancia_total
    simulador.input['tiempo'] = tiempo_total
    simulador.input['consumo'] = consumo_total

    # Calcular la calidad de la ruta
    simulador.compute()
    
    calidad_ruta_actual = simulador.output['calidad_ruta']
    
    # Evaluar si esta ruta es la mejor
    if calidad_ruta_actual > mejor_calidad:
        mejor_calidad = calidad_ruta_actual
        mejor_ruta = ruta

# Imprimir la mejor ruta y su calidad
print("Mejor ruta:", [list(puntos_interes.keys())[i] for i in mejor_ruta])
print("Calidad de la ruta:", mejor_calidad)

# Visualizar rutas y la mejor ruta
fig, ax = plt.subplots()
x, y = zip(*puntos_interes.values())
labels = list(puntos_interes.keys())

# Graficar todas las rutas
for ruta in rutas:
    x_ruta = [x[i] for i in ruta] + [x[ruta[0]]]
    y_ruta = [y[i] for i in ruta] + [y[ruta[0]]]
    ax.plot(x_ruta, y_ruta, linestyle='--', color='gray', alpha=0.5)

# Graficar la mejor ruta
if mejor_ruta:
    mejor_x = [x[i] for i in mejor_ruta] + [x[mejor_ruta[0]]]
    mejor_y = [y[i] for i in mejor_ruta] + [y[mejor_ruta[0]]]
    ax.plot(mejor_x, mejor_y, linestyle='-', color='blue', marker='o', label="Mejor Ruta")

# Añadir etiquetas a los puntos
for i, txt in enumerate(labels):
    ax.annotate(txt, (x[i], y[i]))

ax.set_title("Rutas y Mejor Ruta en el Problema del Agente Viajero")
ax.set_xlabel("Longitud")
ax.set_ylabel("Latitud")
plt.legend()
plt.show()
