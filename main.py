import math

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

vertices = (
    (-1, 0, 0),
    (1, 0, 0),
    (0, 0, math.sqrt(3)),
    (0, math.sqrt(33) / 3, math.sqrt(3) / 3)
)

edges = (
    (0, 1),
    (0, 2),
    (0, 3),
    (1, 2),
    (1, 3),
    (2, 3),
)

colours = (
    (1, 0, 0),
    (1, 1, 0),
    (1, 0, 1),
)

surfaces = (
    (0, 1, 2),
    (0, 2, 3),
    (0, 1, 3),
    (1, 2, 3)
)

ground_vertices = (
    (-4000, 0, 3000),
    (4000, 0, 4000),
    (-4000, 0, -4000),
    (4000, 0, -4000)
)

light_direction = (-1, -1, -1)
light_position = (0, 1, 1)
light_color = (1, 1, 1)


def enable_lighting_direction():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glLightfv(GL_LIGHT0, GL_POSITION, (light_direction[0], light_direction[1], light_direction[2], 0.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))


def enable_lighting_point():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT1)

    glLightfv(GL_LIGHT1, GL_POSITION, (light_position[0], light_position[1], light_position[2], 1.0))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))


def disable_lighting():
    glDisable(GL_LIGHTING)
    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHT1)


def update_light():
    global light_position
    x, y, z = light_position

    global light_color
    r, g, b = light_color


    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                y += 0.1
            elif event.key == pygame.K_s:
                y -= 0.1
            elif event.key == pygame.K_a:
                x -= 0.1
            elif event.key == pygame.K_d:
                x += 0.1
            elif event.key == pygame.K_q:
                z += 0.1
            elif event.key == pygame.K_e:
                z -= 0.1
            elif event.key == pygame.K_z:
                r -= 0.3
            elif event.key == pygame.K_x:
                g -= 0.3
            elif event.key == pygame.K_c:
                b -= 0.3

    if r <=0:
        r = 1
    if g <=0:
        g = 1
    if b <=0:
        b = 1
    light_position = (x, y, z)
    light_color = (r, g, b)

    glLightfv(GL_LIGHT1, GL_POSITION, (x, y, z, 1.0))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (r, g, b, 1.0))





def midpoint(first_point, second_point):
    return (first_point[0] + second_point[0]) / 2, (first_point[1] + second_point[1]) / 2, (
            first_point[2] + second_point[2]) / 2


def get_sub_tetrahedrons(vertices):
    midpoints = []
    for edge in edges:
        midpoints.append(midpoint(vertices[edge[0]], vertices[edge[1]]))

    return [
        (vertices[0], midpoints[0], midpoints[1], midpoints[2]),
        (vertices[1], midpoints[0], midpoints[3], midpoints[4]),
        (vertices[2], midpoints[1], midpoints[3], midpoints[5]),
        (vertices[3], midpoints[2], midpoints[4], midpoints[5])
    ]


def draw_tetrahedron(vertices, textures_on_off):
    glBegin(GL_LINES)
    glColor3fv((1, 1, 1))
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

    if (textures_on_off == False):
        glBegin(GL_TRIANGLES)
        glColor3f(0.5, 0.3, 0.8)

        for surface in surfaces:
            for vertex in surface:
                glVertex3fv(vertices[vertex])
        glEnd()


def do_sierpinski_pyramid(vertices, textures_on_off, depth):
    if depth == 0:
        draw_tetrahedron(vertices, textures_on_off)
        return
    tetrahedrons = get_sub_tetrahedrons(vertices)
    for tetra in tetrahedrons:
        do_sierpinski_pyramid(tetra, textures_on_off, depth - 1)


def ground():
    glBegin(GL_QUADS)
    glColor3fv((0.3, 0.9, 1))
    for vertex in ground_vertices:
        glVertex3fv(vertex)
    glEnd()


def main():
    show_textures = False
    rot_val = 0
    rot_speed = 0.4
    is_rotating = True

    inputt = int(input("Please give the number of recursive depth of Sierpinski's Pyramid: "))
    depthh = inputt
    if depthh > 6:
        depthh = 6

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, -1, -10)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(0, 0, 1.0)
                if event.button == 5:
                    glTranslatef(0, 0, -1.0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    glTranslatef(0, -0.5, 0)
                if event.key == pygame.K_DOWN:
                    glTranslatef(0, 0.5, 0)
                if event.key == pygame.K_LEFT:
                    glTranslatef(0.5, 0, 0)
                if event.key == pygame.K_RIGHT:
                    glTranslatef(-0.5, 0, 0)

                if event.key == pygame.K_r:
                    is_rotating = not (is_rotating)

                if event.key == pygame.K_t:
                    show_textures = not (show_textures)

                if event.key == pygame.K_l:
                    enable_lighting_direction()
                if event.key == pygame.K_k:
                    disable_lighting()
                if event.key == pygame.K_p:
                    enable_lighting_point()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        rot_val += is_rotating

        ground()

        glPushMatrix()
        glRotatef(rot_val, 0, 1, 0)

        do_sierpinski_pyramid(vertices, show_textures, depthh)
        glPopMatrix()



        update_light()


        pygame.display.flip()
        pygame.time.wait(10)


main()
