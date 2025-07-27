import pygame
import sys
import random
import cv2
import mediapipe as mp
import threading

# 
# hand tracking setup
# 

fng1 = None
fng2 = None
to_check_thread = True

def fng_checkUsing_thread():
    global fng1, fng2, to_check_thread

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    mp_draw = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)

    while to_check_thread:
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)
        h, w, _ = frame.shape

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw full landmarks
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # index finger tip
                x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                fng1 = x
                fng2 = y

                # draw green line in the tip of index finger
                cx, cy = int(x * w), int(y * h)
                cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)

        cv2.imshow("Hand Tracking", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            to_check_thread = False
            break

    cap.release()
    cv2.destroyAllWindows()


# Start the hand tracking in a separate thread
threading.Thread(target=fng_checkUsing_thread, daemon=True).start()


# Pygame Snake Game


pygame.init()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
food_colors = [red, blue, white]

# Screen
window_width = 800
window_height = 600
gameDisplay = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('ICSG')

clock = pygame.time.Clock()
FPS = 8
blockSize = 20
font = pygame.font.SysFont("comicsansms", 25, bold=True)

# Load background
try:
    background = pygame.image.load("C:\\Users\\NITIN PANDEY\\OneDrive\\Desktop\\python project\\pygame\\background.jpg")
    background = pygame.transform.scale(background, (window_width, window_height))
except:
    background = None

# Draw Snake with pseudo 3D effect
def draw_snake(snake_body):
    for index, segment in enumerate(snake_body):
        base_color = yellow
        shadow_color = (max(0, base_color[0]-50), max(0, base_color[1]-50), max(0, base_color[2]-50))
        highlight_color = (min(255, base_color[0]+50), min(255, base_color[1]+50), min(255, base_color[2]+50))

        pygame.draw.rect(gameDisplay, base_color, [segment[0], segment[1], blockSize, blockSize])
        pygame.draw.line(gameDisplay, shadow_color,
                         (segment[0], segment[1]+blockSize),
                         (segment[0]+blockSize, segment[1]+blockSize), 2)
        pygame.draw.line(gameDisplay, highlight_color,
                         (segment[0], segment[1]),
                         (segment[0]+blockSize, segment[1]), 2)

        # Draw head features
        if index == len(snake_body) - 1:
            pygame.draw.circle(gameDisplay, black, (segment[0] + 5, segment[1] + 5), 3)
            pygame.draw.circle(gameDisplay, black, (segment[0] + 15, segment[1] + 5), 3)
            pygame.draw.circle(gameDisplay, black, (segment[0] + 10, segment[1] + 15), 2)

def message_to_screen(msg, color, position):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, position)
#   __main body hai___   
####$$$$$$$#####
# Game Loop

def gameLoop():
    global to_check_thread
    gameExit = False
    gameOver = False

    lead_x = window_width // 2
    lead_y = window_height // 2
    change_x = 0
    change_y = 0

    snake_body = []
    snake_length = 1
    score = 0
    foods_eaten = 0

    randomAppleX = random.randrange(0, window_width - blockSize, blockSize)
    randomAppleY = random.randrange(0, window_height - blockSize, blockSize)
    apple_color = random.choice(food_colors)

    last_hand_x = None
    last_hand_y = None

    # food blink karna
    food_visible = True
    last_blink_time = pygame.time.get_ticks()
    blink_interval = 500  # millisecond for food blinking

    global FPS

    while not gameExit and to_check_thread:
        while gameOver:
            gameDisplay.fill(white)
            message_to_screen(f"Game Over! Score: {score}", red, [window_width / 3, window_height / 3])
            message_to_screen("Press C to Play Again or Q to Quit", black, [window_width / 3, window_height / 2])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                    to_check_thread = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                        to_check_thread = False
                    if event.key == pygame.K_c:
                        FPS = 8
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                to_check_thread = False

        # =================
        # hand control logic
        # =================
        if fng1 is not None and fng2 is not None:
            if last_hand_x is not None and last_hand_y is not None:
                dx = fng1 - last_hand_x
                dy = fng2 - last_hand_y
                threshold = 0.02

                if abs(dx) > abs(dy):
                    if dx > threshold:
                        change_x = blockSize
                        change_y = 0
                    elif dx < -threshold:
                        change_x = -blockSize
                        change_y = 0
                else:
                    if dy > threshold:
                        change_y = blockSize
                        change_x = 0
                    elif dy < -threshold:
                        change_y = -blockSize
                        change_x = 0

            last_hand_x = fng1
            last_hand_y = fng2

        # =================
        # for move snake
        # =================
        if lead_x >= window_width or lead_x < 0 or lead_y >= window_height or lead_y < 0:
            gameOver = True

        lead_x += change_x
        lead_y += change_y

        # draw background
        if background:
            gameDisplay.blit(background, (0, 0))
        else:
            gameDisplay.fill(black)

        # blinking food 2
        current_time = pygame.time.get_ticks()
        if current_time - last_blink_time > blink_interval:
            food_visible = not food_visible
            last_blink_time = current_time

        if food_visible:
            pygame.draw.rect(gameDisplay, apple_color, [randomAppleX, randomAppleY, blockSize, blockSize])

        # real-time scorecard banner
        pygame.draw.rect(gameDisplay, white, [0, 0, window_width, 40])
        pygame.draw.line(gameDisplay, black, (0, 40), (window_width, 40), 2)
        message_to_screen(f"Score: {score}  |  Speed: {FPS}", black, [10, 5])

        # snake body update
        snake_head = [lead_x, lead_y]
        snake_body.append(snake_head)
        if len(snake_body) > snake_length:
            del snake_body[0]

        for segment in snake_body[:-1]:
            if segment == snake_head:
                gameOver = True

        draw_snake(snake_body)
        pygame.display.update()

        # check food collision
        if lead_x in range(randomAppleX, randomAppleX + blockSize) and lead_y in range(randomAppleY, randomAppleY + blockSize):
            randomAppleX = random.randrange(0, window_width - blockSize, blockSize)
            randomAppleY = random.randrange(0, window_height - blockSize, blockSize)
            apple_color = random.choice(food_colors)
            snake_length += 1
            score += 10
            foods_eaten += 1
            if foods_eaten % 5 == 0:
                FPS += 2

        clock.tick(FPS)

    pygame.quit()
    sys.exit()

# 
# start the game
# 
gameLoop()
to_check_thread = False
