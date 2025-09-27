from database import *
import mysql.connector
from collections import deque
from classes import *
from functions import *
pygame.init()


CLOCK = pygame.time.Clock()
lobby_img = Rescale_img(pygame.image.load("Lobby.png"), LOBBY)
# queue ensures player advances in correct sequence
KEY_QUEUE = deque(["blue", "green", "yellow", "pink"])


####################### MAIN GAME #############################

def correct_key():
    key = get_game_key()

    if key == "blue":
        KEY_QUEUE.popleft()

    if key == "green":
        KEY_QUEUE.popleft()
        KEY_QUEUE.popleft()

    if key == "yellow":
        KEY_QUEUE.popleft()
        KEY_QUEUE.popleft()
        KEY_QUEUE.popleft()

    if key == "pink":
        KEY_QUEUE.popleft()
        KEY_QUEUE.popleft()
        KEY_QUEUE.popleft()
        KEY_QUEUE.popleft()

    return key


def save():
    ID = save_userid()
    print(DEQUEUED_KEY)
    print(USERID)

    # establish connection
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="PlayerVaultDB"
        )
    my_cursor = connection.cursor()

    UPDATE = "UPDATE gameData SET keyFound = %s WHERE gameDataID = %s"
    my_cursor.execute(UPDATE, (DEQUEUED_KEY, ID))
    connection.commit()

    # Close the cursor and connection
    my_cursor.close()
    connection.close()
    print(my_cursor.rowcount, "records affected")
    print("update successful")


def Die(orcas, coyote):
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("You Died")

    font = pygame.font.SysFont(None, 50)
    text = "YOU DIED: ADVENTURE OVER"

    retry_img = Rescale_img(pygame.image.load("Retry.png"), NEXT_BTN_SCALE)
    retry_btn = Button(490, 450, retry_img, NEXT_RECT_X, NEXT_RECT_Y)

    RUNNING = True
    while RUNNING:
        CLOCK.tick(FPS)
        SCREEN.fill((128, 128, 128))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        write_text(text, font, (0, 0, 0), 230, 270, SCREEN)
        retry_btn.draw_button(SCREEN)

        if retry_btn.click_button():
            Lobby(orcas, coyote)
            RUNNING = False

        pygame.display.update()


def Escape():
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Escape")

    resume_img = Rescale_img(pygame.image.load("Resume.png"), NEXT_BTN_SCALE)
    save_img = Rescale_img(pygame.image.load("Save.png"), NEXT_BTN_SCALE)
    quit_img = Rescale_img(pygame.image.load("Quit.png"), NEXT_BTN_SCALE)
    resume_btn = Button(470, 200, resume_img, NEXT_RECT_X, NEXT_RECT_Y)
    save_btn = Button(470, 300, save_img, NEXT_RECT_X, NEXT_RECT_Y)
    quit_btn = Button(470, 400, quit_img, NEXT_RECT_X, NEXT_RECT_Y)

    RUNNING = True
    while RUNNING:
        CLOCK.tick(FPS)
        SCREEN.fill((128, 128, 128))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False

            key = pygame.key.get_pressed()
            if key[pygame.K_ESCAPE]:
                RUNNING = False

        resume_btn.draw_button(SCREEN)
        save_btn.draw_button(SCREEN)
        quit_btn.draw_button(SCREEN)

        if resume_btn.click_button():
            RUNNING = False
        if quit_btn.click_button():
            quit()
        if save_btn.click_button():
            save()
            print("saved")
        pygame.display.update()


def Intro_scene(orcas, coyote):
    complete = False
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Introduction")

    font = pygame.font.SysFont(None, 25)

    text1 = "You find yourself in a shadowy dungeon, the cold stone walls whispering tales of forgotten times."
    text2 = "Before you are four imposing doors, each sealed with a different coloured key"
    text3 = "It becomes clear that to escape this place, you must find the keys hidden behind these doors"
    text4 = "You must unlock your path to freedom..."

    next_img = Rescale_img(pygame.image.load("Next.png"), NEXT_BTN_SCALE)
    next_btn = Button(480, 550, next_img, NEXT_RECT_X, NEXT_RECT_Y)

    RUNNING = True
    while RUNNING:
        CLOCK.tick(FPS)  # prevents game running too quick
        SCREEN.fill((128, 128, 128))

        if complete:
            Lobby(orcas, coyote)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
                quit()

        write_text(text1, font, (0, 0, 0), 100, 100, SCREEN)
        write_text(text2, font, (0, 0, 0), 170, 150, SCREEN)
        write_text(text3, font, (0, 0, 0), 120, 200, SCREEN)
        write_text(text4, font, (0, 0, 0), 340, 270, SCREEN)

        next_btn.draw_button(SCREEN)
        if next_btn.click_button():
            complete = True

        pygame.display.update()


