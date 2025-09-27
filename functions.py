from classes import Sorcerer, Guard, HealthBar
from constants import *
import pygame
pygame.init()


####################### FUNCTIONS / PROCEDURES  #############################


def Rescale_img(image, scale):

    W = image.get_width()
    H = image.get_height()
    rescaled_image = pygame.transform.scale(image, (W * scale, H * scale))
    return rescaled_image


def Load_tiles():

    tiles = []
    tiles.append(Rescale_img(pygame.image.load("1.png"), TILE_SIZE))
    tiles.append(Rescale_img(pygame.image.load("2.png"), TILE_SIZE))
    tiles.append(Rescale_img(pygame.image.load("3.png"), TILE_SIZE))
    tiles.append(Rescale_img(pygame.image.load("4.png"), TILE_SIZE))
    tiles.append(Rescale_img(pygame.image.load("5.png"), TILE_SIZE))  # collide
    tiles.append(Rescale_img(pygame.image.load("6.png"), TILE_SIZE))  # collide
    return tiles


def Read_level_data(door):

    world_data = []
    if door == 0:
        f = open("lobby.txt", "r")
    if door == 1:
        f = open("red_door.txt", "r")
    if door == 2:
        f = open("blue_door.txt", "r")
    if door == 3:
        f = open("green_door.txt", "r")
    if door == 4:
        f = open("yellow_door.txt", "r")

    for line in f:  # arr
        # strip blank space
        # split at commas
        mini_list = [item.strip() for item in line.split(",")]
        world_data.append(mini_list)
    f.close()

    return world_data


def write_text(text, font, col, x, y, surf):

    text = font.render(text, True, col)
    surf.blit(text, (x, y))


def Load_orcas():

    x = True
    orcas_2 = pygame.image.load("Orcas_2.png")
    orcas_2 = Rescale_img(orcas_2, PLAYER_SCALE)
    orcas_3 = pygame.image.load("Orcas_3.png")
    orcas_3 = Rescale_img(orcas_3, PLAYER_SCALE)
    orcas_4 = pygame.image.load("Orcas_4.png")
    orcas_4 = Rescale_img(orcas_4, PLAYER_SCALE)
    orcas_5 = pygame.image.load("Orcas_5.png")
    orcas_5 = Rescale_img(orcas_5, PLAYER_SCALE)
    sprite_list = [orcas_2, orcas_3, orcas_4, orcas_5]
    return sprite_list, x


def Load_coyote():

    x = True
    coyote_2 = pygame.image.load("Coyote_2.png")
    coyote_2 = Rescale_img(coyote_2, PLAYER_SCALE)
    coyote_3 = pygame.image.load("Coyote_3.png")
    coyote_3 = Rescale_img(coyote_3, PLAYER_SCALE)
    coyote_4 = pygame.image.load("Coyote_4.png")
    coyote_4 = Rescale_img(coyote_4, PLAYER_SCALE)
    coyote_5 = pygame.image.load("Coyote_5.png")
    coyote_5 = Rescale_img(coyote_5, PLAYER_SCALE)
    sprite_list = [coyote_2, coyote_3, coyote_4, coyote_5]
    return sprite_list, x


def Calculate_movement(up, down, left, right, character):

    y = 0
    x = 0

    if right:
        x = VELOCITY
    elif left:
        x = -VELOCITY
    elif up:
        y = -VELOCITY
    elif down:
        y = VELOCITY

    return x, y


def Camera(target):

    cam_x = 0
    cam_y = 0
    if target.rect.right > (SCREEN_WIDTH - CAMERA_BUFFER):
        cam_x = (SCREEN_WIDTH - CAMERA_BUFFER) - target.rect.right
        target.rect.right = (SCREEN_WIDTH-CAMERA_BUFFER)
    elif target.rect.left < CAMERA_BUFFER:
        cam_x = CAMERA_BUFFER - target.rect.left
        target.rect.left = CAMERA_BUFFER

    elif target.rect.top > (SCREEN_HEIGHT - CAMERA_BUFFER):
        cam_y = (SCREEN_HEIGHT - CAMERA_BUFFER) - target.rect.top
        target.rect.top = (SCREEN_HEIGHT-CAMERA_BUFFER)
    elif target.rect.bottom < CAMERA_BUFFER:
        cam_y = CAMERA_BUFFER - target.rect.bottom
        target.rect.bottom = CAMERA_BUFFER

    return cam_x, cam_y


def Event_Keydown(event, up, down, left, right):

    if event.type == pygame.KEYDOWN:
        if (event.key == pygame.K_a) or (event.key == pygame.K_LEFT):
            left = True
        if (event.key == pygame.K_d) or (event.key == pygame.K_RIGHT):
            right = True
        if (event.key == pygame.K_w) or (event.key == pygame.K_UP):
            up = True
        if (event.key == pygame.K_s) or (event.key == pygame.K_DOWN):
            down = True
    return up, down, left, right


def Event_Keyup(event, up, down, left, right):

    if event.type == pygame.KEYUP:
        if (event.key == pygame.K_a) or (event.key == pygame.K_LEFT):
            left = False
        if (event.key == pygame.K_d) or (event.key == pygame.K_RIGHT):
            right = False
        if (event.key == pygame.K_w) or (event.key == pygame.K_UP):
            up = False
        if (event.key == pygame.K_s) or (event.key == pygame.K_DOWN):
            down = False
    return up, down, left, right


def Character_load(orcas, coyote):

    character = None

    # character weapons
    Melee = Rescale_img(pygame.image.load("Melee.png"), MELEE_SCALE)
    Spell = Rescale_img(pygame.image.load("Spell.png"), SPELL_SCALE)
    Wand = Rescale_img(pygame.image.load("Wand.png"), WAND_SCALE)

    if orcas:
        sprite_list, null = Load_orcas()
        character = Sorcerer(X_POSITION, Y_POSITION, sprite_list, Spell, Wand)
    elif coyote:
        sprite_list, null = Load_coyote()
        character = Guard(X_POSITION, Y_POSITION, sprite_list, Melee)
    return character


def Draw_Char(orcas, coyote, screen, character):

    if coyote:
        character.draw_melee(screen)
        character.fight()
    elif orcas:
        character.draw_wand(screen)
        character.cast_spell()
        character.draw_spell(screen)


def Player_Info(screen, character):

    health_bar = HealthBar(30, 30)
    stats_img = Rescale_img(pygame.image.load("Stats.png"), 5)
    pygame.draw.rect(screen, (104, 107, 117), (0, 0, SCREEN_WIDTH, 100))  # player stats bar
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, SCREEN_WIDTH, 100), 3)
    health_bar.draw_health_bar(screen, character.get_health())
    screen.blit(stats_img, (350, 20))  # text saying stats

