## Imports Libraries
import pygame, sys

## draw_floor function, draws two images of the floor
def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,900))
    ## draws second floor image to the right of the first
    screen.blit(floor_surface,(floor_x_pos + 576,900))

## creates a new pipe with rectangle at coords
def create_pipe():
    new_pipe = pipe_surface.get_rect(midtop = (288,512))
    return new_pipe

## for every pipe in the list pipes, move left 5px
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        screen.blit(pipe_surface,pipe)


## initialises pygame
pygame.init()
## sets screen resolution
screen = pygame.display.set_mode((576, 1024))
## defines clock for game fps
clock = pygame.time.Clock()

## Game Variables

gravity = 0.25
bird_movement = 0

## loads main surface png file for background
bg_surface = pygame.image.load('assets/background-day.png').convert()
## scales image x2 to fit screen resolution
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
## sets floor position to be at 0
floor_x_pos = 0

bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert()
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center = (100,512))

pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
## creates a pipe list, sets the time to swawn a new pipe at 1200 milliseconds
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)

while True:
    for event in pygame.event.get():
        ## if game quit, the quit game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        ## If space bar is pressed, paused gravity and move bird up
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 12
        if event.type == SPAWNPIPE:
            pipe_list.append(create_pipe())

    ## draws images
    screen.blit(bg_surface,(0,0))

    ## Bird gravity

    bird_movement += gravity
    bird_rect.centery += bird_movement
    screen.blit(bird_surface,bird_rect)

    pipe_list = move_pipes(pipe_list)
    draw_pipes(pipe_list)

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