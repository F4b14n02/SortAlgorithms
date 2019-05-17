import pygame
import time
import random
import threading

WIDTH = 1600
HEIGHT = 900

size = 1600
 
delay = 0.01

garray = []
running = False
gp = -1
gi = -1
gj = -1
glow = -1
ghigh = -1

def create_randomList(max, lenght):
    array = []
    for i in range(lenght):
        array.append(random.randint(1, max))
    return array

def qs(array, low, high):
    global gp
    global gi
    global gj
    global glow
    global ghigh

    p = array[high]
    i = low
    j = high

    while i < j:
        while array[i] <= p and i < high-1:
            i += 1
        while array[j] >= p and j > low:
            j -= 1
        if i < j:
            temp = array[i]
            array[i] = array[j]
            array[j] = temp
            garray = array
            gp = p
            gi = i
            gj = j
            glow = low
            ghigh = high
            time.sleep(delay)
            if not running:
                return array
    temp = array[i]
    if temp > p:
        array[i] = p
        array[high] = temp
        garray = array
        gp = p
        gi = i
        gj = j
        glow = low
        ghigh = high
        time.sleep(delay)
        if not running:
            return array
    if low < i:
        array = qs(array, low, i)
    if i+1 < high:
        array = qs(array, i+1, high)
    return array

def quick_sort(array):
    global running
    global gp
    global gi
    global gj
    global glow
    global ghigh


    running = True
    array = qs(array, 0, len(array) - 1)
    running = False

    gp = -1
    gi = -1
    gj = -1
    glow = -1
    ghigh = -1

    return array 

def draw_rect(n, height, width, color, screen):
    x = n * width
    y = HEIGHT
    pygame.draw.rect(screen, color, [x, y, width, -height], 0)

def start():
    quick_sort(garray)

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.font.init()
font = pygame.font.SysFont('Times New Roman', 100)

run = True

while run:
    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False
            running = False
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running = False
                time.sleep(delay * 2)
                garray = create_randomList(size, size)
                threading.Thread(target=start).start()

    screen.fill((0, 0, 0))
    
    if (len(garray) == 0):
        textsurface = font.render('press [space]', True, (255, 255, 255))
        screen.blit(textsurface,(WIDTH / 2 - 250, HEIGHT / 2 - 100))

    for i in range(len(garray)):
        if i == gi or i == gj:
            draw_rect(i, (HEIGHT/size)*garray[i], WIDTH / size, (255, 0, 0), screen)
        elif i > gi and i < gj:
            draw_rect(i, (HEIGHT/size)*garray[i], WIDTH / size, (0, 200, 255), screen)
        else:
            draw_rect(i, (HEIGHT/size)*garray[i], WIDTH / size, (255, 255, 255), screen)

    if gp != -1:
        y = (HEIGHT / size) * (gp + 1)
        x = (WIDTH / size) * glow
        dx = (WIDTH / size) * (ghigh + 1)
        if (dx - x > 0):
            rect = pygame.Surface((dx - x, WIDTH / size), pygame.SRCALPHA, 32)
            rect.fill((0, 255, 0, 128))
            screen.blit(rect, (x, HEIGHT - y))

    pygame.display.update()