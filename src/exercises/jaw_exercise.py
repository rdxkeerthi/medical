# -*- coding: utf-8 -*-
import pygame
import random
import mediapipe as mp
import cv2
import numpy as np

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 640, 480
BASKET_WIDTH, BASKET_HEIGHT = 100, 50
EGG_WIDTH, EGG_HEIGHT = 30, 40
BASKET_SPEED = 30
EGG_SPEED = 6
LIVES = 3

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Create Game Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Oral Muscle Exercise game Bunny's Catching Eggs")
clock = pygame.time.Clock()

# Load Images
basket_img = pygame.image.load("/home/sec/mini_project/Priyanka_project/src/assets/images/basket.png")
basket_img = pygame.transform.scale(basket_img, (BASKET_WIDTH, BASKET_HEIGHT))

egg_img = pygame.image.load("/home/sec/mini_project/Priyanka_project/src/assets/images/egg.png")
egg_img = pygame.transform.scale(egg_img, (EGG_WIDTH, EGG_HEIGHT))

# Basket
basket_x = WIDTH // 2 - BASKET_WIDTH // 2
basket_y = HEIGHT - BASKET_HEIGHT - 10

# Egg
egg_x = random.randint(50, WIDTH - 50)
egg_y = 0
score = 0
lives = LIVES

# Mediapipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True, max_num_faces=1)
cap = cv2.VideoCapture(0)

running = True
while running:
    # Read frame from webcam
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)  # Mirror effect
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    # Set background as video frame
    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    background = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
    screen.blit(background, (0, 0))

    # Basket control using lips
    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark

        # Landmark 13 is lower lip center
        lip_x = int(landmarks[13].x * WIDTH)

        # Smooth move towards lip x
        if lip_x < basket_x + BASKET_WIDTH // 2 - 20:
            basket_x -= BASKET_SPEED
        elif lip_x > basket_x + BASKET_WIDTH // 2 + 20:
            basket_x += BASKET_SPEED

        # Limit basket inside screen
        basket_x = max(0, min(WIDTH - BASKET_WIDTH, basket_x))

    # Move Egg
    egg_y += EGG_SPEED

    # Check Catch
    if (basket_x < egg_x < basket_x + BASKET_WIDTH) and (basket_y < egg_y + EGG_HEIGHT < basket_y + BASKET_HEIGHT):
        score += 1
        egg_x = random.randint(50, WIDTH - 50)
        egg_y = 0

    # Missed Egg
    if egg_y > HEIGHT:
        lives -= 1
        egg_x = random.randint(50, WIDTH - 50)
        egg_y = 0
        if lives == 0:
            running = False

    # Draw basket & egg
    screen.blit(basket_img, (basket_x, basket_y))
    screen.blit(egg_img, (egg_x, egg_y))

    # Draw score & lives
    font = pygame.font.SysFont("Arial", 30)
    screen.blit(font.render(f"Score: {score}", True, BLUE), (10, 10))
    screen.blit(font.render(f"Lives: {lives}", True, RED), (10, 45))

    pygame.display.update()
    clock.tick(30)

cap.release()
cv2.destroyAllWindows()
pygame.quit()
