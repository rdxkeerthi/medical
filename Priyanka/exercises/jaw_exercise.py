import sys, time, random, pygame
from collections import deque
import cv2 as cv, mediapipe as mp

# Initialize Mediapipe for face tracking
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
pygame.init()

# Initialize webcam
VID_CAP = cv.VideoCapture(0)  # Change to 3 if external camera
window_size = (int(VID_CAP.get(cv.CAP_PROP_FRAME_WIDTH)), int(VID_CAP.get(cv.CAP_PROP_FRAME_HEIGHT))) 
screen = pygame.display.set_mode(window_size)

# Load and scale bird sprite
bird_img = pygame.image.load("bird_sprite.png")
bird_img = pygame.transform.scale(bird_img, (bird_img.get_width() // 6, bird_img.get_height() // 6))
bird_frame = bird_img.get_rect()
bird_frame.center = (window_size[0] // 6, window_size[1] // 2)

# Load and scale pipe sprite (50% smaller)
pipe_img = pygame.image.load("pipe_sprite_single.png")
pipe_img = pygame.transform.scale(pipe_img, (pipe_img.get_width() // 2, pipe_img.get_height() // 2))  # Scale pipe to 50%
pipe_starting_template = pipe_img.get_rect()
space_between_pipes = 200  # Adjust spacing to fit smaller pipes

# Game variables
pipe_frames = deque()
game_clock = time.time()
stage = 1
pipeSpawnTimer = 0
time_between_pipe_spawn = 40
dist_between_pipes = 500
pipe_velocity = lambda: dist_between_pipes / time_between_pipe_spawn
score = 0
didUpdateScore = False
game_is_running = True

with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:
    
    while True:
        # Check if game is running
        if not game_is_running:
            text = pygame.font.SysFont("Helvetica Bold.ttf", 64).render('Game over!', True, (99, 245, 255))
            tr = text.get_rect()
            tr.center = (window_size[0]/2, window_size[1]/2)
            screen.blit(text, tr)
            pygame.display.update()
            pygame.time.wait(2000)
            VID_CAP.release()
            cv.destroyAllWindows()
            pygame.quit()
            sys.exit()

        # Check if user quits
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                VID_CAP.release()
                cv.destroyAllWindows()
                pygame.quit()
                sys.exit()

        # Capture webcam frame
        ret, frame = VID_CAP.read()
        if not ret:
            print("Empty frame, continuing...")
            continue

        # Clear screen
        screen.fill((125, 220, 232))

        # Process face mesh
        frame.flags.writeable = False
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = face_mesh.process(frame)
        frame.flags.writeable = True

        # Use jaw movement to move bird
        if results.multi_face_landmarks and len(results.multi_face_landmarks) > 0:
            landmarks = results.multi_face_landmarks[0].landmark
            jaw_distance = landmarks[152].y - landmarks[13].y  # Distance between chin (152) and upper lip (13)

            # Normalize movement: opening mouth moves bird UP
            bird_frame.centery = (jaw_distance - 0.05) * -500 + window_size[1] / 2

            # Keep bird within screen bounds
            if bird_frame.top < 0: 
                bird_frame.y = 0
            if bird_frame.bottom > window_size[1]: 
                bird_frame.y = window_size[1] - bird_frame.height

        # Mirror frame for display
        frame = cv.flip(frame, 1).swapaxes(0, 1)

        # Update pipes position
        for pf in pipe_frames:
            pf[0].x -= pipe_velocity()
            pf[1].x -= pipe_velocity()

        if len(pipe_frames) > 0 and pipe_frames[0][0].right < 0:
            pipe_frames.popleft()

        # Update screen with video feed
        pygame.surfarray.blit_array(screen, frame)
        screen.blit(bird_img, bird_frame)
        checker = True

        for pf in pipe_frames:
            # Check if bird goes through the pipe
            if pf[0].left <= bird_frame.x <= pf[0].right:
                checker = False
                if not didUpdateScore:
                    score += 1
                    didUpdateScore = True

            # Draw pipes
            screen.blit(pipe_img, pf[1])
            screen.blit(pygame.transform.flip(pipe_img, 0, 1), pf[0])

        if checker:
            didUpdateScore = False

        # Draw score & stage
        font = pygame.font.SysFont("Helvetica Bold.ttf", 50)
        text = font.render(f'Stage {stage}', True, (99, 245, 255))
        screen.blit(text, (50, 20))
        text = font.render(f'Score: {score}', True, (99, 245, 255))
        screen.blit(text, (50, 80))

        # Refresh screen
        pygame.display.flip()

        # Collision detection
        if any([bird_frame.colliderect(pf[0]) or bird_frame.colliderect(pf[1]) for pf in pipe_frames]):
            game_is_running = False

        # ✅ FIXED PIPE SPAWNING RANGE
        min_pipe_y = max(-pipe_img.get_height(), window_size[1] - 900)
        max_pipe_y = max(-pipe_img.get_height() + 100, window_size[1] - 800)

        if pipeSpawnTimer == 0:
            top = pipe_starting_template.copy()
            top.x, top.y = window_size[0], random.randint(min_pipe_y, max_pipe_y)
            bottom = pipe_starting_template.copy()
            bottom.x, bottom.y = window_size[0], top.y + pipe_img.get_height() + space_between_pipes
            pipe_frames.append([top, bottom])

        # Update pipe spawn timer
        pipeSpawnTimer += 1
        if pipeSpawnTimer >= time_between_pipe_spawn: 
            pipeSpawnTimer = 0

        # Increase difficulty over time
        if time.time() - game_clock >= 10:
            time_between_pipe_spawn *= 5 / 6
            stage += 1
            game_clock = time.time()
