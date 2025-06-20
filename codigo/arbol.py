import pygame
import time
import sys

ANCHO = 800
ALTO = 600
RADIO = 20
FUENTE = None

class Nodo:
    def __init__(self, caracter=None,frecuencia=0):
        self.caracter = caracter 
        self.frecuencia=frecuencia # puede ser letra o None
        self.izquierda = None
        self.derecha = None

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

class NodoVisual:
    def __init__(self, nodo, x, y):
        self.nodo = nodo
        self.x = x
        self.y = y
        self.izquierda = None
        self.derecha = None

def crear_nodo_visual(nodo, x, y, dx):
    if nodo is None:
        return None
    visual = NodoVisual(nodo, x, y)
    visual.izquierda = crear_nodo_visual(nodo.izquierda, x - dx, y + 80, dx // 2)
    visual.derecha = crear_nodo_visual(nodo.derecha, x + dx, y + 80, dx // 2)
    return visual

def dibujar_arbol(screen, visual):
    if visual is None:
        return
    color = (180, 180, 180)
    pygame.draw.circle(screen, color, (visual.x, visual.y), RADIO)
    texto = FUENTE.render(visual.nodo.caracter if visual.nodo.caracter else "*", True, (0, 0, 0))
    rect = texto.get_rect(center=(visual.x, visual.y))
    screen.blit(texto, rect)

    if visual.izquierda:
        pygame.draw.line(screen, (0, 0, 0), (visual.x, visual.y), (visual.izquierda.x, visual.izquierda.y))
        dibujar_arbol(screen, visual.izquierda)

    if visual.derecha:
        pygame.draw.line(screen, (0, 0, 0), (visual.x, visual.y), (visual.derecha.x, visual.derecha.y))
        dibujar_arbol(screen, visual.derecha)

def resaltar(screen, visual, color):
    pygame.draw.circle(screen, color, (visual.x, visual.y), RADIO)
    texto = FUENTE.render(visual.nodo.caracter if visual.nodo.caracter else "*", True, (255, 255, 255))
    rect = texto.get_rect(center=(visual.x, visual.y))
    screen.blit(texto, rect)
    pygame.display.flip()

def dibujar_nodo(screen, nodo, x, y, color=(0, 0, 0), radio=20):
    pygame.draw.circle(screen, color, (x, y), radio)
    texto = FUENTE.render(nodo.caracter if nodo.caracter else "*", True, (255, 255, 255))
    rect = texto.get_rect(center=(x, y))
    screen.blit(texto, rect)

def animar_decodificacion(bits, raiz_logica, mensaje_esperado):
    global FUENTE
    pygame.init()
    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Decodificación Huffman - Pygame")
    FUENTE = pygame.font.SysFont("Arial", 24)

    raiz_visual = crear_nodo_visual(raiz_logica, ANCHO // 2, 50, 200)
    actual_visual = raiz_visual
    actual_logico = raiz_logica
    mensaje = ""

    for bit in bits:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Recorrer bit a bit
        if bit == "0":
            actual_visual = actual_visual.izquierda
            actual_logico = actual_logico.izquierda
        else:
            actual_visual = actual_visual.derecha
            actual_logico = actual_logico.derecha

        # Iluminar recorrido (naranja)
        screen.fill((255, 255, 255))
        dibujar_arbol(screen, raiz_visual)
        resaltar(screen, actual_visual, (255, 165, 0))
        texto = FUENTE.render("Mensaje: " + mensaje, True, (0, 0, 0))
        screen.blit(texto, (20, ALTO - 40))
        pygame.display.flip()
        time.sleep(0.5)

        # Si llega a hoja (carácter)
        if actual_logico.caracter is not None:
            mensaje += actual_logico.caracter
            # Iluminar nodo final (verde)
            screen.fill((255, 255, 255))
            dibujar_arbol(screen, raiz_visual)
            resaltar(screen, actual_visual, (0, 200, 0))
            texto = FUENTE.render("Mensaje: " + mensaje, True, (0, 0, 0))
            screen.blit(texto, (20, ALTO - 40))
            pygame.display.flip()
            time.sleep(0.5)

            # Reiniciar desde raíz
            actual_visual = raiz_visual
            actual_logico = raiz_logica

    # Esperar al final
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

def animar_construccion(pasos):
    global FUENTE
    pygame.init()
    pantalla = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Construcción del Árbol de Huffman")
    FUENTE = pygame.font.SysFont("Arial", 24)

    fondo_color = (255, 255, 255)

    for paso in pasos:
        padre, izq, der = paso
        pantalla.fill(fondo_color)

        dibujar_nodo(pantalla, izq, 200, 300, color=(100, 100, 255))
        dibujar_nodo(pantalla, der, 400, 300, color=(100, 100, 255))
        dibujar_nodo(pantalla, padre, 300, 150, color=(0, 0, 255))

        pygame.draw.line(pantalla, (0, 0, 0), (300, 150), (200, 300), 2)
        pygame.draw.line(pantalla, (0, 0, 0), (300, 150), (400, 300), 2)

        pygame.display.flip()
        time.sleep(1)

    time.sleep(2)
    pygame.quit()
