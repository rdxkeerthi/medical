import pygame
import random
import mediapipe as mp
import cv2

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 500, 600
BASKET_WIDTH, BASKET_HEIGHT = 100, 50
EGG_WIDTH, EGG_HEIGHT = 30, 40
EGG_SPEED = 5
LIVES = 3

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Create Game Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch The Egg")
clock = pygame.time.Clock()

# Load Images
basket_img = pygame.image.load("basket.png")
basket_img = pygame.transform.scale(basket_img, (BASKET_WIDTH, BASKET_HEIGHT))
egg_img = pygame.image.load("egg.png")
egg_img = pygame.transform.scale(egg_img, (EGG_WIDTH, EGG_HEIGHT))

# Basket
basket_x = WIDTH // 2 - BASKET_WIDTH // 2
basket_y = HEIGHT - BASKET_HEIGHT - 10

# Egg
egg_x = random.randint(50, WIDTH - 50)
egg_y = 0
score = 0
lives = LIVES

# Initialize Mediapipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()
cap = cv2.VideoCapture(0)

# Game Loop
running = True
while running:
    # Read Frame from Webcam
    ret, frame = cap.read()
    if not ret:
        continue
    frame = cv2.flip(frame, 1)  # Mirror the video feed
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    # Use webcam as background
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    pygame_frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
    screen.blit(pygame_frame, (0, 0))

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            lip_left_x = face_landmarks.landmark[61].x * WIDTH
            lip_right_x = face_landmarks.landmark[291].x * WIDTH
            lip_center_x = (lip_left_x + lip_right_x) / 2

            # Move basket to extreme left or right based on lip position
            if lip_center_x < WIDTH * 0.3:
                basket_x = 0  # Move basket to left edge
            elif lip_center_x > WIDTH * 0.7:
                basket_x = WIDTH - BASKET_WIDTH  # Move basket to right edge
            else:
                basket_x += (lip_center_x - (basket_x + BASKET_WIDTH / 2)) * 0.5  # Increased sensitivity

    # Keep basket within screen bounds
    basket_x = max(0, min(WIDTH - BASKET_WIDTH, basket_x))

    # Move Egg
    egg_y += EGG_SPEED

    # Check for Catch
    if basket_x < egg_x < basket_x + BASKET_WIDTH and egg_y + EGG_HEIGHT >= basket_y:
        score += 1
        egg_x = random.randint(50, WIDTH - 50)
        egg_y = 0

    # Check for Missed Egg
    if egg_y > HEIGHT:
        lives -= 1
        egg_x = random.randint(50, WIDTH - 50)
        egg_y = 0
        if lives == 0:
            running = False

    # Draw Basket and Egg
    screen.blit(basket_img, (basket_x, basket_y))
    screen.blit(egg_img, (egg_x, egg_y))

    # Display Score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLUE)
    lives_text = font.render(f"Lives: {lives}", True, RED)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 40))

    pygame.display.update()
    clock.tick(30)

cap.release()
cv2.destroyAllWindows()
pygame.quit()
