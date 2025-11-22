import pygame
import cv2
import mediapipe as mp
import numpy as np
import os
import random
import time

# Inicialización de MediaPipe Hands (detección de manos)
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Inicializamos pygame
pygame.init()

# Dimensiones de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego Reciclaje")
clock = pygame.time.Clock()
running = True
mode = 'introduccion1'  # Modo inicial del juego

# Fuente
font = pygame.font.SysFont(None, 40)

# CARGA DE TODAS LAS IMÁGENES
# Todas las imágenes del menú y juego se cargan y escalan aquí

menu_image = pygame.transform.scale(pygame.image.load('Imagenes/Menu.png'), (150, 40))
options_image = pygame.transform.scale(pygame.image.load('Imagenes/Options.png'), (150, 40))
play_image = pygame.transform.scale(pygame.image.load('Imagenes/Play.png'), (150, 40))
game1_image = pygame.transform.scale(pygame.image.load('Imagenes/Game1.png'), (150, 80))
game2_image = pygame.transform.scale(pygame.image.load('Imagenes/Game2.png'), (150, 80))
lern_image = pygame.transform.scale(pygame.image.load('Imagenes/Lern.png'), (150, 80))
controls_image = pygame.transform.scale(pygame.image.load('Imagenes/Controls.png'), (150, 80))

# Imágenes de canecas y basuras
canecaV_image = pygame.transform.scale(pygame.image.load('Imagenes/CanecaV.png'), (200, 400))
canecaB_image = pygame.transform.scale(pygame.image.load('Imagenes/CanecaB.png'), (200, 400))
canecaN_image = pygame.transform.scale(pygame.image.load('Imagenes/CanecaN.png'), (220, 400))

BasuraN_image = pygame.transform.scale(pygame.image.load('Imagenes/BasuraN.png'), (127, 227))
BasuraB_image = pygame.transform.scale(pygame.image.load('Imagenes/BasuraB.png'), (120, 237))
BasuraV_image = pygame.transform.scale(pygame.image.load('Imagenes/BasuraV.png'), (116, 246))

# Notas explicativas
notaN_image = pygame.transform.scale(pygame.image.load('Imagenes/NotaN.png'), (300, 300))
notaB_image = pygame.transform.scale(pygame.image.load('Imagenes/NotaB.png'), (300, 300))
notaV_image = pygame.transform.scale(pygame.image.load('Imagenes/NotaV.png'), (300, 300))

# Replay
replay1_image = pygame.transform.scale(pygame.image.load('Imagenes/Replay1.png'), (150, 80))
replay2_image = pygame.transform.scale(pygame.image.load('Imagenes/Replay2.png'), (150, 80))

# Práctica de introducción
papelito_image = pygame.transform.scale(pygame.image.load('Imagenes/papel.webp'), (50, 50))
caneca_practica_image = pygame.transform.scale(pygame.image.load('Imagenes/CanecaN.png'), (200, 400))
palma_image = pygame.transform.scale(pygame.image.load('Imagenes/palmaM.png'), (300, 320))
manoApunta = pygame.transform.scale(pygame.image.load('Imagenes/manoApunta.png'), (300, 320))

# Definición de posiciones de botones

menu_x, menu_y = WIDTH // 2 - 75, 50
menu_rect = pygame.Rect(menu_x, menu_y, 150, 40)

options_x, options_y = WIDTH - 200, HEIGHT // 2
options_rect = pygame.Rect(options_x, options_y, 150, 40)

play_x, play_y = 50, HEIGHT // 2
play_rect = pygame.Rect(play_x, play_y, 150, 40)

lern_x, lern_y = 50, HEIGHT // 2 - 100
lern_rect = pygame.Rect(lern_x, lern_y, 150, 80)

controls_x, controls_y = WIDTH - 200, HEIGHT // 2 - 100
controls_rect = pygame.Rect(controls_x, controls_y, 150, 80)

