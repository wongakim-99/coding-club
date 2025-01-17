import pygame
import random

#pygmme초기화(pygmme initialization)
pygame.init()

#창 크기 설정(Set window size)
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 900

#색깔 설정(Color settings)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

#창 설정(Window settings)
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Brick Breaker")
clock = pygame.time.Clock()

#텍스트 객체 만들기(Creating a text object)
system_font = pygame.font.SysFont('verdanai', 30)

#Setting bricks
BRICK_WIDTH = 75
BRICK_HEIGHT = 24
BRICK_MARGIN_X = 5
BRICK_MARGIN_Y = 5
COLUMN_COUNT = 6
ROW_COUNT = 5

#벽돌 전체 배열의 가로 너비 계산 (Calculating the width of the entire brick array)
total_bricks_width = (BRICK_WIDTH + BRICK_MARGIN_X) * COLUMN_COUNT - BRICK_MARGIN_X

#벽돌의 시작 위치 계산(Calculate the starting position of the bricks)
start_x = (WINDOW_WIDTH - total_bricks_width) // 2

#벽돌을 리스트로 관리(Manage bricks as a list)
bricks = []

#벽돌을 리스트를 이용하여 생성(Create bricks using a list)
for column_index in range(COLUMN_COUNT):
    for row_index in range(ROW_COUNT):
        brick_x = start_x + column_index * (BRICK_WIDTH + BRICK_MARGIN_X)
        brick_y = 35 + row_index * (BRICK_HEIGHT + BRICK_MARGIN_Y)
        brick = pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT)
        bricks.append(brick)

#쥐의 방향을 바꿔주기 위한 설정 변수(Setting variables to change the direction of the mouse)
mouse_dx = 5
mouse_dy = 5

