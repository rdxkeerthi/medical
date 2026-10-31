import pygame
import cv2
from utils.mediapipe_tracker import MediaPipeTracker
from utils.feedback import Feedback

class TongueExercise:
    def __init__(self):
        self.tracker = MediaPipeTracker()
        self.feedback = Feedback()
        self.maze_pos = [400, 300]
        self.maze_speed = 5
        self.window_width = 800
        self.window_height = 600

    def initialize_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        pygame.display.set_caption("Tongue Exercise Game")
        self.maze_image = pygame.image.load('assets/images/maze.png')
        self.background = pygame.image.load('assets/images/maze_background.png')
        self.background = pygame.transform.scale(self.background, (self.window_width, self.window_height))

    def initialize_webcam(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            exit(1)

    def update_maze_position(self, tongue):
        # Map the tongue position (normalized between 0 and 1) to the maze speed
        dx = (tongue.x - 0.5) * self.maze_speed
        dy = (tongue.y - 0.5) * self.maze_speed

        # Update the maze position but constrain it within the screen bounds
        self.maze_pos[0] += int(dx)
        self.maze_pos[1] += int(dy)

        # Prevent the maze from going off-screen
        self.maze_pos[0] = max(0, min(self.maze_pos[0], self.window_width - self.maze_image.get_width()))
        self.maze_pos[1] = max(0, min(self.maze_pos[1], self.window_height - self.maze_image.get_height()))

    def display_feedback(self):
        self.feedback.display_message(self.screen, "Use your tongue to navigate the maze!", (10, 10))

    def run(self):
        self.initialize_pygame()
        self.initialize_webcam()
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            success, frame = self.cap.read()
            if not success:
                continue

            results = self.tracker.process_frame(frame)
            tongue = self.tracker.get_landmark(results, 13)

            if tongue:
                self.update_maze_position(tongue)

            # Draw the background and maze
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.maze_image, self.maze_pos)

            # Display the feedback message
            self.display_feedback()

            # Update the screen and maintain framerate
            pygame.display.flip()
            clock.tick(30)

            # Show the webcam feed
            cv2.imshow('Webcam', frame)
            if cv2.waitKey(1) & 0xFF == 27:  # Exit if 'Esc' key is pressed
                break

        self.cap.release()
        pygame.quit()
        cv2.destroyAllWindows()

