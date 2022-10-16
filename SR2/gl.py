# SR2
# Mario de Leon 19019
# Graficos por computadora basado en lo escrito por Ing. Carlos Alonso / Ing. Dennis Aldana

import struct
from collections import namedtuple

V2 = namedtuple('Point2', ['x', 'y'])


def char(c):
    # 1 byte
    return struct.pack('=c', c.encode('ascii'))


def word(w):
    # 2 bytes
    return struct.pack('=h', w)


def dword(d):
    # 4 bytes
    return struct.pack('=l', d)


def _color_(r, g, b):
    return bytes([int(b*255),
                  int(g*255),
                  int(r*255)])


# Colores default
white = _color_(1, 1, 1)
black = _color_(0, 0, 0)


class Renderer(object):
    def __init__(init, width, height):
        init.width = width
        init.height = height
        init.clearColor = black
        init.currColor = white
        init.glViewPort(0, 0, init.width, init.height)
        init.glClear()

    # El area donde se va a dibujar
    def glCreateWindow(init, width, height):
        init.width = width
        init.height = height
        init.glClear()

    # Utiliza las coordenadas
    def glViewPort(init, x, y, width, height):
        init.viewportX = x
        init.viewportY = y
        init.viewportWidth = width
        init.viewportHeight = height

    # Limpia los pixeles de la pantalla poniendolos en blanco o negro
    def glClear(init):
        init.framebuffer = [[init.clearColor for y in range(
            init.height)]for x in range(init.width)]

    # Coloca color de fondo
    def glClearColor(init, r, g, b):
        init.clearColor = _color_(r, g, b)

    # Dibuja un punto
    def glVertex(init, vertexX, vertexY, color=None):
        x = int((vertexX+1)*(init.viewportWidth/2)+init.viewportX)
        y = int((vertexY+1)*(init.viewportHeight/2)+init.viewportY)
        init.glPoint(x, y, color)

    def glPoint(init, x, y, color=None):
        # Coordenadas de la ventana
        if (0 <= x < init.width) and (0 <= y < init.height):
            init.framebuffer[x][y] = color or init.currColor

    # Se establece el color de dibujo, si no tiene nada se dibuja blanco
    def glColor(init, r, g, b):
        init.currColor = _color_(r, g, b)

    def glClearViewPort(init, color=None):
        for x in range(init.viewportX, init.viewportX + init.viewportWidth):
            for y in range(init.viewportY, init.viewportY + init.viewportHeight):
                init.glVertex(x, y, color)

    # Algoritmo de Bresenham para creación de lineas
    def glLine(init, v0, v1, color=None):
        # Bresenham line algorithm
        # y = m * x + b
        x0 = int(v0.x)
        x1 = int(v1.x)
        y0 = int(v0.y)
        y1 = int(v1.y)

        # Si el punto0 es igual al punto 1, dibujar solamente un punto
        if x0 == x1 and y0 == y1:
            init.glPoint(x0, y0, color)
            return

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx

        # Si la linea tiene pendiente mayor a 1 o menor a -1
        # intercambio las x por las y, y se dibuja la linea
        # de manera vertical
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        # Si el punto inicial X es mayor que el punto final X,
        # intercambio los puntos para siempre dibujar de
        # izquierda a derecha
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        offset = 0
        limit = 0.5
        m = dy / dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                # Dibujar de manera vertical
                init.glPoint(y, x, color)
            else:
                # Dibujar de manera horizontal
                init.glPoint(x, y, color)

            offset += m

            if offset >= limit:
                if y0 < y1:
                    y += 1
                else:
                    y -= 1

                limit += 1

    # Crea un archivo BMP
    def write(init, filename):
        with open(filename, "bw") as file:
            # pixel header
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))
            file.write(dword(14 + 40 + init.width * init.height * 3))
            file.write(word(0))
            file.write(word(0))
            file.write(dword(14 + 40))

            # informacion del header
            file.write(dword(40))
            file.write(dword(init.width))
            file.write(dword(init.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(init.width * init.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # pixel data
            for y in range(init.height):
                for x in range(init.width):
                    file.write(init.framebuffer[x][y])
