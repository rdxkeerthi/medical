import cv2
import mediapipe as mp
import numpy as np
import threading
import queue
import pygame
from main import runGame
from character import Character

mp_face_mesh = mp.solutions.face_mesh

class TongueController:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True, min_detection_confidence=0.8, min_tracking_confidence=0.8)
        self.direction_queue = queue.Queue()
        self.running = True
        self.prev_x = None
        self.prev_y = None
        
    def get_tongue_direction(self, landmarks, image_shape):
        tongue_tip_idx = 14  # Adjusted for better detection
        tongue_tip = landmarks[tongue_tip_idx]
        image_height, image_width = image_shape
        x, y = int(tongue_tip.x * image_width), int(tongue_tip.y * image_height)
        
        center_x, center_y = image_width // 2, image_height // 2
        threshold_x = image_width * 0.12
        threshold_y = image_height * 0.12
        
        # Movement filtering to reduce false positives
        if self.prev_x is not None and self.prev_y is not None:
            if abs(x - self.prev_x) < 8 and abs(y - self.prev_y) < 8:
                return None  # Ignore small movements
        
        self.prev_x, self.prev_y = x, y
        
        if x > center_x + threshold_x:
            return "RIGHT"
        elif x < center_x - threshold_x:
            return "LEFT"
        elif y < center_y - threshold_y:
            return "UP"
        elif y > center_y + threshold_y:
            return "DOWN"
        return None
    
    def capture_movement(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue
            
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.face_mesh.process(rgb_frame)
            
            if result.multi_face_landmarks:
                for face_landmarks in result.multi_face_landmarks:
                    direction = self.get_tongue_direction(face_landmarks.landmark, frame.shape[:2])
                    if direction:
                        self.direction_queue.put(direction)
                        print(f"Detected movement: {direction}")
            
            cv2.imshow('Tongue Control', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False
                break
        
        self.cap.release()
        cv2.destroyAllWindows()

    def get_direction(self):
        if not self.direction_queue.empty():
            return self.direction_queue.get()
        return None

def game_loop(controller):
    grid_size = 20
    side_length = 10
    mode = 0  # Adjust game mode as needed
    
    pygame.init()
    
    game_data, player1 = runGame(grid_size, side_length, mode)  # Ensure player1 is correctly extracted
    if not isinstance(player1, Character):
        print("Error: Player character not found!")
        return
    
    clock = pygame.time.Clock()
    
    while controller.running:
        direction = controller.get_direction()
        if direction:
            print(f"Moving in direction: {direction}")
            if direction == "RIGHT":
                player1.move_right()
            elif direction == "LEFT":
                player1.move_left()
            elif direction == "UP":
                player1.move_up()
            elif direction == "DOWN":
                player1.move_down()
        
        pygame.display.flip()
        clock.tick(10)  # Limit to 10 FPS to prevent excessive movement

def main():
    controller = TongueController()
    
    capture_thread = threading.Thread(target=controller.capture_movement)
    game_thread = threading.Thread(target=game_loop, args=(controller,))
    
    capture_thread.start()
    game_thread.start()
    
    capture_thread.join()
    controller.running = False
    game_thread.join()

if __name__ == "__main__":
    main()