def RD_story():  # red door storyline
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Red Door Story")

    font = pygame.font.SysFont(None, 25)

    text1 = "After exploring the dungeon, you are faced with the first obstacle: "
    text2 = "The menacing ghouls lurking behind the red door"
    text3 = "Their eyes glow with evil, and their eerie moans echo through the chamber"
    text4 = "The only way to progress is to confront these curses of nature..."

    next_img = Rescale_img(pygame.image.load("Next.png"), NEXT_BTN_SCALE)
    next_btn = Button(480, 550, next_img, NEXT_RECT_X, NEXT_RECT_Y)

    RUNNING = True
    while RUNNING:
        CLOCK.tick(FPS)  # prevents game running too quick
        SCREEN.fill((128, 128, 128))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
                quit()

        write_text(text1, font, (0, 0, 0), 230, 100, SCREEN)
        write_text(text2, font, (0, 0, 0), 280, 150, SCREEN)
        write_text(text3, font, (0, 0, 0), 180, 200, SCREEN)
        write_text(text4, font, (0, 0, 0), 220, 280, SCREEN)

        next_btn.draw_button(SCREEN)
        if next_btn.click_button():
            RUNNING = False

        pygame.display.update()


def BD_story():  # blue door storyline
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Blue Door Story")

    font = pygame.font.SysFont(None, 25)

    text1 = "With the blue key in hand, you unlock the second door."
    text2 = "The chamber is small, and inside rests an ancient spellbook"
    text3 = "To obtain the green key, you must decipher the books twisted rhymes"
    text4 = "Unroll the secrets, flip the fortune's token, a precious metal, the blade spoken."

    next_img = Rescale_img(pygame.image.load("Next.png"), NEXT_BTN_SCALE)
    next_btn = Button(480, 550, next_img, NEXT_RECT_X, NEXT_RECT_Y)

    RUNNING = True
    while RUNNING:
        CLOCK.tick(FPS)  # prevents game running too quick
        SCREEN.fill((128, 128, 128))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
                quit()

        write_text(text1, font, (0, 0, 0), 270, 100, SCREEN)
        write_text(text2, font, (0, 0, 0), 240, 150, SCREEN)
        write_text(text3, font, (0, 0, 0), 200, 200, SCREEN)
        write_text(text4, font, (0, 0, 0), 160, 280, SCREEN)

        next_btn.draw_button(SCREEN)
        if next_btn.click_button():
            RUNNING = False

        pygame.display.update()


def GD_story():  # green door storyline
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Green Door Story")

    font = pygame.font.SysFont(None, 25)

    text1 = "Beyond the green door lies a vast hall adorned with relics from a bygone era"
    text2 = "Four pedestals stand empty, awaiting the return of their respective treasures."
    text3 = "To unlock the yellow key, you must place the four items in their correct positions"
    text4 = "Relics old, in shadows entwined, Align their tales, their powers combined."

    next_img = Rescale_img(pygame.image.load("Next.png"), NEXT_BTN_SCALE)
    next_btn = Button(480, 550, next_img, NEXT_RECT_X, NEXT_RECT_Y)

    RUNNING = True
    while RUNNING:
        CLOCK.tick(FPS)  # prevents game running too quick
        SCREEN.fill((128, 128, 128))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
                quit()

        write_text(text1, font, (0, 0, 0), 150, 100, SCREEN)
        write_text(text2, font, (0, 0, 0), 145, 150, SCREEN)
        write_text(text3, font, (0, 0, 0), 130, 200, SCREEN)
        write_text(text4, font, (0, 0, 0), 170, 280, SCREEN)

        next_btn.draw_button(SCREEN)
        if next_btn.click_button():
            RUNNING = False

        pygame.display.update()


def YD_story():  # yellow door storyline
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Yellow Door Story")

    font = pygame.font.SysFont(None, 25)

    text1 = "The yellow door opens to reveal a chamber filled with huge creatures"
    text2 = "Powerful beasts, guardians of the dungeon lunge at you, each stronger than the last."
    text3 = "To claim the final key, you outsmart these guardians"
    text4 = "but beware, these guardians are tasked with protecting the dungeons deepest secrets..."

    next_img = Rescale_img(pygame.image.load("Next.png"), NEXT_BTN_SCALE)
    next_btn = Button(480, 400, next_img, NEXT_RECT_X, NEXT_RECT_Y)

    RUNNING = True
    while RUNNING:
        CLOCK.tick(FPS)  # prevents game running too quick
        SCREEN.fill((128, 128, 128))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
                quit()

        write_text(text1, font, (0, 0, 0), 190, 100, SCREEN)
        write_text(text2, font, (0, 0, 0), 130, 150, SCREEN)
        write_text(text3, font, (0, 0, 0), 260, 200, SCREEN)
        write_text(text4, font, (0, 0, 0), 130, 500, SCREEN)

        next_btn.draw_button(SCREEN)
        if next_btn.click_button():
            RUNNING = False

        pygame.display.update()


