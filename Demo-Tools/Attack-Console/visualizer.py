"""Here goes the opengl stuff"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

key_sens = 0.4

# The Chaperone vertices and edges, received from vivedump.build_obj()
chap_vert = []
chap_edges = []
num_edges = 0

# List of tracked devices to draw
# (matrix4x4, type)
devices = []


# Defines the edges in a cube
cube_edge = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 3),
    (7, 4),
    (1, 5),
    (2, 6),
    (0, 4)
]

def get_rect(width, height, depth):
    """ Enter half the width height and depth you would like """
    return [
        (width, height, depth),
        (-width, height, depth),
        (-width, -height, depth),
        (width, -height, depth),
        (width, height, -depth),
        (-width, height, -depth),
        (-width, -height, -depth),
        (width, -height, -depth),
    ]


class Vis:

    # Starting camera location
    cam_x = 0
    cam_y = 7
    cam_z = -7

    def clear_chap(self):
        chap_vert[:] = []
        chap_edges[:] = []

    def set_num_edges(self, num):
        self.num_edges = num

    def update_edge(self, index, i, j):
        chap_edges[index] = [i, j]

    def add_vert(self, x, y, z):
        chap_vert.append((x, y, z))

    def update_vert(self, index, x, y, z):
        chap_vert[index] = [x, y, z]

    def add_edge(self, i, j):
        chap_edges.append((i, j))

    def set_device(self, x, type, i):
        if len(devices) <= i:
            devices.append([x, type])
        else:
            devices[i] = (x, type)

    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 1280, 800
        self.num_edges = 0;
        for i in range(10):
            chap_edges.append([4 * i, 4 * i + 1])
            chap_edges.append([4 * i + 1, 4 * i + 2])
            chap_edges.append([4 * i + 2, 4 * i + 3])
            chap_edges.append([4 * i + 3, 4 * i])

        for i in range(10*4):
            chap_vert.append([0, 3, 0])

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size,  DOUBLEBUF | OPENGL )
        self._running = True
        gluPerspective(45, (self.size[0] / self.size[1]), 0.1, 50.0)
        gluLookAt(self.cam_x, self.cam_y, self.cam_z, 0, 0, 0, 0, 1, 0)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

            # Camera movements
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.cam_x -= key_sens
            elif event.key == pygame.K_RIGHT:
                self.cam_x += key_sens
            elif event.key == pygame.K_UP:
                self.cam_y += key_sens
            elif event.key == pygame.K_DOWN:
                self.cam_y -= key_sens
            elif event.key == pygame.K_QUOTE:
                self.cam_z += key_sens
            elif event.key == pygame.K_SLASH:
                self.cam_z -= key_sens

            # Reload new perpective
            glLoadIdentity()
            gluPerspective(45, (self.size[0] / self.size[1]), 0.1, 50.0)
            gluLookAt(self.cam_x, self.cam_y, self.cam_z, 0, 0, 0, 0, 1, 0)

    def on_loop(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        if self.num_edges:
            self.draw_chaperone()
        if devices:
            self.draw_devices()

    def on_render(self):
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while (self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def draw_chaperone(self):
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_LINES)
        for edge in range(self.num_edges):
            vertex1 = chap_edges[edge][0]
            vertex2 = chap_edges[edge][1]
            glVertex3fv(chap_vert[vertex1])
            glVertex3fv(chap_vert[vertex2])
        glEnd()

    def draw_devices(self):
        for d in devices:
            # Set the appropriate size and color for each device type
            if d[1] == 1:
                rectangle = get_rect(0.1, 0.06, 0.06)
                glColor3f(1.0, 0.0, 0.0)    # Red
            elif d[1] == 2:
                rectangle = get_rect(0.01, 0.01, 0.1)
                glColor3f(0.0, 1.0, 0.0)    # Green
            else:
                rectangle = get_rect(0.05, 0.05, 0.01)
                glColor3f(0.0, 0.0, 1.0)    # Blue

            glPushMatrix()
            glMultMatrixf(d[0])
            glBegin(GL_LINES)
            for edge in cube_edge:
                for vertex in edge:
                    glVertex3fv(rectangle[vertex])

            # Draw line to show front face
            glVertex3f(0, 0, 0)
            glVertex3f(0, 0, -0.08)
            glEnd()
            glPopMatrix()
