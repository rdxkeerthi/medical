from utils.mediapipe_tracker import MediaPipeTracker
from utils.feedback import Feedback
import pygame
import cv2
import random
from .base_exercise import BaseExercise

class RabbitCatchGame(BaseExercise):
    def __init__(self):
        super().__init__("Rabbit Catch Game")
        self.screen_width, self.screen_height = 800, 600  # Default screen size
        self.rabbit_pos = [self.screen_width // 2, self.screen_height - 100]  # Start at bottom center
        self.rabbit_speed = 5
        self.carrot_speed = 5
        self.rabbit_image = pygame.image.load('assets/images/rabbit.png')
        self.carrot_image = pygame.image.load('assets/images/carrot.png')
        self.background = self.load_background('assets/images/background.png')
        self.carrots = []  # List to store falling carrots
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.tracker = MediaPipeTracker()
        self.cap = cv2.VideoCapture(0)
        
    def spawn_carrot(self):
        x_pos = random.randint(50, self.screen_width - 50)
        self.carrots.append([x_pos, 0])

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            success, frame = self.cap.read()
            if not success:
                continue

            results = self.tracker.process_frame(frame)
            left_cheek = self.tracker.get_landmark(results, 234)
            right_cheek = self.tracker.get_landmark(results, 454)

            if left_cheek and right_cheek:
                if left_cheek.y < right_cheek.y:
                    self.rabbit_pos[0] -= self.rabbit_speed
                elif right_cheek.y < left_cheek.y:
                    self.rabbit_pos[0] += self.rabbit_speed
            
            self.rabbit_pos[0] = max(0, min(self.rabbit_pos[0], self.screen_width - self.rabbit_image.get_width()))

            if random.randint(1, 50) == 1:  # Randomly drop a carrot
                self.spawn_carrot()

            for carrot in self.carrots:
                carrot[1] += self.carrot_speed
            
            self.carrots = [c for c in self.carrots if c[1] < self.screen_height]

            for carrot in self.carrots[:]:
                rabbit_rect = pygame.Rect(self.rabbit_pos[0], self.rabbit_pos[1], self.rabbit_image.get_width(), self.rabbit_image.get_height())
                carrot_rect = pygame.Rect(carrot[0], carrot[1], self.carrot_image.get_width(), self.carrot_image.get_height())
                if rabbit_rect.colliderect(carrot_rect):
                    self.carrots.remove(carrot)
                    self.score += 1
            
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.rabbit_image, self.rabbit_pos)
            
            for carrot in self.carrots:
                self.screen.blit(self.carrot_image, carrot)
            
            score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))
            
            self.feedback.display_message(self.screen, "Move lips to control the rabbit!", (10, 50))
            pygame.display.flip()
            self.clock.tick(30)
            cv2.imshow('Webcam', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        self.cap.release()
        cv2.destroyAllWindows()
        self.quit()
