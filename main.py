import pygame
import cv2
import mediapipe as mp
import numpy as np
import os
import random
import time

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
pygame.init()

WIDTH, HEIGTH = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption("Juego Reciclaje")
clock = pygame.time.Clock()
running = True
mode = 'menu'

menu_image = pygame.transform.scale(pygame.image.load('Imagenes/Menu.png'),
                                    (150, 40))
options_image = pygame.transform.scale(pygame.image.load('Imagenes/Options.png'),
                                       (150, 40))
play_image = pygame.transform.scale(pygame.image.load('Imagenes/Play.png'),
                                    (150, 40))
game1_image = pygame.transform.scale(pygame.image.load('Imagenes/Game1.png'),
                                     (150, 80))
game2_image = pygame.transform.scale(pygame.image.load('Imagenes/Game2.png'),
                                     (150, 80))
lern_image = pygame.transform.scale(pygame.image.load('Imagenes/Lern.png'),
                                    (150, 80))
controls_image = pygame.transform.scale(pygame.image.load('Imagenes/Controls.png'),
                                        (150, 80))
canecaV_image = pygame.transform.scale(pygame.image.load('Imagenes/CanecaV.png'),
                                       (200, 400))
canecaB_image = pygame.transform.scale(pygame.image.load('Imagenes/CanecaB.png'),
                                       (200, 400))
canecaN_image = pygame.transform.scale(pygame.image.load('Imagenes/CanecaN.png'),
                                       (220, 400))
BasuraN_image = pygame.transform.scale(pygame.image.load('Imagenes/BasuraN.png'),
                                       (127, 227))
BasuraB_image = pygame.transform.scale(pygame.image.load('Imagenes/BasuraB.png'),
                                       (120, 237))
BasuraV_image = pygame.transform.scale(pygame.image.load('Imagenes/BasuraV.png'),
                                       (116, 246))
notaN_image = pygame.transform.scale(pygame.image.load('Imagenes/NotaN.png'),
                                     (300, 300))
notaB_image = pygame.transform.scale(pygame.image.load('Imagenes/NotaB.png'),
                                     (300, 300))
notaV_image = pygame.transform.scale(pygame.image.load('Imagenes/NotaV.png'),
                                     (300, 300))
replay1_image = pygame.transform.scale(pygame.image.load('Imagenes/Replay1.png'),
                                       (150, 80))
replay2_image = pygame.transform.scale(pygame.image.load('Imagenes/Replay2.png'),
                                       (150, 80))

menu_x, menu_y = WIDTH // 2 - 75, 50
menu_rect = pygame.Rect(menu_x, menu_y, 150, 40)
options_x, options_y = WIDTH - 200, HEIGTH // 2
options_rect = pygame.Rect(options_x, options_y, 150, 40)
play_x, play_y = 50, HEIGTH // 2
play_rect = pygame.Rect(play_x, play_y, 150, 40)
lern_x, lern_y = 50, HEIGTH // 2 - 100
lern_rect = pygame.Rect(lern_x, lern_y, 150, 80)
controls_x, controls_y = WIDTH - 200, HEIGTH // 2 - 100
controls_rect = pygame.Rect(controls_x, controls_y, 150, 80)
menu2_x, menu2_y = WIDTH - 175, 25
menu2_rect = pygame.Rect(menu2_x, menu2_y, 150, 40)
canecaV_x, canecaV_y = WIDTH - 230, HEIGTH - 200
canecaV_rect = pygame.Rect(canecaV_x, canecaV_y, 200, 400)
canecaN_x, canecaN_y = 30, HEIGTH - 200
canecaN_rect = pygame.Rect(canecaN_x, canecaN_y, 220, 400)
canecaB_x, canecaB_y = WIDTH // 2 - 100, HEIGTH - 200
canecaB_rect = pygame.Rect(canecaB_x, canecaB_y, 200, 400)
nota_x, nota_y = 50, HEIGTH // 2 - 200
Basura_x, Basura_y = WIDTH - 300, HEIGTH // 2 - 150
game1_rect = pygame.Rect(lern_x, lern_y, 150, 80)
game2_rect = pygame.Rect(controls_x, controls_y, 150, 80)
replay_x, replay_y = WIDTH // 2 - 75, HEIGTH // 2 - 120
replay1_rect = pygame.Rect(replay_x, replay_y, 150, 80)
replay2_rect = pygame.Rect(replay_x, replay_y, 150, 80)