def Ending():  # ending

    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Ending")

    font = pygame.font.SysFont(None, 25)

    text1 = "With the pink key in hand, you approach the final door — a gateway to freedom"
    text2 = "As the door swings open, a rush of fresh air fills the room, and you step out"
    text3 = "you feel victorious having unlocked the secrets of the four doors."
    text4 = "But as you stand in the doorway, you realize that the true treasure lies not in the escape"
    text5 = "but in the battles fought, the riddles solved, and the keys collected along the way."

    next_img = Rescale_img(pygame.image.load("Next.png"), NEXT_BTN_SCALE)
    next_btn = Button(480, 550, next_img, NEXT_RECT_X, NEXT_RECT_Y)

    RUNNING = True
    while RUNNING:
        CLOCK.tick(FPS)  # prevents game running too quick
        SCREEN.fill((128, 128, 128))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
                quit()

        write_text(text1, font, (0, 0, 0), 170, 100, SCREEN)
        write_text(text2, font, (0, 0, 0), 170, 150, SCREEN)
        write_text(text3, font, (0, 0, 0), 210, 200, SCREEN)
        write_text(text4, font, (0, 0, 0), 140, 250, SCREEN)
        write_text(text5, font, (0, 0, 0), 150, 300, SCREEN)

        next_btn.draw_button(SCREEN)
        if next_btn.click_button():
            quit()

        pygame.display.update()


def dragging_puzzle(orcas, coyote):
    GD_story()
    items = []
    pos_index = None
    identifier = None
    node = None
    correct = ['scroll', 'coin', 'silver', 'blade']
    font = pygame.font.SysFont(None, 50)

    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("The Relic Puzzle")

    # img
    silver_img = Rescale_img(pygame.image.load("Silver.png"), LL_SCALE)
    coin_img = Rescale_img(pygame.image.load("Coin.png"), LL_SCALE)
    dull_blade_img = Rescale_img(pygame.image.load("Dull_blade.png"), LL_SCALE)
    scroll_img = Rescale_img(pygame.image.load("Scroll.png"), LL_SCALE)

    # instances
    coin = DraggableItem(coin_img, 200, 200, 1)
    scroll = DraggableItem(scroll_img, 400, 200, 2)
    silver = DraggableItem(silver_img, 600, 200, 3)
    dull_blade = DraggableItem(dull_blade_img, 800, 200, 4)

    enter_img = Rescale_img(pygame.image.load("Enter.png"), 4)
    enter_btn = Button(490, 600, enter_img, MENU_RECT_X, MENU_RECT_Y)

    items.append(coin)
    items.append(scroll)
    items.append(silver)
    items.append(dull_blade)

    rect1 = pygame.Rect(175, 350, 150, 150)
    rect2 = pygame.Rect(325, 350, 150, 150)
    rect3 = pygame.Rect(475, 350, 150, 150)
    rect4 = pygame.Rect(625, 350, 150, 150)

    linked_list = LinkedList()

    RUNNING = True

    while RUNNING:

        SCREEN.fill((128, 128, 128))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if event.button == 1:
                    for item in items:
                        if item.item_rect.collidepoint(pos):
                            item.drag = True
            if event.type == pygame.MOUSEBUTTONUP:
                for item in items:
                    item.drag = False

        enter_btn.draw_button(SCREEN)
        if enter_btn.click_button():
            enter = True
        else:
            enter = False

        pygame.draw.rect(SCREEN, (0, 0, 0), rect1, 3)
        pygame.draw.rect(SCREEN, (0, 0, 0), rect2, 3)
        pygame.draw.rect(SCREEN, (0, 0, 0), rect3, 3)
        pygame.draw.rect(SCREEN, (0, 0, 0), rect4, 3)

        for item in items:
            item.draw(SCREEN)
            item.update()

            if item.item_rect.colliderect(rect1):
                pos_index = 0
                identifier = item.id
                node = item.get_node()
            if not item.item_rect.colliderect(rect1):
                identifier = item.id  # Retrieve the id for itm
                try:
                    linked_list.remove_ll(identifier)
                except:
                    pass

            if item.item_rect.colliderect(rect2):
                pos_index = 1
                identifier = item.id
                node = item.get_node()

            if item.item_rect.colliderect(rect3):
                pos_index = 2
                identifier = item.id
                node = item.get_node()

            if item.item_rect.colliderect(rect4):
                pos_index = 3
                identifier = item.id
                node = item.get_node()

            if pos_index is not None:
                if node is not None:
                    if linked_list.insert_ll(node, identifier, pos_index):
                        # if item was inserted reset variables
                        pos_index = None
                        node = None
                    else:
                        # if pos out of range append item
                        linked_list.append_ll(node, identifier)
                        # reset variables
                        pos_index = None
                        node = None

        text = str(linked_list.display_ll())
        write_text(text, font, (0, 0, 0), 250, 50, SCREEN)

        if enter:
            if linked_list.display_ll() == correct:
                print("correct")
                RUNNING = False
                Enter_Green(orcas, coyote)
            elif linked_list.display_ll() != correct:
                print("try again")

        pygame.display.update()


