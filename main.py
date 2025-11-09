import pygame
import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
pygame.init()

WIDTH, HEIGTH = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption("Juego Reciclaje")
clock = pygame.time.Clock()
running = True
mode = 'menu'

menu_image = pygame.transform.scale(pygame.image.load('Menu.png'),
                                    (150, 40))
options_image = pygame.transform.scale(pygame.image.load('Options.png'),
                                       (150, 40))
play_image = pygame.transform.scale(pygame.image.load('Play.png'),
                                    (150, 40))
lern_image = pygame.transform.scale(pygame.image.load('Lern.png'),
                                    (150, 80))
controls_image = pygame.transform.scale(pygame.image.load('Controls.png'),
                                        (150, 80))
canecaV_image = pygame.transform.scale(pygame.image.load('CanecaV.png'),
                                       (200, 400))
canecaB_image = pygame.transform.scale(pygame.image.load('CanecaB.png'),
                                       (200, 400))
canecaN_image = pygame.transform.scale(pygame.image.load('CanecaN.png'),
                                       (220, 400))
BasuraN_image = pygame.transform.scale(pygame.image.load('BasuraN.png'),
                                       (127, 227))
BasuraB_image = pygame.transform.scale(pygame.image.load('BasuraB.png'),
                                       (120, 237))
BasuraV_image = pygame.transform.scale(pygame.image.load('BasuraV.png'),
                                       (116, 246))
notaN_image = pygame.transform.scale(pygame.image.load('NotaN.png'),
                                     (300, 300))
notaB_image = pygame.transform.scale(pygame.image.load('NotaB.png'),
                                     (300, 300))
notaV_image = pygame.transform.scale(pygame.image.load('NotaV.png'),
                                     (300, 300))

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

        dedos_data = []  # [(x, y, dedos_arriba), ...]

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

            for (x, y, dedos_arriba) in dedos_data:
                if dedos_arriba == 1 and is_finger_over_button(x,
                                                               y,
                                                               menu2_rect):
                    mode = 'menu'

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