# La configuración de la camara
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 60)


def fingers_up(landmarks):
    tips = [8, 12, 16, 20]
    fingers = []
    for tip in tips:
        fingers.append(landmarks[tip].y < landmarks[tip - 2].y)
    return sum(fingers)


def is_finger_over_button(finger_x, finger_y, rect):
    return rect.collidepoint(finger_x, finger_y)


class Basura:
    def __init__(self, tipo, imagen):
        self.tipo = tipo
        self.img = imagen
        self.rect = self.img.get_rect(topleft=(random.randint(100,
                                                              WIDTH - 200),
                                               random.randint(100,
                                                              HEIGTH - 300)))
        self.drag = False

    def draw(self):
        screen.blit(self.img, self.rect)


def cargar_basuritas_imagenes():
    basuras_verdes = [pygame.image.load(f'Imagenes/basuritaV{i}.png') for i in range(1, 4) if os.path.exists(f'Imagenes/basuritaV{i}.png')]
    basuras_blancas = [pygame.image.load(f'Imagenes/basuritaB{i}.png') for i in range(1, 5) if os.path.exists(f'Imagenes/basuritaB{i}.png')]
    basuras_negras = [pygame.image.load(f'Imagenes/basuritaN{i}.png') for i in range(1, 5) if os.path.exists(f'Imagenes/basuritaN{i}.png')]

    basuras_verdes = [pygame.transform.scale(img, (100, 100)) for img in basuras_verdes]
    basuras_blancas = [pygame.transform.scale(img, (100, 100)) for img in basuras_blancas]
    basuras_negras = [pygame.transform.scale(img, (100, 100)) for img in basuras_negras]

    return {
        'verde': basuras_verdes,
        'blanco': basuras_blancas,
        'negro': basuras_negras
        }


def crear_basuritas(imagenes):
    tipos = ["verde", "blanco", "negro"]
    basuras = []
    for _ in range(10):
        tipo = random.choice(tipos)
        if imagenes[tipo]:
            img = random.choice(imagenes[tipo])
            basuras.append(Basura(tipo, img))
    return basuras


imagenes_basuras = cargar_basuritas_imagenes()
basuras = crear_basuritas(imagenes_basuras)
puntuacion_correctas = 0
puntuacion_incorrectas = 0
juego1_finalizado = 'false'


class BasuraCae:
    def __init__(self, tipo, imagen):
        self.tipo = tipo
        self.img = imagen
        self.x = random.randint(50, WIDTH - 150)
        self.y = -100
        self.speed = random.randint(3, 7)
        self.rect = self.img.get_rect(topleft=(self.x, self.y))

    def update(self):
        self.y += self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        screen.blit(self.img, self.rect)


game2_etapa = 'elegir'
caneca_elegida = None
game2_basuras = []
game2_caught = 0
game2_caught_t = 0
game2_start_time = 0