def potion_puzzle(order, r, g, b, complete, SCREEN):
    correct_order = ["green", "red", "blue"]
    puzzle = True
    pygame.display.set_caption("The Potion Enchantment Puzzle")
    SCREEN.fill((114, 111, 117))
    font = pygame.font.SysFont(None, 25)

    # potion puzzle
    red_puzzle_img = Rescale_img(pygame.image.load("Red_puzzle.png"), PZL_SCALE)
    blue_puzzle_img = Rescale_img(pygame.image.load("Blue_puzzle.png"), PZL_SCALE)
    green_puzzle_img = Rescale_img(pygame.image.load("Green_puzzle.png"), PZL_SCALE)
    bin_img = Rescale_img(pygame.image.load("Bin.png"), PZL_SCALE)

    text1 = "In a forgotten chamber, there's a spell book lying open"
    text2 = "The spell book contains a cryptic verse, To receive a key you must complete the riddle:"
    text3 = ("To harness the age-old magic and elevate your brew begin with the potion of red mingling with the "
             "forest's hue.")
    text4 = ("But heed this warning, before your task is through, The potion of blue must come last, or all you've "
             "done will undo.")
    text5 = "What order should the potions be combined in ?"

    red = Button(200, 550, red_puzzle_img, PZL_W, PZL_H)
    blue = Button(400, 550, blue_puzzle_img, PZL_W, PZL_H)
    green = Button(600, 550, green_puzzle_img, PZL_W, PZL_H)
    bin = Button(800, 550, bin_img, PZL_W, PZL_H)

    write_text(text1, font, (0, 0, 0), 250, 100, SCREEN)
    write_text(text2, font, (0, 0, 0), 110, 150, SCREEN)
    write_text(text3, font, (0, 0, 0), 30, 250, SCREEN)
    write_text(text4, font, (0, 0, 0), 20, 300, SCREEN)
    write_text(text5, font, (0, 0, 0), 270, 400, SCREEN)

    red.draw_button(SCREEN)
    blue.draw_button(SCREEN)
    green.draw_button(SCREEN)
    bin.draw_button(SCREEN)

    if bin.click_button():
        r, g, b = False, False, False
        if len(order) >= 1:
            order.pop()  # pop item from stack
            print(order)

    if g:
        write_text("Green", font, (0, 255, 0), 570, 460, SCREEN)
    if r:
        write_text("Red", font, (255, 0, 0), 180, 460, SCREEN)
    if b:
        write_text("Blue", font, (0, 0, 255), 380, 460, SCREEN)

    if green.click_button() and not g:
        g = True
        order.append("green")
        print(order)

    if red.click_button() and not r:
        r = True
        order.append("red")
        print(order)

    if blue.click_button() and not b:
        b = True
        order.append("blue")
        print(order)

    if order == correct_order:
        complete = True
        puzzle = False

    return puzzle, order, r, g, b, complete


def Lobby(orcas, coyote):
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Lobby")

    world = TilemapSurf()
    world_data = Read_level_data(0)
    tile_list = Load_tiles()
    world.create_map(world_data, tile_list)

    red_door_img = Rescale_img(pygame.image.load("Red_door.png"), DOOR_SCALE)
    blue_door_img = Rescale_img(pygame.image.load("Blue_door.png"), DOOR_SCALE)
    green_door_img = Rescale_img(pygame.image.load("Green_door.png"), DOOR_SCALE)
    yellow_door_img = Rescale_img(pygame.image.load("Yellow_door.png"), DOOR_SCALE)
    pink_door_img = Rescale_img(pygame.image.load("Pink_door.png"), DOOR_SCALE)

    # doors
    door_group = pygame.sprite.Group()
    red_door = Collectables(R_DOOR_ID, red_door_img, 50, 370, DOOR_W, DOOR_H)
    blue_door = Collectables(B_DOOR_ID, blue_door_img, 900, 370, DOOR_W, DOOR_H)
    green_door = Collectables(G_DOOR_ID, green_door_img, 480, 40, DOOR_W, DOOR_H)
    yellow_door = Collectables(Y_DOOR_ID, yellow_door_img, 480, 700, DOOR_W, DOOR_H)
    pink_door = Collectables(P_DOOR_ID, pink_door_img, 1600, 900, DOOR_W, DOOR_H)

    door_group.add(red_door, blue_door, green_door, yellow_door, pink_door)

    character = Character_load(orcas, coyote)

    UP, DOWN, LEFT, RIGHT = False, False, False, False
    RUNNING = True

    while RUNNING:
        CLOCK.tick(FPS)  # prevents game running too quick
        SCREEN.fill((0, 0, 0))

        X, Y = Calculate_movement(UP, DOWN, LEFT, RIGHT, character)
        CAM_X, CAM_Y = Camera(character)  # aggregation

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
                quit()

            # pressing key
            UP, DOWN, LEFT, RIGHT = Event_Keydown(event, UP, DOWN, LEFT, RIGHT)
            # releasing key
            UP, DOWN, LEFT, RIGHT = Event_Keyup(event, UP, DOWN, LEFT, RIGHT)

            # when ESC pressed
            key = pygame.key.get_pressed()
            if key[pygame.K_ESCAPE]:
                Escape()

        world.draw(SCREEN)

        for door in door_group:
            door.draw(SCREEN)
            door.scroll(CAM_X, CAM_Y)

            if door.enter_red_door(character):
                Enter_Red(orcas, coyote)
                RUNNING = False

            if door.enter_blue_door(character, DEQUEUED_KEY):
                Enter_Blue(orcas, coyote)
                RUNNING = False

            if door.enter_green_door(character, DEQUEUED_KEY):
                dragging_puzzle(orcas, coyote)
                RUNNING = False

            if door.enter_yellow_door(character, DEQUEUED_KEY):
                Enter_Yellow(orcas, coyote)
                RUNNING = False

            if door.enter_pink_door(character, DEQUEUED_KEY):
                Ending()
                RUNNING = False

        character.move_character(X, Y)
        character.animate(UP, DOWN, LEFT, RIGHT)
        character.draw_character(SCREEN)

        world.camera_scroll(CAM_X, CAM_Y)
        world.collisions(character.get_rect(), tile_list, X, Y)

        Draw_Char(orcas, coyote, SCREEN, character)
        Player_Info(SCREEN, character)

        pygame.display.update()


