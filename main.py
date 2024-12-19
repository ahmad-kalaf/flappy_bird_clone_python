import pygame, sys, random

from secure_score import SecureScore

# Constans
WIDTH = 345.6
HEIGHT = 614.4
BG_TRANSFORM_FACTOR = 1.2

# change screensize:
scale = 1.2
WIDTH = int(WIDTH * scale)  # Ganzzahlen
HEIGHT = int(HEIGHT * scale)
BG_TRANSFORM_FACTOR = BG_TRANSFORM_FACTOR * scale

def draw_floor():
    screen.blit(source=floor_surface, dest=(floor_x_pos,floor_y_position))
    screen.blit(source=floor_surface, dest=(floor_x_pos+WIDTH,floor_y_position))

def improt_and_transform_png(source: str) -> pygame.Surface:
    surface = pygame.image.load(source).convert_alpha()
    surface = pygame.transform.scale_by(surface, factor=BG_TRANSFORM_FACTOR)
    return surface

def check_collisions(pipes) -> bool:
    if bird_rect.top <= 0 or bird_rect.bottom >= floor_y_position:
        hit_sound.play()
        return False
    for p in pipes:
        if bird_rect.colliderect(p):
            hit_sound.play()
            return False
    return True

def create_pipes():
    random_height = random.choice(pipes_height)
    top_pipe = pipe_surface.get_rect(midbottom = ((WIDTH*2),random_height - (HEIGHT*0.25)))
    bottom_pipe = pipe_surface.get_rect(midtop = ((WIDTH*2),random_height))
    return top_pipe, bottom_pipe

def move_pipes(pipes):
    for p in pipes:
        p.centerx -= 4
    return pipes

def draw_pipes():
    for p in pipe_list:
        if p.bottom >= HEIGHT - 100:
            screen.blit(source=pipe_surface, dest=p)
        else:
            flip_pipe = pygame.transform.flip(surface=pipe_surface, flip_x=False, flip_y=True)
            screen.blit(source=flip_pipe, dest=p)

def rotate_bird(bird: pygame.Surface):
    return pygame.transform.rotozoom(surface=bird, angle= - bird_movment * 3, scale=1)

def display_score(is_game_over: bool):
    score_surface = game_font.render(f'SCORE: {score}', True, (255,255,255))
    score_rect = score_surface.get_rect(center = ((WIDTH/2), (HEIGHT-(HEIGHT*0.95))))
    screen.blit(score_surface, score_rect)
    if is_game_over:
        high_score_surface = game_font.render(f'HIGHSCORE: {high_score}', True, (228, 8, 10))
        high_score_rect = high_score_surface.get_rect(center = ((WIDTH/2), (HEIGHT-(HEIGHT*0.85))))
        screen.blit(high_score_surface, high_score_rect)

def update_score():
    global score, high_score
    for i in range(len(pipe_list)-1):
            pipe = pipe_list[i]
            next_pipe = pipe_list[i+1]
            if pipe.right < bird_rect.left and pipe not in passed_pipes:
                passed_pipes.append(pipe)
                passed_pipes.append(next_pipe)
                score += 1
                point_sound.play()
    high_score = score if score > high_score else high_score

pygame.mixer.pre_init(frequency= 44100, size= 16, channels= 1, buffer= 512)
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 25)
secure_score = SecureScore()

game_active = False
floor_x_pos = 0
floor_y_position = HEIGHT - 100
gravity = 0.45
bird_movment = 0
pipes_height = [(HEIGHT*0.8),(HEIGHT*0.7),(HEIGHT*0.65),(HEIGHT*0.6),(HEIGHT*0.5),(HEIGHT*0.4),(HEIGHT*0.35),(HEIGHT*0.3)]
score = 0
high_score = secure_score.load_score()
passed_pipes = []

bg_surface = improt_and_transform_png('assets/background-day.png')

floor_surface = improt_and_transform_png('assets/base.png')

bird_frames = [
    pygame.transform.scale_by(pygame.image.load('assets/redbird-downflap.png'), factor=BG_TRANSFORM_FACTOR).convert_alpha(),
    pygame.transform.scale_by(pygame.image.load('assets/redbird-midflap.png'), factor=BG_TRANSFORM_FACTOR).convert_alpha(),
    pygame.transform.scale_by(pygame.image.load('assets/redbird-upflap.png'), factor=BG_TRANSFORM_FACTOR).convert_alpha(),
]
bird_frames_index = 0
bird_surface = bird_frames[bird_frames_index]
bird_rect = bird_surface.get_rect(center = (100,(HEIGHT/2)))

flip_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
point_sound = pygame.mixer.Sound('sound/sfx_point.wav')

pipe_surface = improt_and_transform_png('assets/pipe-green.png')
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(event=SPAWNPIPE,millis=1100)
BIRDFLAP = pygame.USEREVENT+1
pygame.time.set_timer(BIRDFLAP, 100)

game_over_surface = improt_and_transform_png('assets/message.png')
screen_center_x = screen.get_rect().centerx
screen_center_y = screen.get_rect().centery
game_over_rect = game_over_surface.get_rect(center = (screen_center_x, screen_center_y))

while True: 
    # looking for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            secure_score.save_score(high_score)
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movment = 0
                bird_movment -= 9
                flip_sound.play()
            if event.key == pygame.K_SPACE and not(game_active):
                game_active = True
                pipe_list.clear()
                passed_pipes.clear()
                bird_rect.center = 100,(HEIGHT/2)
                bird_movment = 0
                score = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipes())
        if event.type == BIRDFLAP:
            bird_frames_index += 1
            bird_frames_index = bird_frames_index % 2
            bird_surface = bird_frames[bird_frames_index]
        if event.type == pygame.MOUSEBUTTONDOWN and game_active:
            bird_movment = 0
            bird_movment -= 9
            flip_sound.play()
        if event.type == pygame.MOUSEBUTTONDOWN and not(game_active):
            game_active = True
            pipe_list.clear()
            passed_pipes.clear()
            bird_rect.center = 100,(HEIGHT/2)
            bird_movment = 0
            score = 0

    screen.blit(source=bg_surface, dest=(0,0))
    if game_active:
        # Bird
        bird_movment += gravity
        bird_rect.centery += bird_movment 
        rotated_bird = rotate_bird(bird_surface)
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collisions(pipe_list)
        
        # Pipes
        pipe_list = move_pipes(pipe_list)
        update_score()
        draw_pipes()
        display_score(False)
    else:
        screen.blit(game_over_surface, game_over_rect)
        display_score(True)

    # Floor
    floor_x_pos -= 4
    draw_floor()
    if (floor_x_pos) <= -WIDTH:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(60) # max fps