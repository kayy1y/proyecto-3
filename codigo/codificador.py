import heapq
from collections import Counter
import os

# ========== CLASE NODO PARA EL ÁRBOL DE HUFFMAN ==========

class Nodo:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

# ========== FUNCIONES PARA CONSTRUIR ÁRBOL Y TABLA ==========

def construir_arbol_con_animacion(frecuencias):
    heap = [Nodo(c, f) for c, f in frecuencias.items()]
    heapq.heapify(heap)
    pasos = []

    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        nuevo = Nodo(None, n1.frecuencia + n2.frecuencia)
        nuevo.izquierda = n1
        nuevo.derecha = n2
        pasos.append((nuevo, n1, n2))
        heapq.heappush(heap, nuevo)

    return heap[0], pasos

def generar_tabla_codigos(nodo, codigo="", tabla=None):
    if tabla is None:
        tabla = {}

    if nodo.caracter is not None:
        tabla[nodo.caracter] = codigo
    else:
        if nodo.izquierda:
            generar_tabla_codigos(nodo.izquierda, codigo + "0", tabla)
        if nodo.derecha:
            generar_tabla_codigos(nodo.derecha, codigo + "1", tabla)

    return tabla

# ========== FUNCIONES PARA CODIFICAR Y CONVERTIR A BYTES ==========

def codificar_mensaje(mensaje, tabla_codigos):
    return ''.join([tabla_codigos[char] for char in mensaje])

def bits_a_bytes(bits):
    bits_descartados = (8 - len(bits) % 8) % 8
    bits += '0' * bits_descartados
    byte_array = bytearray()

    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        byte_array.append(int(byte, 2))

    return byte_array, bits_descartados

# ========== ESCRIBIR ARCHIVO BINARIO .bin ==========

def escribir_archivo_bin(ruta, frecuencias, bytes_codificados, bits_descartados):
    with open(ruta, "wb") as f:
        cantidad = len(frecuencias)
        f.write(cantidad.to_bytes(4, byteorder='big'))  # 4 bytes

        for caracter in sorted(frecuencias):
            frecuencia = frecuencias[caracter]
            f.write(caracter.encode('utf-8'))  # 1 byte
            f.write(frecuencia.to_bytes(2, byteorder='big'))  # 2 bytes

        f.write(bits_descartados.to_bytes(1, byteorder='big'))  # 1 byte
        f.write(bytes_codificados)  # datos codificados

def obtener_ultima_ruta_bin():
    carpeta = "binarios"
    archivos = [f for f in os.listdir(carpeta) if f.startswith("salida") and f.endswith(".bin")]
    archivos.sort()
    if archivos:
        return os.path.join(carpeta, archivos[-1])
    else:
        return None

# ========== FUNCIÓN PRINCIPAL DEL CODIFICADOR ==========

def codificar_archivo(mensaje, ruta_salida_ignorada="IGNORADO.bin"):
    frecuencias = dict(Counter(mensaje))
    arbol, _ = construir_arbol_con_animacion(frecuencias)
    tabla = generar_tabla_codigos(arbol)
    bits = codificar_mensaje(mensaje, tabla)
    bytes_codificados, bits_descartados = bits_a_bytes(bits)

    carpeta = "binarios"
    os.makedirs(carpeta, exist_ok=True)
    archivos_existentes = [f for f in os.listdir(carpeta) if f.startswith("salida") and f.endswith(".bin")]
    numero = len(archivos_existentes) + 1
    nombre_archivo = f"salida{numero}.bin"
    ruta_completa = os.path.join(carpeta, nombre_archivo)

    escribir_archivo_bin(ruta_completa, frecuencias, bytes_codificados, bits_descartados)

    print("Archivo guardado en:", ruta_completa)
    return ruta_completa







