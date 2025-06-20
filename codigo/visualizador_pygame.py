import pygame
import time
import sys
import heapq
from arbol import Nodo

ANCHO = 800
ALTO = 600
RADIO = 20
FUENTE = None

class NodoVisual:
    def __init__(self, nodo_logico, x, y):
        self.nodo = nodo_logico
        self.x = x
        self.y = y
        self.izquierda = None
        self.derecha = None

def crear_nodo_visual(nodo, x, y, dx):
    if nodo is None:
        return None
    actual = NodoVisual(nodo, x, y)
    actual.izquierda = crear_nodo_visual(nodo.izquierda, x - dx, y + 80, dx // 2)
    actual.derecha = crear_nodo_visual(nodo.derecha, x + dx, y + 80, dx // 2)
    return actual

def dibujar_arbol(screen, nodo):
    if nodo is None:
        return
    color = (200, 200, 200)
    pygame.draw.circle(screen, color, (nodo.x, nodo.y), RADIO)
    valor = nodo.nodo.caracter if nodo.nodo.caracter else "*"
    texto = FUENTE.render(valor, True, (0, 0, 0))
    rect = texto.get_rect(center=(nodo.x, nodo.y))
    screen.blit(texto, rect)

    if nodo.izquierda:
        pygame.draw.line(screen, (0, 0, 0), (nodo.x, nodo.y), (nodo.izquierda.x, nodo.izquierda.y))
        dibujar_arbol(screen, nodo.izquierda)

    if nodo.derecha:
        pygame.draw.line(screen, (0, 0, 0), (nodo.x, nodo.y), (nodo.derecha.x, nodo.derecha.y))
        dibujar_arbol(screen, nodo.derecha)

def resaltar_nodo(screen, nodo, color):
    pygame.draw.circle(screen, color, (nodo.x, nodo.y), RADIO)
    valor = nodo.nodo.caracter if nodo.nodo.caracter else "*"
    texto = FUENTE.render(valor, True, (255, 255, 255))
    rect = texto.get_rect(center=(nodo.x, nodo.y))
    screen.blit(texto, rect)
    pygame.display.flip()

def animar_construccion_y_decodificacion(frecuencias, bits, arbol_final):
    global FUENTE
    pygame.init()
    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Decodificación del Árbol de Huffman")
    FUENTE = pygame.font.SysFont("Arial", 24)

    class NodoTmp:
        def __init__(self, caracter, frecuencia):
            self.caracter = caracter
            self.frecuencia = frecuencia
            self.izquierda = None
            self.derecha = None

        def __lt__(self, otro):
            return self.frecuencia < otro.frecuencia

    heap = [NodoTmp(c, f) for c, f in sorted(frecuencias.items(), key=lambda x: x[1])]
    heapq.heapify(heap)

    posiciones = {}
    nivel = 0
    x_pos = ANCHO // 2
    y_pos = 50

    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        nuevo = NodoTmp(None, n1.frecuencia + n2.frecuencia)
        nuevo.izquierda = n1
        nuevo.derecha = n2
        heapq.heappush(heap, nuevo)

        screen.fill((255, 255, 255))
        pygame.draw.circle(screen, (0, 0, 255), (x_pos, y_pos), RADIO)
        texto = FUENTE.render("*", True, (255, 255, 255))
        screen.blit(texto, texto.get_rect(center=(x_pos, y_pos)))
        pygame.display.flip()
        pygame.time.delay(700)

        pygame.draw.line(screen, (0, 0, 0), (x_pos, y_pos), (x_pos - 100, y_pos + 80), 3)
        pygame.draw.circle(screen, (150, 150, 255), (x_pos - 100, y_pos + 80), RADIO)
        pygame.display.flip()
        pygame.time.delay(700)

        pygame.draw.line(screen, (0, 0, 0), (x_pos, y_pos), (x_pos + 100, y_pos + 80), 3)
        pygame.draw.circle(screen, (150, 150, 255), (x_pos + 100, y_pos + 80), RADIO)
        pygame.display.flip()
        pygame.time.delay(700)

    if not bits:
        return

    raiz_visual = crear_nodo_visual(arbol_final, ANCHO // 2, 50, 200)
    mensaje = ""
    actual_visual = raiz_visual

    screen.fill((255, 255, 255))
    dibujar_arbol(screen, raiz_visual)
    pygame.display.flip()

    for bit in bits:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if bit == "0":
            actual_visual = actual_visual.izquierda
        else:
            actual_visual = actual_visual.derecha

        resaltar_nodo(screen, actual_visual, (255, 165, 0))
        pygame.time.delay(500)

        if actual_visual.nodo.caracter is not None:
            mensaje += actual_visual.nodo.caracter
            resaltar_nodo(screen, actual_visual, (0, 200, 0))
            pygame.time.delay(500)
            actual_visual = raiz_visual

        screen.fill((255, 255, 255))
        dibujar_arbol(screen, raiz_visual)
        texto = FUENTE.render("Mensaje: " + mensaje, True, (0, 0, 0))
        screen.blit(texto, (20, ALTO - 40))
        pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