#바나나 이미지 붙이고 설정(Paste and set the banana image)
banana_image = pygame.image.load("banana.png")
banana_rect = banana_image.get_rect()
banana_rect.centerx = (WINDOW_WIDTH // 2)
banana_rect.bottom = 20

#쥐 이미지 붙이고 설정(Paste the mouse image and set it)
mouse_image = pygame.image.load("mouse.png")
mouse_rect = mouse_image.get_rect()
mouse_rect.centerx = (WINDOW_WIDTH // 2)
mouse_rect.bottom = 500

#코끼리 이미지 붙이고 설정(Paste the elephant image and set it)
elephant_image = pygame.image.load("elephant.png")
elephant_rect = elephant_image.get_rect()
elephant_rect.centerx = (WINDOW_WIDTH // 2)
elephant_rect.bottom = 700

#게임 시간 제한과 점수 설정(Set game time limits and scores)
TIME_LIMIT = 60
start_time = pygame.time.get_ticks()
score = 0

#pygame.mixer 초기화(Initializing pygame.mixer)
pygame.mixer.init()
game_over_sound = pygame.mixer.Sound("gameover.wav")
game_over_sound.set_volume(0.1)

#게임이 동작하는 동안 이벤트(Events while the game is running)
winner = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #키보드가 눌러졌을 때 발생하는 이벤트 지정(Set events when a key is pressed)
    keys = pygame.key.get_pressed()

    #방향키에 대한 키보드 이벤트(Keyboard events for direction keys)
    #코끼리가 화면 밖으로 나가지 않도록 제한(Limit the elephant to stay within the screen)
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and elephant_rect.left > 0:
        elephant_rect.x -= 5
    if (keys[pygame.K_RIGHT]
            or keys[pygame.K_d]) and elephant_rect.right < WINDOW_WIDTH:
        elephant_rect.x += 5

    #바탕화면, 그림을 나타냄(Displays the desktop, picture)
    display_surface.fill((255, 255, 255))

    #쥐가 자동으로 움직임(The mouse moves automatically)
    prev_x, prev_y = mouse_rect.x, mouse_rect.y   
    mouse_rect.x = mouse_rect.x + mouse_dx
    mouse_rect.y = mouse_rect.y + mouse_dy

    #쥐의 움직임을 바꿔주는 설정(Settings that change the mouse's movement)
    if mouse_rect.x > WINDOW_WIDTH or mouse_rect.x < 0:
        mouse_dx = mouse_dx * -1
    if mouse_rect.y > WINDOW_HEIGHT or mouse_rect.y < 0:
        mouse_dy = mouse_dy * -1

    #쥐가 바닥에 닿는지 확인(Make sure the mouse touches the floor)
    if mouse_rect.bottom >= WINDOW_HEIGHT:
        score -= 10  
        # 쥐의 위치를 랜덤하게 설정(Set the mouse's location randomly)
        mouse_rect.x = random.randint(0, WINDOW_WIDTH - mouse_rect.width)
        mouse_rect.y = random.randint(0, WINDOW_HEIGHT // 2)  # Randomly generated only in the top half area

        mouse_dx = random.choice([-5, 5])
        mouse_dy = random.choice([-5, 5])

    #Change the direction of the mouse when the elephant and mouse collide
    if elephant_rect.colliderect(mouse_rect):
        #충돌 방향에 따라 쥐의 위치를 조정(Adjust the mouse's position depending on the direction of the collision)
        if mouse_rect.centerx < elephant_rect.centerx:  #쥐가 코끼리의 왼쪽에서 충돌
            mouse_rect.right = elephant_rect.left
        elif mouse_rect.centerx > elephant_rect.centerx:  #쥐가 코끼리의 오른쪽에서 충돌
            mouse_rect.left = elephant_rect.right
        elif mouse_rect.centery < elephant_rect.centery:  #쥐가 코끼리의 위쪽에서 충돌
            mouse_rect.bottom = elephant_rect.top
        elif mouse_rect.centery > elephant_rect.centery:  #쥐가 코끼리의 아래쪽에서 충돌
            mouse_rect.top = elephant_rect.bottom
        
        mouse_dx = mouse_dx * -1
        mouse_dy = mouse_dy * -1

    #벽돌 그리기(Drawing bricks)
    for brick in bricks:
        pygame.draw.rect(display_surface, GREEN, brick)

    for brick in bricks:
        if mouse_rect.colliderect(brick):
            #충돌 방향 계산(Calculating collision direction)
            if prev_y + mouse_rect.height <= brick.top or prev_y >= brick.bottom:
                #위/아래에서 충돌(Collision from above/below)
                mouse_dy *= -1
            elif prev_x + mouse_rect.width <= brick.left or prev_x >= brick.right:
                #좌/우에서 충돌(Collision from left/right)
                mouse_dx *= -1

            score += 10
            bricks.remove(brick)  #충돌한 벽돌 제거(Remove the crashed bricks)
            break

    #바나나와 쥐 충돌 처리(Banana and Rat Collision Handling)
    if mouse_rect.colliderect(banana_rect):
        winner = True
        break

    #남은 시간 계산(Calculate remaining time)
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    remain_time = max(0, TIME_LIMIT - elapsed_time)
    if remain_time <= 0:
        running = False  #quit game

    #남은 시간에 대한 변수(Variable for remaining time)
    time_surface = system_font.render(f"Time: {int(remain_time)}", True, BLACK)

    #점수에 대한 변수(Variable for score)
    score_surface = system_font.render(f"Score: {score}", True, BLACK)

    display_surface.blit(time_surface, (10, 10))
    display_surface.blit(score_surface, (10, 30))
    display_surface.blit(banana_image, banana_rect)
    display_surface.blit(mouse_image, mouse_rect)
    display_surface.blit(elephant_image, elephant_rect)

    #디스플레이 업데이트(Display Update)
    pygame.display.update()

    #분당 프레임 설정(Set frames per minute)
    clock.tick(60)

#승리 처리(Winner -> When the mouse ate the banana)
if winner:
    display_surface.fill(WHITE)
    win_surface = system_font.render("Winner Winner Chicken Dinner!!", True,
                                     BLUE)
    display_surface.blit(
        win_surface,
        (WINDOW_WIDTH // 2 - win_surface.get_width() // 2, WINDOW_HEIGHT // 2))
    pygame.display.update()
    pygame.time.delay(5000)
else:
    display_surface.fill(WHITE)
    gameover_surface = system_font.render("GAME OVER", True, RED)
    display_surface.blit(
        gameover_surface,
        (WINDOW_WIDTH // 2 - gameover_surface.get_width() // 2,
         WINDOW_HEIGHT // 2))
    game_over_sound.play()
    pygame.display.update()
    pygame.time.delay(5000)

pygame.quit()
