import pygame

class Feedback:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font(None, 36)

    def display_message(self, screen, message, position, color=(0, 0, 0)):
        text = self.font.render(message, True, color)
        screen.blit(text, position)