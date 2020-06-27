## Imports Libraries
import pygame, sys, random

## draw_floor function, draws two images of the floor
def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,900))
    ## draws second floor image to the right of the first
    screen.blit(floor_surface,(floor_x_pos + 576,900))

## creates a new pipe with rectangle at coords
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (288,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (288,random_pipe_pos - 300))
    return bottom_pipe,top_pipe

## for every pipe in the list pipes, move left 5px
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        ## If pipe is at the bottom , do nothing, else flip the pipe
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False
    
    return True

## rotates bird
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-bird_movement * 3,1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird,new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (288,850))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score
## initialises pygame
pygame.init()
## sets screen resolution
screen = pygame.display.set_mode((576, 1024))
## defines clock for game fps
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF',40)

## Game Variables

gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

## loads main surface png file for background
bg_surface = pygame.image.load('assets/background-day.png').convert()
## scales image x2 to fit screen resolution
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
## sets floor position to be at 0
floor_x_pos = 0

## adds three images for animation, adds to list
bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100,512))

## user event has to be + 1 because user event has already been used. Each time used, + 1
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

#bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
#bird_surface = pygame.transform.scale2x(bird_surface)
#bird_rect = bird_surface.get_rect(center = (100,512))

pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
## creates a pipe list, sets the time to swawn a new pipe at 1200 milliseconds
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
## possible heights for pipes
pipe_height = [400,600,800] 

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288,512))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')

while True:
    for event in pygame.event.get():
        ## if game quit, the quit game
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        ## If space bar is pressed, paused gravity and move bird up
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 12
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,512)
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            ## loops around 1,2,0 animation frames, has to be if statement to stop number getting too big
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface,bird_rect = bird_animation()

    ## draws images
    screen.blit(bg_surface,(0,0))

    if game_active:
        ## Bird gravity
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        ## Shows rotated bird
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collision(pipe_list)

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score += 0.01
        score_display('main_game')
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')

    ## redraws floor -1 pixels every frame
    floor_x_pos -= 1
    ## calls draw floor function
    draw_floor()
    ## if floor is less than 576 (screen res) then
    ## reset back to 0, creating a looping effect
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    ## game fps
    clock.tick(120)