import struct
from collections import Counter
import heapq
from itertools import count
contador_global = count()
# Clase Nodo
class Nodo:
    def __init__(self, caracter=None, frecuencia=0):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None
        self.orden = next(contador_global) 
    def __lt__(self, otro):
        if self.frecuencia == otro.frecuencia:
            return self.orden < otro.orden
        return self.frecuencia < otro.frecuencia
# Construir el árbol de Huffman desde frecuencias
def construir_arbol(frecuencias):
    heap = [Nodo(c, f) for c, f in frecuencias]
    heapq.heapify(heap)

    while len(heap) > 1:
        nodo1 = heapq.heappop(heap)
        nodo2 = heapq.heappop(heap)
        nuevo = Nodo(None, nodo1.frecuencia + nodo2.frecuencia)
        nuevo.izquierda = nodo1
        nuevo.derecha = nodo2
        heapq.heappush(heap, nuevo)

    return heap[0]

# Decodificar los bits usando el árbol
def decodificar_bits(bits, raiz):
    mensaje = ""
    actual = raiz
    for bit in bits:
        actual = actual.izquierda if bit == "0" else actual.derecha
        if actual.caracter is not None:
            mensaje += actual.caracter
            actual = raiz
    return mensaje

# Leer archivo binario como lo especificaste
def leer_archivo_binario(path):
    with open(path, "rb") as f:
        # Leer cantidad de caracteres (4 bytes)
        cantidad = int.from_bytes(f.read(4), "big")

        frecuencias = []
        for _ in range(cantidad):
            caracter = f.read(1).decode("utf-8")
            frecuencia = int.from_bytes(f.read(2), "big")
            frecuencias.append((caracter, frecuencia))
        bits_descartados = int.from_bytes(f.read(1), "big")
        contenido = f.read()

    return frecuencias, bits_descartados, contenido

# Convertir los bytes en una secuencia de bits
def bytes_a_bits(data, bits_descartados):
    bits = ""
    for byte in data:
        bits += f"{byte:08b}"
    if bits_descartados > 0:
        bits = bits[:-bits_descartados]
    return bits

# Función principal
def decodificar_archivo(path="salida.bin"):
    frecuencias, bits_descartados, codificados = leer_archivo_binario(path)
    arbol=construir_arbol(frecuencias)
    print("Frecuencias:", frecuencias)
    print("Bits descartados:", bits_descartados)
    print("Bytes codificados (hex):", codificados.hex())

    arbol = construir_arbol(frecuencias)
    bits = bytes_a_bits(codificados, bits_descartados)
    print("Bits:", bits)

    mensaje = decodificar_bits(bits, arbol)
    print("Mensaje decodificado:", mensaje)


if __name__ == "__main__":
    decodificar_archivo("salida.bin")
