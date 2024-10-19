from kybra import Opt, query, StableBTreeMap, update, void, Vec

# Inicializamos el mapa clave-valor con zonas como clave y crímenes como valor.
db = StableBTreeMap[str, str](memory_id=0, max_key_size=100, max_value_size=100)

@query
def get(key: str) -> Opt[str]:
    return db.get(key)

@update
def set(zona: str, crimen: str) -> void:
    # Si la zona ya tiene crímenes asociados, añadimos el nuevo crimen.
    existing_value = db.get(zona)
    if existing_value:
        new_value = f"{existing_value},{crimen}"  # Añadir crimen separado por coma
        db.insert(zona, new_value)
    else:
        db.insert(zona, crimen)  # Si no hay crímenes, lo insertamos directamente

@query
def getAllZonas() -> Vec[str]:
    # Obtenemos todas las claves (zonas)
    return db.keys()

@query
def getAllCrimenes() -> Vec[str]:
    # Creamos un set para evitar duplicados de crímenes
    crimenes_set = list()
    for zona in db.keys():
        value = db.get(zona)
        if value:
            # Dividimos los crímenes por coma y añadimos al set
            crimenes = value.split(',')
            crimenes_set = crimenes_set + crimenes 
    return crimenes_set  # Convertimos el set en una lista

@query
def getCrimenesByZona(zona: str) -> Vec[str]:
    # Obtenemos los crímenes de una zona específica
    value = db.get(zona)
    if value:
        return value.split(',')  # Retornamos los crímenes como una lista
    return []

@query
def getZonasByCrimen(crimen: str) -> Vec[str]:
    # Lista para almacenar las zonas donde ocurrió el crimen
    zonas_con_crimen = []
    
    # Iteramos por todas las zonas en el mapa
    for zona in db.keys():
        value = db.get(zona)
        if value:
            # Dividimos los crímenes asociados a la zona y buscamos el crimen
            crimenes = value.split(',')
            if crimen in [c.strip() for c in crimenes]:  # Aseguramos que no haya espacios
                zonas_con_crimen.append(zona)
    
    return zonas_con_crimen