menu2_x, menu2_y = WIDTH - 175, 25
menu2_rect = pygame.Rect(menu2_x, menu2_y, 150, 40)

# Posiciones de canecas
canecaV_x, canecaV_y = WIDTH - 230, HEIGHT - 200
canecaV_rect = pygame.Rect(canecaV_x, canecaV_y, 200, 400)

canecaN_x, canecaN_y = 30, HEIGHT - 200
canecaN_rect = pygame.Rect(canecaN_x, canecaN_y, 220, 400)

canecaB_x, canecaB_y = WIDTH // 2 - 100, HEIGHT - 200
canecaB_rect = pygame.Rect(canecaB_x, canecaB_y, 200, 400)

nota_x, nota_y = 50, HEIGHT // 2 - 200
Basura_x, Basura_y = WIDTH - 300, HEIGHT // 2 - 150

game1_rect = pygame.Rect(lern_x, lern_y, 150, 80)
game2_rect = pygame.Rect(controls_x, controls_y, 150, 80)

replay_x, replay_y = WIDTH // 2 - 75, HEIGHT // 2 - 120
replay1_rect = pygame.Rect(replay_x, replay_y, 150, 80)
replay2_rect = pygame.Rect(replay_x, replay_y, 150, 80)

# Elementos práctica introducción
papelito_x, papelito_y = WIDTH // 2, HEIGHT // 2
papelito_rect = pygame.Rect(papelito_x, papelito_y, 50, 50)

caneca_practica_x, caneca_practica_y = 100, HEIGHT - 200
caneca_practica_rect = pygame.Rect(caneca_practica_x, caneca_practica_y, 200, 400)

menu_intro_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 - 20, 150, 40)

# Configuración de la cámara

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 60)


# Funciones de detección

def fingers_up(landmarks):
    """
    Cuenta cuántos dedos están levantados comparando la punta del dedo con la articulación anterior.
    """
    tips = [8, 12, 16, 20]  # Índices de puntas de dedos
    fingers = []
    for tip in tips:
        fingers.append(landmarks[tip].y < landmarks[tip - 2].y)
    return sum(fingers)


def is_finger_over_button(finger_x, finger_y, rect):
    """Retorna True si el dedo está sobre un botón."""
    return rect.collidepoint(finger_x, finger_y)


# Clases

class Basura:
    """Basura arrastrable para el juego 1."""
    def __init__(self, tipo, imagen):
        self.tipo = tipo
        self.img = imagen
        self.rect = self.img.get_rect(
            topleft=(random.randint(100, WIDTH - 200),
                     random.randint(100, HEIGHT - 300))
        )

    def draw(self):
        screen.blit(self.img, self.rect)


def cargar_basuritas_imagenes():
    """
    Carga basuritas pequeñas de cada color si existen en la carpeta.
    """
    basuras_verdes = [
        pygame.image.load(f'Imagenes/basuritaV{i}.png')
        for i in range(1, 4)
        if os.path.exists(f'Imagenes/basuritaV{i}.png')
    ]

    basuras_blancas = [
        pygame.image.load(f'Imagenes/basuritaB{i}.png')
        for i in range(1, 5)
        if os.path.exists(f'Imagenes/basuritaB{i}.png')
    ]

    basuras_negras = [
        pygame.image.load(f'Imagenes/basuritaN{i}.png')
        for i in range(1, 5)
        if os.path.exists(f'Imagenes/basuritaN{i}.png')
    ]

    # Escalamos todo a tamaño uniforme
    basuras_verdes = [
        pygame.transform.scale(img, (100, 100)) for img in basuras_verdes
        ]
    basuras_blancas = [
        pygame.transform.scale(img, (100, 100)) for img in basuras_blancas
        ]
    basuras_negras = [
        pygame.transform.scale(img, (100, 100)) for img in basuras_negras
        ]

    return {
        'verde': basuras_verdes,
        'blanco': basuras_blancas,
        'negro': basuras_negras
    }


