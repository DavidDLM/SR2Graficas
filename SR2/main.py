from gl import Renderer, _color_, V2

#################################

width = 1024
height = 512
black = _color_(0, 0, 0)
white = _color_(1, 1, 1)

rend = Renderer(width, height)

#################################

# Funcion para dibujar desde punto A a punto B


def draw(points, color=None):
    for x in range(len(points)):
        rend.glLine(points[x], points[(x+1) % len(points)], color)

#################################


# Linea
rend.glClear()
linea = [V2(150, 150), V2(800, 300)]
draw(linea, white)

#################################

rend.write('SR2.bmp')