def Enter_Red(orcas, coyote):  # red door
    RD_story()
    global KEY_QUEUE
    global DEQUEUED_KEY
    got_blue_key = False

    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Red Door")

    # enemies
    Enemy_img = Rescale_img(pygame.image.load("Enemy.png"), ENEMY_SCALE)
    lobby_btn = Button(920, 50, lobby_img, LOBBY_W, LOBBY_H)

    tile_list = Load_tiles()
    world = TilemapSurf()
    world_data = Read_level_data(1)
    world.create_map(world_data, tile_list)

    enemy_group = pygame.sprite.Group()
    collectables_group = pygame.sprite.Group()

    blue_key_img = Rescale_img(pygame.image.load("Blue_key.png"), COLLECTABLES_SCALE)
    blue_key = Collectables(KEY_ID, blue_key_img, 300, 1800, COLLECTABLES_W, COLLECTABLES_H)
    Blue_potion_img = Rescale_img(pygame.image.load("Blue_potion.png"), POTION_SCALE)
    blue_potion = Collectables(3, Blue_potion_img, 100, 600, COLLECTABLES_W, COLLECTABLES_H)

    collectables_group.add(blue_potion)

    # generate random num of enemies
    num_enemies = rand.randint(1, 10)
    for i in range(0, num_enemies):
        enemy = Enemy(Enemy_img, 40, 40)
        enemy_group.add(enemy)

    character = Character_load(orcas, coyote)

    UP, DOWN, LEFT, RIGHT = False, False, False, False
    RUNNING = True
    while RUNNING:
        CLOCK.tick(FPS)  # prevents game running too quick
        SCREEN.fill((0, 0, 0))  # (92, 51, 2)

        X, Y = Calculate_movement(UP, DOWN, LEFT, RIGHT, character)
        CAM_X, CAM_Y = Camera(character)

        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
                quit()

            UP, DOWN, LEFT, RIGHT = Event_Keydown(event, UP, DOWN, LEFT, RIGHT)
            UP, DOWN, LEFT, RIGHT = Event_Keyup(event, UP, DOWN, LEFT, RIGHT)

            # when ESC pressed
            key = pygame.key.get_pressed()
            if key[pygame.K_ESCAPE]:
                Escape()

        world.draw(SCREEN)

        for enemy in enemy_group:
            enemy.draw_enemy(SCREEN)
            # Association
            gain_health = enemy.attack(character.get_rect(), character.get_clicked())
            enemy.update(SCREEN_WIDTH)
            # Association
            character.attack(SCREEN, enemy.get_enemy_rect(), gain_health)
            enemy.scroll(CAM_X, CAM_Y)

        if len(enemy_group) == 0 and not got_blue_key:
            got_blue_key = True
            collectables_group.add(blue_key)

        for collectable in collectables_group:
            collectable.draw(SCREEN)
            collectable.scroll(CAM_X, CAM_Y)
            KEY_QUEUE, DEQUEUED_KEY = collectable.collect_key(character.get_rect(), KEY_QUEUE, DEQUEUED_KEY)
            collectable.drink(character)

        character.move_character(X, Y)
        character.animate(UP, DOWN, LEFT, RIGHT)
        character.draw_character(SCREEN)
        # if die
        if character.character_health <= 0:
            Die(orcas, coyote)

        world.camera_scroll(CAM_X, CAM_Y)
        world.collisions(character.get_rect(), tile_list, X, Y)

        Draw_Char(orcas, coyote, SCREEN, character)
        Player_Info(SCREEN, character)

        lobby_btn.draw_button(SCREEN)
        if lobby_btn.click_button():
            Lobby(orcas, coyote)

        pygame.display.update()


