#Setup
import pygame
import random
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()


#Game
block_size = 20
head_x = 300
head_y = 200
normal_speed = 10
boost_speed = 15
game_speed = normal_speed
blue_apple_time = 0
blue_x = -100
blue_y = -100

game_state = "START"

title_font = pygame.font.SysFont("times new roman", 40)
instruction_font = pygame.font.SysFont("times new roman", 20)

#obstacles = []

def create_obstacles():
    global obstacles
    obstacles = []
    for i in range(5):
        pos = get_random_position()
        while pos == [head_x, head_y] or pos in snake_body:
            pos = get_random_position()
        obstacles.append(pos)

def get_random_position():
    x = random.randrange(0, 800 - block_size, block_size)
    y = random.randrange(0, 600 - block_size, block_size)
    return [x, y]

def spawn_blue_bonus():
    global blue_x, blue_y
    blue_x, blue_y = get_random_position()
    while [blue_x, blue_y] in snake_body or [blue_x, blue_y] in obstacles or [blue_x, blue_y] == [food_x, food_y]:
        blue_x, blue_y = get_random_position()

def reset_game():
    global head_x, head_y, x_change, y_change, snake_body, snake_length, snake_speed, score
    head_x = 300
    head_y = 200
    x_change = 0
    y_change = 0
    snake_body = []
    snake_length = 1
    snake_speed = 10
    score = 0


x_change = 0
y_change = 0
score = 0

food_x = random.randrange(0, 800 - block_size, block_size)
food_y = random.randrange(0, 600 - block_size, block_size)

snake_body = [[head_x, head_y]]
snake_length = 1

obstacles = []

for i in range(5):
    new_obstacle = get_random_position()
    while new_obstacle == [head_x, head_y]:
        new_obstacle = get_random_position()
    obstacles.append(new_obstacle)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == "START":
                if event.key == pygame.K_SPACE:
                    game_state = "PLAYING"
                    x_change = block_size
                    y_change = 0
            elif game_state == "DEAD":
                if event.key == pygame.K_SPACE:
                    reset_game()
                    game_state = "START"
            if event.key == pygame.K_LEFT:
                x_change = -block_size
                y_change = 0
            elif event.key == pygame.K_RIGHT:
                x_change = block_size
                y_change = 0
            elif event.key == pygame.K_UP:
                y_change = -block_size
                x_change = 0
            elif event.key == pygame.K_DOWN:
                y_change = block_size
                x_change = 0

    head_x += x_change
    head_y += y_change

    if head_x < 0 or head_x >= 800 or head_y < 0 or head_y >= 600:
        game_state = "DEAD"

    if head_x == food_x and head_y == food_y:
        snake_length += 1
        score += 1
        food_x, food_y = get_random_position()
        while [food_x, food_y] in snake_body or [food_x, food_y] in obstacles:
            food_x, food_y = get_random_position()

        if blue_x == -100 and blue_y == -100 and random.random() < 0.05:
            spawn_blue_bonus()

    if blue_x != -100 and blue_y != -100 and head_x == blue_x and head_y == blue_y:
        blue_apple_time = pygame.time.get_ticks() + 10000
        blue_x = -100
        blue_y = -100
        game_speed = boost_speed

    if blue_apple_time != 0 and pygame.time.get_ticks() >= blue_apple_time:
        game_speed = normal_speed
        blue_apple_time = 0

    for segment in snake_body[:-1]:
        if segment == [head_x, head_y]:
            game_state = "DEAD"

    snake_body.append([head_x, head_y])

    if len(snake_body) > snake_length:
        del snake_body[0]


    screen.fill((30, 30, 30))
    if game_state == "START":
        title = title_font.render("SNAKE GAME", True, (0, 255, 120))
        instruction1 = instruction_font.render("Use Arrow Keys to Move", True, (255, 255, 255))
        instruction2 = instruction_font.render("Eat Red Apples to Grow", True, (255, 255, 255))
        instruction3 = instruction_font.render("Blue Apples Boost Speed for 10 Seconds", True, (255, 255, 255))
        prompt = instruction_font.render("Press SPACE to Play", True, (50, 255, 255))
    
        screen.blit(title, (200, 150))
        screen.blit(instruction1, (150, 250))
        screen.blit(instruction2, (150, 280))
        screen.blit(instruction3, (100, 310))
        screen.blit(prompt, (210, 380))

    elif game_state == "DEAD":
        death_title = title_font.render("GAME OVER", True, (255, 0, 0))
        final_score = title_font.render(f"Final Score: {score}", True, (255, 255, 255))
        replay_prompt = instruction_font.render("Press SPACE to Return to Menu", True, (50, 255, 255))
        
        screen.blit(death_title, (200, 150))
        screen.blit(final_score, (150, 250))
        screen.blit(replay_prompt, (120, 350))

    else:
        for i, segment in enumerate(snake_body):
            if i == len(snake_body) - 1:
                colour = (0, 220, 100)
            else:
                colour = (0, 200, 90)
            pygame.draw.rect(screen, colour, (segment[0], segment[1], block_size, block_size))
        pygame.draw.rect(screen, (255, 0, 0), (food_x, food_y, block_size, block_size))
        if blue_x != -100 and blue_y != -100:
            pygame.draw.rect(screen, (0, 150, 255), (blue_x, blue_y, block_size, block_size))
        
        score_text = instruction_font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
    pygame.display.flip()
    clock.tick(game_speed)