def crear_basuritas(imagenes):
    """Crea una lista de basuras aleatorias para el juego 1."""
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

agarrando = False


class BasuraCae:
    """Basura que cae desde arriba en el juego 2."""
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


# Variables juego 2
game2_etapa = 'elegir'
caneca_elegida = None
game2_basuras = []
game2_caught = 0
game2_caught_t = 0
game2_start_time = 0

# BUCLE PRINCIPAL

with mp_hands.Hands(min_detection_confidence=0.5,
                    min_tracking_confidence=0.5,
                    max_num_hands=2) as hands:
    while running:

        # EVENTOS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Captura de la cámara
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # Cámara en modo espejo
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        dedos_data = []  # Lista con datos de cada mano detectada

        # Procesamiento de manos
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(rgb_frame,
                                       hand_landmarks,
                                       mp_hands.HAND_CONNECTIONS)

                lm = hand_landmarks.landmark

                # Coordenadas del dedo índice (normalizado → pixel)
                d_x = int(lm[8].x * WIDTH)
                d_y = int(lm[8].y * HEIGHT)

                dedos = fingers_up(lm)  # Cuenta dedos levantados

                dedos_data.append((d_x, d_y, dedos))

        # Convertimos la imagen a superficie de pygame
        rgb_frame = cv2.flip(rgb_frame, 1)
        frame_resized = cv2.resize(rgb_frame, (WIDTH, HEIGHT))
        frame_surface = pygame.surfarray.make_surface(np.rot90(frame_resized))
        screen.blit(frame_surface, (0, 0))

        # MODOS DEL JUEGO

        # MENÚ
        if mode == 'menu':
            screen.blit(menu_image, (menu_x, menu_y))
            screen.blit(options_image, (options_x, options_y))
            screen.blit(play_image, (play_x, play_y))

            # Deteción de dedo índice sobre botones
            for (x, y, dedos_arriba) in dedos_data:
                if dedos_arriba == 1:  # 1 dedo para seleccionar
                    if is_finger_over_button(x, y, play_rect):
                        mode = 'play'
                    elif is_finger_over_button(x, y, options_rect):
                        mode = 'options'

        # PLAY / SELECCIÓN DE JUEGOS
        elif mode == 'play':
            screen.blit(menu_image, (menu2_x, menu2_y))
            screen.blit(play_image, (menu_x, menu_y))
            screen.blit(game1_image, (lern_x, lern_y))
            screen.blit(game2_image, (controls_x, controls_y))

            # Botón volver
            for (x, y, dedos_arriba) in dedos_data:
                if dedos_arriba == 1 and is_finger_over_button(x, y, menu2_rect):
                    mode = 'menu'

            # Selección de game1
            for (x, y, dedos_arriba) in dedos_data:
                if dedos_arriba == 1 and is_finger_over_button(x, y, game1_rect):
                    mode = 'game1'

            # Selección game2
            for (x, y, dedos_arriba) in dedos_data:
                if dedos_arriba == 1 and is_finger_over_button(x, y, game2_rect):
                    mode = 'game2'

        # JUEGO 1: CLASIFICAR BASURA
        elif mode == 'game1':
            font = pygame.font.Font(None, 60)
            text = font.render("¡Clasifica la basura!", True, (255, 255, 255))

            screen.blit(menu_image, (menu2_x, menu2_y))
            screen.blit(game1_image, (menu_x, menu_y))

            # Dibujar canecas
            screen.blit(canecaN_image, canecaN_rect)
            screen.blit(canecaB_image, canecaB_rect)
            screen.blit(canecaV_image, canecaV_rect)
            screen.blit(text, (200, HEIGHT - 60))

            if juego1_finalizado == 'false':

                # Dibujar basuras
                for basura in basuras:
                    basura.draw()

                # Detección dedos
                for (x, y, dedos_arriba) in dedos_data:

                    # Mover basura si hay 2 dedos
                    if dedos_arriba == 2:
                        for basura in basuras:
                            if basura.rect.collidepoint(x, y):
                                basura.rect.center = (x, y)

                    # 1 dedo para soltar basura y clasificar
                    elif dedos_arriba == 1:
                        for basura in basuras[:]:

                            if (basura.rect.colliderect(canecaV_rect) or
                                basura.rect.colliderect(canecaB_rect) or
                                basura.rect.colliderect(canecaN_rect)):

                                # Evaluar si es correcta
                                if basura.tipo == 'verde' and basura.rect.colliderect(canecaV_rect):
                                    puntuacion_correctas += 1
                                elif basura.tipo == 'blanco' and basura.rect.colliderect(canecaB_rect):
                                    puntuacion_correctas += 1
                                elif basura.tipo == 'negro' and basura.rect.colliderect(canecaN_rect):
                                    puntuacion_correctas += 1
                                else:
                                    puntuacion_incorrectas += 1

                                basuras.remove(basura)

                # Si ya no hay basuras → final del juego
                if not basuras:
                    juego1_finalizado = 'true'

            else:
                # Pantalla final
                font = pygame.font.Font(None, 60)
                text = font.render(f"Correctas: {puntuacion_correctas}  Incorrectas: {puntuacion_incorrectas}",
                                   True, (255, 255, 255))
                screen.blit(text, (100, HEIGHT // 2 - 30))
                screen.blit(replay1_image, (replay_x, replay_y))

                # Reiniciar
                for (x, y, dedos_arriba) in dedos_data:
                    if dedos_arriba == 1 and is_finger_over_button(x, y, replay1_rect):
                        puntuacion_correctas = 0
                        puntuacion_incorrectas = 0
                        basuras = crear_basuritas(cargar_basuritas_imagenes())
                        juego1_finalizado = 'false'

            # Botón volver
            for (x, y, dedos_arriba) in dedos_data:
                if dedos_arriba == 1 and is_finger_over_button(x, y, menu2_rect):
                    mode = 'menu'

        # JUEGO 2
        elif mode == 'game2':

            screen.blit(menu_image, (menu2_x, menu2_y))
            screen.blit(game2_image, (menu_x, menu_y))

            # Botón volver
            for (x, y, dedos_arriba) in dedos_data:
                if dedos_arriba == 1 and is_finger_over_button(x, y, menu2_rect):
                    mode = 'menu'

            # Etapa 1: elegir caneca
            if game2_etapa == 'elegir':
                font = pygame.font.Font(None, 50)
                screen.blit(font.render("Elige tu caneca usando 1 dedo",
                                        True, (255, 255, 255)), (150, 120))

                screen.blit(canecaN_image, canecaN_rect)
                screen.blit(canecaB_image, canecaB_rect)
                screen.blit(canecaV_image, canecaV_rect)

                for (x, y, dedos_arriba) in dedos_data:
                    if dedos_arriba == 1:

                        # Selección de caneca negra
                        if canecaN_rect.collidepoint(x, y):
                            caneca_elegida = ('negro',
                                              pygame.transform.scale(canecaN_image, (
                                                  canecaN_image.get_width() // 2,
                                                  canecaN_image.get_height() // 2)))
                            game2_etapa = 'explicar'

                        # Selección de caneca blanca
                        elif canecaB_rect.collidepoint(x, y):
                            caneca_elegida = ('blanco',
                                              pygame.transform.scale(canecaB_image, (
                                                  canecaB_image.get_width() // 2,
                                                  canecaB_image.get_height() // 2)))
                            game2_etapa = 'explicar'

                        # Selección verde
                        elif canecaV_rect.collidepoint(x, y):
                            caneca_elegida = ('verde',
                                              pygame.transform.scale(canecaV_image, (
                                                  canecaV_image.get_width() // 2,
                                                  canecaV_image.get_height() // 2)))
                            game2_etapa = 'explicar'

            # Etapa 2: Explicación
            elif game2_etapa == 'explicar':
                font = pygame.font.Font(None, 40)
                lines = [
                    "Lluvia de basura!",
                    "Mueve tu caneca con la mano abierta.",
                    "Atrapa SOLO la basura de tu color.",
                    "Dura 30 segundos.",
                    "Toca con 2 dedos para comenzar."
                ]

                for i, txt in enumerate(lines):
                    screen.blit(font.render(txt, True, (255, 255, 255)), (150, 120 + i*50))

                screen.blit(caneca_elegida[1], (WIDTH // 2 - 100, 350))

                # 2 dedos → iniciar juego
                for (x, y, dedos_arriba) in dedos_data:
                    if dedos_arriba == 2:
                        game2_basuras = []
                        game2_caught = 0
                        game2_caught_t = 0
                        game2_start_time = time.time()
                        game2_etapa = 'jugando'

            # Etapa 3: Jugando
            elif game2_etapa == 'jugando':

                tipo_caneca, img_caneca = caneca_elegida

                # Posición inicial de la caneca
                caneca_rect = img_caneca.get_rect(
                    center=(WIDTH // 2, HEIGHT - 120)
                )

                # Mover caneca con la mano abierta (4 dedos arriba)
                for (x, y, dedos_arriba) in dedos_data:
                    if dedos_arriba == 4:
                        caneca_rect.center = (int(x), int(y))

                screen.blit(img_caneca, caneca_rect)

                # Generar basura aleatoria
                if random.random() < 0.03:
                    tipo = random.choice(["verde", "blanco", "negro"])
                    img = random.choice(imagenes_basuras[tipo])
                    game2_basuras.append(BasuraCae(tipo, img))

                # Actualizar basuras
                for basura in game2_basuras[:]:
                    basura.update()
                    basura.draw()

                    # Colisión con caneca
                    if basura.rect.colliderect(caneca_rect):
                        if basura.tipo == tipo_caneca:
                            game2_caught += 1
                        else:
                            game2_caught_t += 1
                        game2_basuras.remove(basura)

                    # Si cae al piso → eliminar
                    if basura.y > HEIGHT:
                        game2_basuras.remove(basura)

                # Timer
                tiempo = int(30 - (time.time() - game2_start_time))
                t = pygame.font.Font(None, 60).render(f"{tiempo}", True, (255, 255, 255))
                screen.blit(t, (20, 20))

                if tiempo <= 0:
                    game2_etapa = 'final'

            # Etapa 4: Final
            elif game2_etapa == 'final':
                font = pygame.font.Font(None, 60)

                screen.blit(font.render(f"Atrapadas correctas: {game2_caught}",
                                        True, (255, 255, 255)),
                            (200, HEIGHT // 2 - 30))

                screen.blit(font.render(f"Atrapadas incorrectas: {game2_caught_t}",
                                        True, (255, 255, 255)),
                            (200, HEIGHT // 2 + 90))

                screen.blit(replay2_image, (replay_x, replay_y))

                # Reiniciar juego 2
                for (x, y, dedos_arriba) in dedos_data:
                    if dedos_arriba == 1 and is_finger_over_button(x, y, replay2_rect):
                        game2_etapa = 'elegir'
                        caneca_elegida = None
                        game2_basuras = []
                        game2_caught = 0
                        game2_caught_t = 0

        # OPTIONS
        elif mode == 'options':
            screen.blit(menu_image, (menu2_x, menu2_y))
            screen.blit(options_image, (menu_x, menu_y))
            screen.blit(lern_image, (lern_x, lern_y))
            screen.blit(controls_image, (controls_x, controls_y))

            # Volver
            for (x, y, dedos_arriba) in dedos_data:
                if dedos_arriba == 1 and is_finger_over_button(x, y, menu2_rect):
                    mode = 'menu'

            # Ir a aprendizajes
            for (x, y, dedos_arriba) in dedos_data:
                if dedos_arriba == 1 and is_finger_over_button(x, y, lern_rect):
                    mode = 'lern'

            # Ir a controles
            for (x, y, dedos_arriba) in dedos_data:
                if dedos_arriba == 1 and is_finger_over_button(x, y, controls_rect):
                    mode = 'introduccion1'

        # SECCIÓN LERN
        elif mode == 'lern':
            screen.blit(menu_image, (menu2_x, menu2_y))
            screen.blit(lern_image, (menu_x, menu_y))

            # Mostrar canecas
            screen.blit(canecaN_image, (canecaN_x, canecaN_y))
            screen.blit(canecaB_image, (canecaB_x, canecaB_y))
            screen.blit(canecaV_image, (canecaV_x, canecaV_y))

            # Volver
            for (x, y, dedos_arriba) in dedos_data:
                if dedos_arriba == 1 and is_finger_over_button(x, y, menu2_rect):
                    mode = 'menu'

            # Mostrar info de cada caneca
            for (x, y, dedos_arriba) in dedos_data:
                if dedos_arriba == 1:

                    if canecaV_rect.collidepoint(x, y):
                        screen.blit(BasuraV_image, (Basura_x, Basura_y))
                        screen.blit(notaV_image, (nota_x, nota_y))

                    if canecaB_rect.collidepoint(x, y):
                        screen.blit(BasuraB_image, (Basura_x, Basura_y))
                        screen.blit(notaB_image, (nota_x, nota_y))

                    if canecaN_rect.collidepoint(x, y):
                        screen.blit(BasuraN_image, (Basura_x, Basura_y))
                        screen.blit(notaN_image, (nota_x, nota_y))

        # INTRODUCCIÓN 1
        elif mode == 'introduccion1':
            font = pygame.font.SysFont(None, 40)

            screen.blit(palma_image, (WIDTH // 2 - 300, HEIGHT // 2))
            screen.blit(font.render("Levanta la palma para continuar",
                                    True, (255, 255, 255)), (100, 50))

            # Palma = 4 dedos arriba
            for (x, y, dedos_arriba) in dedos_data:
                if dedos_arriba == 4:
                    mode = 'introduccion2'
                    pygame.time.delay(300)

        # INTRODUCCIÓN 2
        elif mode == 'introduccion2':
            screen.blit(menu_image, (WIDTH // 2 - 75, HEIGHT // 2 - 20))
            screen.blit(manoApunta, (WIDTH // 2 - 300, HEIGHT // 2))

            text = font.render("¡Perfecto! Apunta a un botón para seleccionar",
                               True, (255, 255, 255))
            screen.blit(text, (100, 50))

            # 1 dedo → seleccionar botón
            for (x, y, dedos_arriba) in dedos_data:
                if dedos_arriba == 1 and is_finger_over_button(x, y, menu_intro_rect):
                    mode = 'introduccion3'
                    pygame.time.delay(300)

        # INTRODUCCIÓN 3
        elif mode == 'introduccion3':

            screen.blit(menu_image, (menu_x, menu_y))
            text = font.render("¡Practica! Mueve el papel a la caneca usando dos dedos",
                               True, (255, 255, 255))
            screen.blit(text, (25, 100))

            screen.blit(caneca_practica_image, (caneca_practica_x, caneca_practica_y))
            screen.blit(papelito_image, (papelito_rect.x, papelito_rect.y))

            # Control del papelito
            agarrando_actual = False

            for (x, y, dedos_arriba) in dedos_data:
                if dedos_arriba == 2 and papelito_rect.collidepoint(x, y):
                    agarrando_actual = True
                    papelito_rect.x = x - papelito_rect.width // 2
                    papelito_rect.y = y - papelito_rect.height // 2

            # Si lo suelta dentro de la caneca
            if agarrando_actual and papelito_rect.colliderect(caneca_practica_rect):
                mode = 'menu'
                papelito_rect.x, papelito_rect.y = WIDTH // 2, HEIGHT // 2

            agarrando = agarrando_actual

        # ACTUALIZAR PANTALLA
        pygame.display.flip()
        clock.tick(60)

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
pygame.quit()
