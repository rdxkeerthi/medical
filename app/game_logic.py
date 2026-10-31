import pygame

class SwallowingGame:
    def __init__(self, model, tracker):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Swallowing Function Training")
        self.clock = pygame.time.Clock()
        self.running = True
        self.model = model
        self.tracker = tracker

    def start(self):
        print("Game started.")
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((255, 255, 255))  # White background

            # Get facial landmarks
            landmarks = self.tracker.get_landmarks()
            if landmarks:
                prediction = self.model.predict(landmarks)
                print(f"Prediction: {prediction}")

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()