def Enter_Blue(orcas, coyote):
    BD_story()
    global KEY_QUEUE
    global DEQUEUED_KEY
    order = []
    puzzle = False
    r, g, b = False, False, False
    complete = False

    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Blue Door")

    book_img = Rescale_img(pygame.image.load("Book.png"), BOOK_SCALE)
    lobby_btn = Button(920, 50, lobby_img, LOBBY_W, LOBBY_H)

    world = TilemapSurf()
    world_data = Read_level_data(2)
    tile_list = Load_tiles()
    world.create_map(world_data, tile_list)

    books = pygame.sprite.Group()
    keys = pygame.sprite.Group()
    book = Collectables(BOOK_ID, book_img, 430, 380, BOOK_W, BOOK_H)
    books.add(book)
    green_key_img = Rescale_img(pygame.image.load("Green_key.png"), COLLECTABLES_SCALE)
    green_key = Collectables(KEY_ID, green_key_img, 200, 380, COLLECTABLES_W, COLLECTABLES_H)
    keys.add(green_key)

    character = Character_load(orcas, coyote)

    UP, DOWN, LEFT, RIGHT = False, False, False, False
    RUNNING = True
    while RUNNING:

        CLOCK.tick(FPS)  # prevents game running too quick
        SCREEN.fill((0, 0, 0))

        X, Y = Calculate_movement(UP, DOWN, LEFT, RIGHT, character)
        CAM_X, CAM_Y = Camera(character)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
                quit()

            # pressing key
            UP, DOWN, LEFT, RIGHT = Event_Keydown(event, UP, DOWN, LEFT, RIGHT)

            # releasing key
            UP, DOWN, LEFT, RIGHT = Event_Keyup(event, UP, DOWN, LEFT, RIGHT)

            # when ESC pressed
            key = pygame.key.get_pressed()
            if key[pygame.K_ESCAPE]:
                Escape()

        world.draw(SCREEN)

        if len(books) > 0:
            for book in books:
                if not complete:
                    book.draw(SCREEN)
                    book.scroll(CAM_X, CAM_Y)
                    if book.spell_book(character):
                        puzzle = True

                if complete:
                    book.complete(True)

        if len(books) == 0:
            for key in keys:
                key.draw(SCREEN)
                key.scroll(CAM_X, CAM_Y)
                KEY_QUEUE, DEQUEUED_KEY = key.collect_key(character.get_rect(), KEY_QUEUE, DEQUEUED_KEY)

        character.move_character(X, Y)
        character.animate(UP, DOWN, LEFT, RIGHT)
        character.draw_character(SCREEN)

        world.camera_scroll(CAM_X, CAM_Y)
        world.collisions(character.get_rect(), tile_list, X, Y)

        Draw_Char(orcas, coyote, SCREEN, character)
        Player_Info(SCREEN, character)

        lobby_btn.draw_button(SCREEN)
        if lobby_btn.click_button():
            Lobby(orcas, coyote)

        if puzzle:
            puzzle, order, r, g, b, complete = potion_puzzle(order, r, g, b, complete, SCREEN)

        pygame.display.update()


def Enter_Green(orcas, coyote):
    global KEY_QUEUE
    global DEQUEUED_KEY

    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Green Door")

    keys = pygame.sprite.Group()
    yellow_key_img = Rescale_img(pygame.image.load("Yellow_key.png"), COLLECTABLES_SCALE)
    yellow_key = Collectables(KEY_ID, yellow_key_img, 500, 1400, COLLECTABLES_W, COLLECTABLES_H)
    keys.add(yellow_key)

    world = TilemapSurf()
    world_data = Read_level_data(3)
    tile_list = Load_tiles()
    world.create_map(world_data, tile_list)
    lobby_btn = Button(920, 50, lobby_img, LOBBY_W, LOBBY_H)

    character = Character_load(orcas, coyote)

    UP, DOWN, LEFT, RIGHT = False, False, False, False
    RUNNING = True
    while RUNNING:

        CLOCK.tick(FPS)  # prevents game running too quick
        SCREEN.fill((0, 0, 0))

        X, Y = Calculate_movement(UP, DOWN, LEFT, RIGHT, character)
        CAM_X, CAM_Y = Camera(character)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
                quit()

            UP, DOWN, LEFT, RIGHT = Event_Keydown(event, UP, DOWN, LEFT, RIGHT)
            UP, DOWN, LEFT, RIGHT = Event_Keyup(event, UP, DOWN, LEFT, RIGHT)

            key = pygame.key.get_pressed()
            if key[pygame.K_ESCAPE]:
                Escape()

        world.draw(SCREEN)

        character.move_character(X, Y)
        character.animate(UP, DOWN, LEFT, RIGHT)
        character.draw_character(SCREEN)

        world.camera_scroll(CAM_X, CAM_Y)
        world.collisions(character.get_rect(), tile_list, X, Y)

        Draw_Char(orcas, coyote, SCREEN, character)
        Player_Info(SCREEN, character)  # aggregation

        for key in keys:
            key.draw(SCREEN)
            key.scroll(CAM_X, CAM_Y)
            KEY_QUEUE, DEQUEUED_KEY = key.collect_key(character.get_rect(), KEY_QUEUE, DEQUEUED_KEY)

        lobby_btn.draw_button(SCREEN)
        if lobby_btn.click_button():
            Lobby(orcas, coyote)

        pygame.display.update()