with mp_hands.Hands(min_detection_confidence=0.5,
                    min_tracking_confidence=0.5,
                    max_num_hands=2) as hands:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        dedos_data = []

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(rgb_frame,
                                       hand_landmarks,
                                       mp_hands.HAND_CONNECTIONS)
                lm = hand_landmarks.landmark
                d_x = int(lm[8].x * WIDTH)
                d_y = int(lm[8].y * HEIGTH)
                dedos = fingers_up(lm)
                dedos_data.append((d_x, d_y, dedos))

        rgb_frame = cv2.flip(rgb_frame, 1)
        frame_resized = cv2.resize(rgb_frame,
                                   (WIDTH, HEIGTH),
                                   interpolation=cv2.INTER_LINEAR)
        frame_surface = pygame.surfarray.make_surface(np.rot90(frame_resized))
        screen.blit(frame_surface, (0, 0))

        if mode == 'menu':
            screen.blit(menu_image, (menu_x, menu_y))
            screen.blit(options_image, (options_x, options_y))
            screen.blit(play_image, (play_x, play_y))

            for (x, y, dedos_arriba) in dedos_data:
                if dedos_arriba == 1:
                    if is_finger_over_button(x, y, play_rect):
                        mode = 'play'
                    elif is_finger_over_button(x, y, options_rect):
                        mode = 'options'

        elif mode == 'play':
            screen.blit(menu_image, (menu2_x, menu2_y))
            screen.blit(play_image, (menu_x, menu_y))
            screen.blit(game1_image, (lern_x, lern_y))
            screen.blit(game2_image, (controls_x, controls_y))

            for (x, y, dedos_arriba) in dedos_data:
                if dedos_arriba == 1 and is_finger_over_button(x,
                                                               y,
                                                               menu2_rect):
                    mode = 'menu'
                                                                 
            for (x, y, dedos_arriba) in dedos_data:
                if dedos_arriba == 1 and is_finger_over_button(x,
                                                               y,
                                                               game1_rect):
                    mode = 'game1'

            for (x, y, dedos_arriba) in dedos_data:
                if dedos_arriba == 1 and is_finger_over_button(x,
                                                               y,
                                                               game2_rect):
                    mode = 'game2'

        elif mode == 'game1':
            font = pygame.font.Font(None, 60)
            text = font.render("¡Clasifica la basura!",
                               True,
                               (255, 255, 255))
            screen.blit(menu_image, (menu2_x, menu2_y))
            screen.blit(game1_image, (menu_x, menu_y))
            screen.blit(canecaN_image, canecaN_rect)
            screen.blit(canecaB_image, canecaB_rect)
            screen.blit(canecaV_image, canecaV_rect)
            screen.blit(text, (200, HEIGTH - 60))

            if juego1_finalizado == 'false':
                for basura in basuras:
                    basura.draw()

                for (x, y, dedos_arriba) in dedos_data:
                    if dedos_arriba == 2:
                        for basura in basuras:
                            if basura.rect.collidepoint(x, y):
                                basura.rect.center = (x, y)

                    elif dedos_arriba == 1:
                        for basura in basuras[:]:
                            if (basura.rect.colliderect(canecaV_rect) or
                                basura.rect.colliderect(canecaB_rect) or
                                basura.rect.colliderect(canecaN_rect)):

                                if basura.tipo == 'verde' and basura.rect.colliderect(canecaV_rect):
                                    puntuacion_correctas += 1
                                elif basura.tipo == 'blanco' and basura.rect.colliderect(canecaB_rect):
                                    puntuacion_correctas += 1
                                elif basura.tipo == 'negro' and basura.rect.colliderect(canecaN_rect):
                                    puntuacion_correctas += 1
                                else:
                                    puntuacion_incorrectas += 1
                                basuras.remove(basura)

                if not basuras:
                    juego1_finalizado = 'true'
            elif juego1_finalizado == 'true':
                font = pygame.font.Font(None, 60)
                text = font.render(f"Correctas: {puntuacion_correctas} Incorrectas: {puntuacion_incorrectas}",
                                   True,
                                   (255, 255, 255))
                screen.blit(text, (100, HEIGTH // 2 - 30))
                screen.blit(replay1_image, (replay_x, replay_y))

                for (x, y, dedos_arriba) in dedos_data:
                    if dedos_arriba == 1 and is_finger_over_button(x,
                                                                   y,
                                                                   replay1_rect):
                        puntuacion_correctas = 0
                        puntuacion_incorrectas = 0
                        imagenes_basuras = cargar_basuritas_imagenes()
                        basuras = crear_basuritas(imagenes_basuras)
                        juego1_finalizado = 'false'

            for (x, y, dedos_arriba) in dedos_data:
                if dedos_arriba == 1 and is_finger_over_button(x,
                                                               y,
                                                               menu2_rect):
                    mode = 'menu'

        elif mode == 'game2':
            screen.blit(menu_image, (menu2_x, menu2_y))
            screen.blit(game2_image, (menu_x, menu_y))

            for (x, y, dedos_arriba) in dedos_data:
                if dedos_arriba == 1 and is_finger_over_button(x,
                                                               y,
                                                               menu2_rect):
                    mode = 'menu'

            if game2_etapa == 'elegir':
                font = pygame.font.Font(None, 50)
                txt = font.render("Elige tu caneca usando 1 dedo",
                                  True,
                                  (255, 255, 255))
                screen.blit(txt, (150, 120))

                screen.blit(canecaN_image, canecaN_rect)
                screen.blit(canecaB_image, canecaB_rect)
                screen.blit(canecaV_image, canecaV_rect)

                for (x, y, dedos_arriba) in dedos_data:
                    if dedos_arriba == 1:
                        if canecaN_rect.collidepoint(x, y):
                            mini = pygame.transform.scale(canecaN_image, 
                                                          (canecaN_image.get_width()//2,
                                                           canecaN_image.get_height()//2))
                            caneca_elegida = ('negro', mini)
                            game2_etapa = 'explicar'

                        elif canecaB_rect.collidepoint(x, y):
                            mini = pygame.transform.scale(canecaB_image,
                                                          (canecaB_image.get_width()//2,
                                                           canecaB_image.get_height()//2))
                            caneca_elegida = ('blanco', mini)
                            game2_etapa = 'explicar'

                        elif canecaV_rect.collidepoint(x, y):
                            mini = pygame.transform.scale(canecaV_image,
                                                          (canecaV_image.get_width()//2,
                                                           canecaV_image.get_height()//2))
                            caneca_elegida = ('verde', mini)
                            game2_etapa = 'explicar'

            elif game2_etapa == 'explicar':
                font = pygame.font.Font(None, 40)
                lines = [
                    "Lluvia de basura!",
                    "Mueve tu caneca con la mano abierta.",
                    "Atrapá SOLO la basura de tu color!",
                    "Dura 30 segundos.",
                    "Toca con 2 dedo para comenzar."
                ]
                for i, txt in enumerate(lines):
                    t = font.render(txt, True, (255, 255, 255))
                    screen.blit(t, (150, 120 + i*50))

                screen.blit(caneca_elegida[1], (WIDTH//2 - 100, 350))

                for (x, y, dedos_arriba) in dedos_data:
                    if dedos_arriba == 2:
                        game2_basuras = []
                        game2_caught = 0
                        game2_caught_t = 0
                        game2_start_time = time.time()
                        game2_etapa = 'jugando'

            elif game2_etapa == 'jugando':
                tipo_caneca, img_caneca = caneca_elegida

                caneca_rect = img_caneca.get_rect(center=(WIDTH // 2, HEIGTH - 120))

                for (x, y, dedos_arriba) in dedos_data:
                    if dedos_arriba == 4:
                        caneca_rect.center = (int(x), int(y))

                screen.blit(img_caneca, caneca_rect)

                if random.random() < 0.03:
                    tipo = random.choice(["verde", "blanco", "negro"])
                    img = random.choice(imagenes_basuras[tipo])
                    game2_basuras.append(BasuraCae(tipo, img))

                for basura in game2_basuras[:]:
                    basura.update()
                    basura.draw()

                    if basura.rect.colliderect(caneca_rect):
                        if basura.tipo == tipo_caneca:
                            game2_caught += 1
                        else:
                            game2_caught_t += 1
                        game2_basuras.remove(basura)

                    if basura.y > HEIGTH:
                        game2_basuras.remove(basura)

                tiempo = int(30 - (time.time() - game2_start_time))
                font = pygame.font.Font(None, 60)
                t = font.render(f"{tiempo}", True, (255, 255, 255))
                screen.blit(t, (20, 20))

                if tiempo <= 0:
                    game2_etapa = 'final'

            elif game2_etapa == 'final':
                font = pygame.font.Font(None, 60)
                t = font.render(f"Atrapadas correctas: {game2_caught}",
                                True,
                                (255, 255, 255))
                t2 = font.render(f"Atrapadas incorrectas: {game2_caught_t}",
                                 True,
                                 (255, 255, 255))
                screen.blit(t, (200, HEIGTH // 2 - 30))
                screen.blit(t2, (200, HEIGTH // 2 + 90))


                screen.blit(replay2_image, (replay_x, replay_y))

                for (x, y, dedos_arriba) in dedos_data:
                    if dedos_arriba == 1 and is_finger_over_button(x,
                                                                   y,
                                                                   replay2_rect):
                        game2_etapa = 'elegir'
                        caneca_elegida = None
                        game2_basuras = []
                        game2_caught = 0
                        game2_caught_t = 0

        elif mode == 'options':
            screen.blit(menu_image, (menu2_x, menu2_y))
            screen.blit(options_image, (menu_x, menu_y))
            screen.blit(lern_image, (lern_x, lern_y))
            screen.blit(controls_image, (controls_x, controls_y))

            for (x, y, dedos_arriba) in dedos_data:
                if dedos_arriba == 1 and is_finger_over_button(x,
                                                               y,
                                                               menu2_rect):
                    mode = 'menu'

            for (x, y, dedos_arriba) in dedos_data:
                if dedos_arriba == 1 and is_finger_over_button(x,
                                                               y,
                                                               lern_rect):
                    mode = 'lern'

            for (x, y, dedos_arriba) in dedos_data:
                if dedos_arriba == 1 and is_finger_over_button(x,
                                                               y,
                                                               controls_rect):
                    mode = 'controls'

        elif mode == 'lern':
            screen.blit(menu_image, (menu2_x, menu2_y))
            screen.blit(lern_image, (menu_x, menu_y))
            screen.blit(canecaN_image, (canecaN_x, canecaN_y))
            screen.blit(canecaB_image, (canecaB_x, canecaB_y))
            screen.blit(canecaV_image, (canecaV_x, canecaV_y))

            for (x, y, dedos_arriba) in dedos_data:
                if dedos_arriba == 1 and is_finger_over_button(x,
                                                               y,
                                                               menu2_rect):
                    mode = 'menu'

            for (x, y, dedos_arriba) in dedos_data:
                if dedos_arriba == 1 and is_finger_over_button(x,
                                                               y,
                                                               canecaV_rect):
                    screen.blit(BasuraV_image, (Basura_x, Basura_y))
                    screen.blit(notaV_image, (nota_x, nota_y))

            for (x, y, dedos_arriba) in dedos_data:
                if dedos_arriba == 1 and is_finger_over_button(x,
                                                               y,
                                                               canecaB_rect):
                    screen.blit(BasuraB_image, (Basura_x, Basura_y))
                    screen.blit(notaB_image, (nota_x, nota_y))

            for (x, y, dedos_arriba) in dedos_data:
                if dedos_arriba == 1 and is_finger_over_button(x,
                                                               y,
                                                               canecaN_rect):
                    screen.blit(BasuraN_image, (Basura_x, Basura_y))
                    screen.blit(notaN_image, (nota_x, nota_y))
                                                                 
        elif mode == 'controls':
            screen.blit(menu_image, (menu2_x, menu2_y))
            screen.blit(controls_image, (menu_x, menu_y))

            for (x, y, dedos_arriba) in dedos_data:
                if dedos_arriba == 1 and is_finger_over_button(x,
                                                               y,
                                                               menu2_rect):
                    mode = 'menu'

        pygame.display.flip()
        clock.tick(60)

cap.release()
cv2.destroyAllWindows()
pygame.quit()
