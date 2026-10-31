import pygame
import cv2
from utils.mediapipe_tracker import MediaPipeTracker
from utils.feedback import Feedback

class BaseExercise:
    def __init__(self, title, width=700, height=500):
        self.tracker = MediaPipeTracker()
        self.feedback = Feedback()
        self.screen_width = width
        self.screen_height = height
        self.title = title
        self.running = True
        self.cap = cv2.VideoCapture(0)
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()

    def load_background(self, image_path):
        background = pygame.image.load(image_path)
        return pygame.transform.scale(background, (self.screen_width, self.screen_height))

    def quit(self):
        self.cap.release()
        pygame.quit()
        cv2.destroyAllWindows()

    def run(self):
        raise NotImplementedError("Run method must be implemented by subclasses")