def Enter_Yellow(orcas, coyote):
    YD_story()
    global KEY_QUEUE
    global DEQUEUED_KEY

    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Green Door")

    keys = pygame.sprite.Group()
    pink_key_img = Rescale_img(pygame.image.load("Pink_key.png"), COLLECTABLES_SCALE)
    pink_key = Collectables(KEY_ID, pink_key_img, 500, 500, COLLECTABLES_W, COLLECTABLES_H)
    keys.add(pink_key)

    boss_group = pygame.sprite.Group()
    boss_img = Rescale_img(pygame.image.load("Boss.png"), BOSS_SCALE)

    potion_group = pygame.sprite.Group()
    red_potion_img = Rescale_img(pygame.image.load("Red_potion.png"), POTION_SCALE)

    for i in range(6):
        x = rand.randint(200, 1200)
        y = rand.randint(300, 600)
        red_potion = Collectables(2, red_potion_img, x, y, COLLECTABLES_W, COLLECTABLES_H)
        potion_group.add(red_potion)

    for i in range(0, 3):
        boss = Enemy(boss_img, 100, 100)
        boss_group.add(boss)
    print(boss_group)  # temp

    world = TilemapSurf()
    world_data = Read_level_data(4)
    tile_list = Load_tiles()
    world.create_map(world_data, tile_list)
    lobby_btn = Button(920, 50, lobby_img, LOBBY_W, LOBBY_H)

    character = Character_load(orcas, coyote)

    UP, DOWN, LEFT, RIGHT = False, False, False, False
    RUNNING = True
    while RUNNING:

        CLOCK.tick(FPS)  # prevents game running too quick
        SCREEN.fill((0, 0, 0))

        X, Y = Calculate_movement(UP, DOWN, LEFT, RIGHT, character)
        CAM_X, CAM_Y = Camera(character)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
                quit()

            UP, DOWN, LEFT, RIGHT = Event_Keydown(event, UP, DOWN, LEFT, RIGHT)
            UP, DOWN, LEFT, RIGHT = Event_Keyup(event, UP, DOWN, LEFT, RIGHT)

            # when ESC pressed
            key = pygame.key.get_pressed()
            if key[pygame.K_ESCAPE]:
                Escape()

        world.draw(SCREEN)

        character.move_character(X, Y)
        character.animate(UP, DOWN, LEFT, RIGHT)
        character.draw_character(SCREEN)

        # if die
        if character.character_health <= 0:
            Die(orcas, coyote)

        world.camera_scroll(CAM_X, CAM_Y)
        world.collisions(character.get_rect(), tile_list, X, Y)

        for boss in boss_group:
            boss.draw_enemy(SCREEN)
            gain_health = boss.attack(character.get_rect(), character.get_clicked())
            boss.update(SCREEN_WIDTH)
            character.attack(SCREEN, boss.get_enemy_rect(), gain_health)
            boss.scroll(CAM_X, CAM_Y)

        for potion in potion_group:
            potion.draw(SCREEN)
            potion.scroll(CAM_X, CAM_Y)
            potion.drink(character) # aggregation

        Draw_Char(orcas, coyote, SCREEN, character)
        Player_Info(SCREEN, character)

        lobby_btn.draw_button(SCREEN)
        if lobby_btn.click_button():
            Lobby(orcas, coyote)

        if len(boss_group) == 0:
            for key in keys:
                key.draw(SCREEN)
                key.scroll(CAM_X, CAM_Y)
                KEY_QUEUE, DEQUEUED_KEY = key.collect_key(character.get_rect(), KEY_QUEUE, DEQUEUED_KEY)

        pygame.display.update()


