from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
import serial

#ser = serial.Serial('/dev/tty.usbserial', 38400, timeout=1)
ser = serial.Serial('COM13', 38400, timeout=1)

ax = ay = az = 0.0


def resize(width, height):
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0*width/height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def init():
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)


def drawText(position, textString):
    font = pygame.font.SysFont("Courier", 18, True)
    textSurface = font.render(
        textString, True, (255, 255, 255, 255), (0, 0, 0, 255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glRasterPos3d(*position)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(),
                 GL_RGBA, GL_UNSIGNED_BYTE, textData)


def draw():
    global rquad
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    glTranslatef(0, 0.0, -60.0)

    osd_text = "pitch: " + str("{0:.2f}".format(ay)) + \
        ", roll: " + str("{0:.2f}".format(ax))

    osd_line = osd_text + ", yaw: " + str("{0:.2f}".format(az))

    drawText((-20, -20, 1), osd_line)

    # the way I'm holding the IMU board, X and Y axis are switched
    # with respect to the OpenGL coordinate system
    # experimental
    glRotatef(az, 0.0, 1.0, 0.0)  # Yaw,   rotate around y-axis
    glRotatef(ay, 1.0, 0.0, 0.0)        # Pitch, rotate around x-axis
    glRotatef(-1*ax, 0.0, 0.0, 1.0)     # Roll,  rotate around z-axis

    octagonalVertices = ((7, 14, 0), (6.5, 14, 2.75), (5, 14, 5), (2.75, 14, 6.5), (0, 14, 7), (-2.75, 14, 6.5), (-5, 14, 5), (-6.5, 14, 2.75),   # yük köşeleri
                         (-7, 14, 0), (-6.5, 14, -2.75), (-5, 14, -5), (-2.75, 14, -6.5), (0,
                                                                                           14, -7), (2.75, 14, -6.5), (5, 14, -5), (6.5, 14, -2.75),  # yük köşeleri
                         (7, -14, 0), (6.5, -14, 2.75), (5, -14, 5), (2.75, -14, 6.5), (0, -14,
                                                                                        7), (-2.75, -14, 6.5), (-5, -14, 5), (-6.5, -14, 2.75),  # yük köşeleri
                         (-7, -14, 0), (-6.5, -14, -2.75), (-5, -14, -5), (-2.75, -14, -6.5), (0, - \
                                                                                               14, -7), (2.75, -14, -6.5), (5, -14, -5), (6.5, -14, -2.75),  # yük köşeleri
                         (1.4, 14, 0), (1.3, 14, 0.55), (1, 14, 1), (0.55, 14, 1.3), (0, 14, 1.4), (-0.55,
                                                                                                    14, 1.3), (-1, 14, 1), (-1.3, 14, 0.55),  # alt pervane kökü ayırıcı
                         (-1.4, 14, 0), (-1.3, 14, -0.55), (-1, 14, -1), (-0.55, 14, -1.3), (0, 14, - \
                                                                                             1.4), (0.55, 14, -1.3), (1, 14, -1), (1.3, 14, -0.55),  # alt pervane kökü ayırıcı
                         (1.4, 15, 0), (1.3, 15, 0.55), (1, 15, 1), (0.55, 15, 1.3), (0, 15, 1.4), (-0.55,
                                                                                                    15, 1.3), (-1, 15, 1), (-1.3, 15, 0.55),  # alt pervane kökü ayırıcı
                         (-1.4, 15, 0), (-1.3, 15, -0.55), (-1, 15, -1), (-0.55, 15, -1.3), (0, 15, - \
                                                                                             1.4), (0.55, 15, -1.3), (1, 15, -1), (1.3, 15, -0.55),  # alt pervane kökü ayırıcı
                         (6, 15, 4.5), (4.5, 15, 6), (-6, 15, -4.5), (-4.5, 15, -6), (6, 16,
                                                                                      4.5), (4.5, 16, 6), (-6, 16, -4.5), (-4.5, 16, -6),  # alt pervane kökü
                         (1.4, 16, 0), (1.3, 16, 0.55), (1, 16, 1), (0.55, 16, 1.3), (0, 16, 1.4), (-0.55,
                                                                                                    16, 1.3), (-1, 16, 1), (-1.3, 16, 0.55),  # üst pervane kökü ayırıcı
                         (-1.4, 16, 0), (-1.3, 16, -0.55), (-1, 16, -1), (-0.55, 16, -1.3), (0, 16, - \
                                                                                             1.4), (0.55, 16, -1.3), (1, 16, -1), (1.3, 16, -0.55),  # üst pervane kökü ayırıcı
                         (1.4, 17, 0), (1.3, 17, 0.55), (1, 17, 1), (0.55, 17, 1.3), (0, 17, 1.4), (-0.55,
                                                                                                    17, 1.3), (-1, 17, 1), (-1.3, 17, 0.55),  # üst pervane kökü ayırıcı
                         (-1.4, 17, 0), (-1.3, 17, -0.55), (-1, 17, -1), (-0.55, 17, -1.3), (0, 17, - \
                                                                                             1.4), (0.55, 17, -1.3), (1, 17, -1), (1.3, 17, -0.55),  # üst pervane kökü ayırıcı
                         (-4.5, 17, 6), (-6, 17, 4.5), (4.5, 17, -6), (6, 17, -4.5), (-4.5, 18,
                                                                                      6), (-6, 18, 4.5), (4.5, 18, -6), (6, 18, -4.5),  # üst pervane kökü
                         (16, 15, 14.5), (14.5, 15, 16), (16, 16, 14.5), (14.5, 16, 16), (-16,
                                                                                          15, -14.5), (-14.5, 15, -16), (-16, 16, -14.5), (-14.5, 16, -16),
                         (-14.5, 17, 16), (-16, 17, 14.5), (-14.5, 18, 16), (-16, 18, 14.5), (14.5, 17, -16), (16, 17, -14.5), (14.5, 18, -16), (16, 18, -14.5))

    polygons = ((0, 1, 17, 16), (1, 2, 18, 17), (2, 3, 19, 18), (3, 4, 20, 19), (4, 5, 21, 20), (5, 6, 22, 21), (6, 7, 23, 22), (7, 8, 24, 23),  # yük kenarları
                (8, 9, 25, 24), (9, 10, 26, 25), (10, 11, 27, 26), (11, 12, 28, 27), (12, 13,
                                                                                      29, 28), (13, 14, 30, 29), (14, 15, 31, 30), (15, 0, 16, 31),  # yük kenarları
                (0, 1, 33, 32), (1, 2, 34, 33), (2, 3, 35, 34), (3, 4, 36, 35), (4, 5,
                                                                                 37, 36), (5, 6, 38, 37), (6, 7, 39, 38), (7, 8, 40, 39),  # yük kenarları
                (8, 9, 41, 40), (9, 10, 42, 41), (10, 11, 43, 42), (11, 12, 44, 43), (12, 13,
                                                                                      45, 44), (13, 14, 46, 45), (14, 15, 47, 46), (15, 0, 32, 47),   # yük kenarları
                (16, 17, 24, 25), (17, 18, 25, 26), (18, 19, 26, 27), (19, 20, 27, 28), (20, 21,
                                                                                         28, 29), (21, 22, 29, 30), (22, 23, 30, 31), (23, 24, 31, 16),  # yük kenarları
                (32, 33, 49, 48), (33, 34, 50, 49), (34, 35, 51, 50), (35, 36, 52, 51), (36, 37, 53,
                                                                                         52), (37, 38, 54, 53), (38, 39, 55, 54), (39, 40, 56, 55),  # alt pervane kökü ayırıcı
                (40, 41, 57, 56), (41, 42, 58, 57), (42, 43, 59, 58), (43, 44, 60, 59), (44, 45, 61,
                                                                                         60), (45, 46, 62, 61), (46, 47, 63, 62), (47, 32, 48, 63),  # alt pervane kökü ayırıcı
                (64, 65, 54, 62), (65, 66, 58, 50), (66, 67, 62, 54), (67, 64, 50, 58), (64, 65,
                                                                                         69, 68), (65, 66, 70, 69), (66, 67, 71, 70), (67, 64, 68, 71),  # alt pervane kökü
                (68, 69, 78, 86), (69, 70, 82, 74), (70, 71,
                                                     86, 78), (71, 68, 74, 82),  # alt pervane kökü
                (72, 73, 89, 88), (73, 74, 90, 89), (74, 75, 91, 90), (75, 76, 92, 91), (76, 77, 93,
                                                                                         92), (77, 78, 94, 93), (78, 79, 95, 94), (79, 80, 96, 95),  # üst pervane kökü ayırıcı
                (80, 81, 97, 96), (81, 82, 98, 97), (82, 83, 99, 98), (83, 84, 100, 99), (84, 85, 101,
                                                                                          100), (85, 86, 102, 101), (86, 87, 103, 102), (87, 72, 88, 103),  # üst pervane kökü ayırıcı
                (104, 105, 98, 90), (105, 106, 102, 94), (106, 107, 90, 98), (107, 104, 94, 102), (104, 105, 109,
                                                                                                   108), (105, 106, 110, 109), (106, 107, 111, 110), (107, 104, 108, 111), (108, 109, 110, 111),
                (112, 113, 65, 64), (114, 115, 69, 68), (112, 113,
                                                         115, 114), (112, 114, 68, 64), (113, 115, 69, 65),
                (116, 117, 67, 66), (118, 119, 71, 70), (116, 117,
                                                         119, 118), (116, 118, 70, 66), (117, 119, 71, 67),
                (120, 121, 105, 104), (122, 123, 109, 108), (120, 121,
                                                             123, 122), (120, 122, 108, 104), (121, 123, 109, 105),
                (124, 125, 107, 106), (126, 127, 111, 110), (124, 125, 127, 126), (124, 126, 110, 106), (125, 127, 111, 107))

    glColor4f(1, 0, 0, 0)
    glBegin(GL_QUADS)
    i = 0
    for polygon in polygons:
        if i > 40 and i < 57:
            glColor4f(1, 1, 0, 0)
        elif i > 56 and i < 69:
            glColor4f(0, 0, 1, 1)
        elif i > 68 and i < 85:
            glColor4f(1, 1, 0, 0)
        elif i > 84 and i < 94:
            glColor4f(0, 0, 1, 1)
        elif i > 93:
            glColor4f(1, 1, 1, 0)
        else:
            glColor4f(1, 0, 0, 0)
        i = i+1
        for octagonalVertex in polygon:
            glVertex3fv(octagonalVertices[octagonalVertex])
    glEnd()
    i = 0


def read_data():
    global ax, ay, az
    ax = ay = az = 0.0
    line_done = 0

    # request data by sending a dot
    ser.write(b".")  # * encode string to bytes
    # while not line_done:
    line = ser.readline()
    angles = line.split(b", ")
    if len(angles) == 3:
        ax = float(angles[0])
        ay = float(angles[1])
        az = float(angles[2])
        line_done = 1


def main():
    video_flags = OPENGL | DOUBLEBUF
    pygame.init()
    screen = pygame.display.set_mode((640, 480), video_flags)
    pygame.display.set_caption("Gyro Simulation")
    resize(640, 480)
    init()
    frames = 0
    ticks = pygame.time.get_ticks()
    while 1:
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()  # * quit pygame properly
            break

        read_data()
        draw()

        pygame.display.flip()
        frames = frames+1

    ser.close()


if __name__ == '__main__':
    main()
