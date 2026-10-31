import sys, time, random, pygame
from collections import deque
import cv2 as cv, mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

pygame.init()

# Initialize webcam and Pygame screen
VID_CAP = cv.VideoCapture(0)
window_size = (int(VID_CAP.get(cv.CAP_PROP_FRAME_WIDTH)), int(VID_CAP.get(cv.CAP_PROP_FRAME_HEIGHT)))
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Mandible Movement Practice Birdie on the Breeze")

# Load and resize bird
bird_img = pygame.image.load("/home/sec/mini_project/Priyanka_project/FlappyBird/bird_sprite.png")
bird_img = pygame.transform.scale(bird_img, (bird_img.get_width() // 6, bird_img.get_height() // 6))
bird_frame = bird_img.get_rect()
bird_frame.center = (window_size[0] // 6, window_size[1] // 2)

# Load and resize pipes
pipe_img = pygame.image.load("/home/sec/mini_project/Priyanka_project/FlappyBird/pipe_sprite_single.png")
pipe_img = pygame.transform.scale(pipe_img, (80, 300))  # reduced size
pipe_starting_template = pipe_img.get_rect()
space_between_pipes = 250
pipe_height = 300

pipe_frames = deque()

# Game logic variables
game_clock = time.time()
stage = 1
pipeSpawnTimer = 0
time_between_pipe_spawn = 40
dist_between_pipes = 500
pipe_velocity = lambda: dist_between_pipes / time_between_pipe_spawn
level = 0
score = 0
didUpdateScore = False
game_is_running = True

# Start MediaPipe face mesh
with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:

    while True:
        if not game_is_running:
            text = pygame.font.SysFont("Helvetica Bold.ttf", 64).render('Game over!', True, (99, 245, 255))
            tr = text.get_rect(center=(window_size[0] / 2, window_size[1] / 2))
            screen.blit(text, tr)
            pygame.display.update()
            pygame.time.wait(2000)
            VID_CAP.release()
            cv.destroyAllWindows()
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                VID_CAP.release()
                cv.destroyAllWindows()
                pygame.quit()
                sys.exit()

        # Get webcam frame
        ret, frame = VID_CAP.read()
        if not ret:
            print("Empty frame, continuing...")
            continue

        screen.fill((125, 220, 232))

        # Detect face landmarks
        frame.flags.writeable = False
        frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = face_mesh.process(frame_rgb)
        frame.flags.writeable = True

        # Control bird by nose tip (landmark 94)
        if results.multi_face_landmarks and len(results.multi_face_landmarks) > 0:
            marker = results.multi_face_landmarks[0].landmark[94].y
            bird_frame.centery = (marker - 0.5) * 1.5 * window_size[1] + window_size[1] / 2
            bird_frame.top = max(bird_frame.top, 0)
            bird_frame.bottom = min(bird_frame.bottom, window_size[1])

        # Mirror and display frame as background
        frame = cv.flip(frame, 1).swapaxes(0, 1)
        pygame.surfarray.blit_array(screen, frame)

        # Update pipes
        for pf in pipe_frames:
            pf[0].x -= pipe_velocity()
            pf[1].x -= pipe_velocity()

        if len(pipe_frames) > 0 and pipe_frames[0][0].right < 0:
            pipe_frames.popleft()

        screen.blit(bird_img, bird_frame)

        # Pipe collision and score detection
        checker = True
        for pf in pipe_frames:
            if pf[0].left <= bird_frame.x <= pf[0].right:
                checker = False
                if not didUpdateScore:
                    score += 1
                    didUpdateScore = True
            screen.blit(pipe_img, pf[1])
            screen.blit(pygame.transform.flip(pipe_img, 0, 1), pf[0])
        if checker:
            didUpdateScore = False

        # Display stage and score
        font = pygame.font.SysFont("Helvetica Bold.ttf", 50)
        screen.blit(font.render(f'Stage {stage}', True, (99, 245, 255)), (20, 20))
        screen.blit(font.render(f'Score: {score}', True, (99, 245, 255)), (20, 80))

        pygame.display.flip()

        # Game over check
        if any([bird_frame.colliderect(pf[0]) or bird_frame.colliderect(pf[1]) for pf in pipe_frames]):
            game_is_running = False

        # Spawn new pipes
        if pipeSpawnTimer == 0:
            top = pipe_starting_template.copy()
            max_top_y = window_size[1] - space_between_pipes - pipe_height
            top.x = window_size[0]
            top.y = random.randint(-pipe_height + 120, max_top_y)
            bottom = pipe_starting_template.copy()
            bottom.x = window_size[0]
            bottom.y = top.y + pipe_height + space_between_pipes
            pipe_frames.append([top, bottom])

        pipeSpawnTimer += 1
        if pipeSpawnTimer >= time_between_pipe_spawn:
            pipeSpawnTimer = 0

        # Stage difficulty increase
        if time.time() - game_clock >= 10:
            time_between_pipe_spawn = max(20, time_between_pipe_spawn * 5 // 6)
            stage += 1
            game_clock = time.time()