def How_to_play():
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("How to Play")

    font = pygame.font.SysFont(None, 25)

    text1 = "You have mysteriously found yourself in an immense dungeon "
    text2 = "Surrounding you, there are numerous different coloured doors, unlocked by coloured keys"
    text3 = "Your aim is to escape the dungeon and find your way to freedom"
    text4 = "To Play:"
    text5 = "Use the arrow keys or [W], [A], [S], [D] keys to move"
    text6 = "Explore different rooms and corridors to find all the keys and unlock the doors."
    text7 = "Once you have collected a key, you can unlock the door of the corresponding color."
    text8 = "Approach the locked door and click to use the key to unlock it."
    text9 = "Pay attention to the clues in the dungeon to help you find the keys"
    text10 = "Best of luck for your adventure..."

    next_img = Rescale_img(pygame.image.load("Next.png"), NEXT_BTN_SCALE)
    next_btn = Button(470, 570, next_img, NEXT_RECT_X, NEXT_RECT_Y)

    RUNNING = True
    while RUNNING:
        CLOCK.tick(FPS)  # prevents game running too quick
        SCREEN.fill((128, 128, 128))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
                quit()

        write_text(text1, font, (0, 0, 0), 230, 50, SCREEN)
        write_text(text2, font, (0, 0, 0), 120, 90, SCREEN)
        write_text(text3, font, (0, 0, 0), 230, 130, SCREEN)
        write_text(text4, font, (0, 0, 0), 460, 200, SCREEN)
        write_text(text5, font, (0, 0, 0), 290, 250, SCREEN)
        write_text(text6, font, (0, 0, 0), 180, 290, SCREEN)
        write_text(text7, font, (0, 0, 0), 170, 330, SCREEN)
        write_text(text8, font, (0, 0, 0), 245, 370, SCREEN)
        write_text(text9, font, (0, 0, 0), 230, 410, SCREEN)
        write_text(text10, font, (0, 0, 0), 350, 450, SCREEN)

        next_btn.draw_button(SCREEN)
        if next_btn.click_button():
            RUNNING = False

        pygame.display.update()


def Back():
    Choose_character()


def Menu_screen():
    RUNNING = True

    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Menu")

    # menu screen
    play_img = Rescale_img(pygame.image.load("Play.png"), MENU_BTN_SCALE)
    how_to_play_img = Rescale_img(pygame.image.load("How_to_play.png"), MENU_BTN_SCALE)
    back_img = Rescale_img(pygame.image.load("Back.png"), MENU_BTN_SCALE)
    exit_img = Rescale_img(pygame.image.load("Exit.png"), MENU_BTN_SCALE)
    play_btn = Button(500, 200, play_img, MENU_RECT_X, MENU_RECT_Y)
    how_to_play_btn = Button(500, 300, how_to_play_img, MENU_RECT_X, MENU_RECT_Y)
    back_btn = Button(500, 400, back_img, MENU_RECT_X, MENU_RECT_Y)
    exit_btn = Button(500, 500, exit_img, MENU_RECT_X, MENU_RECT_Y)

    while RUNNING:
        CLOCK.tick(FPS)
        SCREEN.fill((128, 128, 128))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        play_btn.draw_button(SCREEN)
        how_to_play_btn.draw_button(SCREEN)
        back_btn.draw_button(SCREEN)
        exit_btn.draw_button(SCREEN)

        # handles if buttons are pressed
        if play_btn.click_button():
            if DEQUEUED_KEY == 'default':
                Intro_scene(Orc, Coy)
            else:
                Lobby(Orc, Coy)

        elif how_to_play_btn.click_button():
            How_to_play()

        elif back_btn.click_button():
            Back()

        elif exit_btn.click_button():
            RUNNING = False
            quit()

        pygame.display.update()


def Choose_character():
    RUNNING = True
    global SPRITE_LIST
    global Orc
    global Coy
    Orc, Coy = False, False
    SPRITE_LIST = None

    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Choose Character")

    choose_chr_txt = Rescale_img(pygame.image.load("Choose_cha_txt.png"), 7)
    coyote_btn_img = Rescale_img(pygame.image.load("Coyote_button.png"), CHAR_CHOICE_SCALE)
    orcas_btn_img = Rescale_img(pygame.image.load("Orcas_button.png"), CHAR_CHOICE_SCALE)
    coyote_btn = Button(250, 380, coyote_btn_img, CHOOSE_CHAR_RECT_X, CHOOSE_CHAR_RECT_Y)
    orcas_btn = Button(750, 380, orcas_btn_img, CHOOSE_CHAR_RECT_X, CHOOSE_CHAR_RECT_Y)

    while RUNNING:
        CLOCK.tick(FPS)
        SCREEN.fill((128, 128, 128))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False

        SCREEN.blit(choose_chr_txt, (150, 100))
        coyote_btn.draw_button(SCREEN)
        orcas_btn.draw_button(SCREEN)

        if coyote_btn.click_button():
            SPRITE_LIST, Coy = Load_coyote()
            Menu_screen()
        elif orcas_btn.click_button():
            SPRITE_LIST, Orc = Load_orcas()
            Menu_screen()

        pygame.display.update()

    return Orc, Coy


########### The Mystic Key Adventure ###########

if not login_complete():
    open_homepage()
    window.mainloop()

if login_complete():
    DEQUEUED_KEY = correct_key()  # what door user can enter
    Choose_character()

