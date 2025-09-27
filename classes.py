import random as rand
import pygame
from constants import *
pygame.init()

####################### CLASSES #############################


class HealthBar:
    def __init__(self, x_pos, y_pos):
        self.__x = x_pos
        self.__y = y_pos
        self.__width = 100
        self.__height = 30

    def draw_health_bar(self, surf, player_health):
        if player_health > 100:
            player_health = 100
        pygame.draw.rect(surf, (255, 0, 0), (self.__x, self.__y, self.__width, self.__height))
        pygame.draw.rect(surf, (0, 255, 0), (self.__x, self.__y, player_health, self.__height))
        pygame.draw.rect(surf, (0, 0, 0), (self.__x, self.__y, self.__width, self.__height), 3)


class Button:
    def __init__(self, x, y, button_img, rect_x, rect_y):
        self.__button_img = button_img  # private
        self.clicked = False  # public
        self.rect = pygame.Rect(0, 0, rect_x, rect_y)
        self.rect.center = (x, y)

    def draw_button(self, surf):
        surf.blit(self.__button_img, self.rect)
        # pygame.draw.rect(surf, (255, 255, 255), self.rect, 1)

    def click_button(self):
        clicked = False
        mouse_position = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_position):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                clicked = True

            elif pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
                clicked = False

        return clicked


class Character:
    def __init__(self, xpos, ypos, sprite_list):
        self.__list = sprite_list  # private
        self._current = 0  # protected
        self.img = self.__list[self._current]
        self.flipped = False
        self.rect = pygame.Rect(0, 0, 50, 50)
        self.rect.center = (xpos, ypos)

    def get_rect(self):  # getter
        return self.rect

    def animate(self, up, down, left, right):  # make char move
        if up or down or left or right:
            self._current += 0.15  # speed of animation
            self.img = self.__list[int(self._current)]  # next img after 7 clicks
            length = len(self.__list) - 1

            if self._current >= length:
                self._current = 0

    def move_character(self, x_change, y_change):

        if x_change > -1:
            self.flipped = False
        elif x_change < 1:
            self.flipped = True

        self.rect.x += x_change
        self.rect.y += y_change

    def draw_character(self, surf):
        player = pygame.transform.flip(self.img, self.flipped, False)
        surf.blit(player, self.rect)
        # pygame.draw.rect(surf, (255, 255, 255), self.rect, 1)


class Guard(Character):  # inheritance
    def __init__(self, xpos, ypos, sprite_list, melee):
        super().__init__(xpos, ypos, sprite_list)
        self.melee_img = melee
        self.angle = 0
        self.clicked = False
        self.character_health = 100
        self.__collide = False

    def get_health(self):  # getter
        return self.character_health

    def get_clicked(self):  # getter
        return self.clicked

    def draw_melee(self, surf):
        melee = pygame.transform.rotate(self.melee_img, self.angle)
        if self.flipped:
            if self.clicked:
                self.angle = 130
                surf.blit(melee, (self.rect.x - 30, self.rect.y + 10))
            else:
                self.angle = 90
                surf.blit(melee, (self.rect.x - 30, self.rect.y + 10))
        else:
            if self.clicked:
                self.angle = 320
                surf.blit(melee, (self.rect.x + 50, self.rect.y + 10))
            else:
                self.angle = 0
                surf.blit(melee, (self.rect.x + 50, self.rect.y + 10))

    def fight(self):
        mouse_position = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_position):
            # left click
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
            elif pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

    def attack(self, surf, enemy_rect, gain_health):
        self.character_health += gain_health
        if self.character_health <= 0:
            print("dead")
        elif self.character_health > 100:
            self.character_health = 100
        elif self.rect.colliderect(enemy_rect):
            self.__collide = True
            if self.__collide and not self.clicked:
                self.__collide = True
                self.character_health -= 1
        else:
            self.__collide = False


class Sorcerer(Character):  # inheritance
    def __init__(self, xpos, ypos, sprite_list, spell, wand):
        super().__init__(xpos, ypos, sprite_list)
        self.angle = 0
        self.spell_img = spell
        self.wand_img = wand
        self.clicked = False
        self.character_health = 80
        self.__collide = False  # private attribute

    def get_health(self):  # getter
        return self.character_health

    def get_clicked(self):  # getter
        return self.clicked

    def draw_wand(self, surf):
        wand = pygame.transform.rotate(self.wand_img, self.angle)
        if self.flipped:
            if self.clicked:
                self.angle = 130
                surf.blit(wand, (self.rect.x - 20, self.rect.y + 20))
            else:
                self.angle = 90
                surf.blit(wand, (self.rect.x - 20, self.rect.y + 20))
        else:
            if self.clicked:
                self.angle = 320
                surf.blit(wand, (self.rect.x + 55, self.rect.y + 20))
            else:
                self.angle = 0
                surf.blit(wand, (self.rect.x + 55, self.rect.y + 20))

    def draw_spell(self, surf):
        spell = pygame.transform.flip(self.spell_img, self.flipped, False)
        if self.flipped:
            if self.clicked:
                surf.blit(spell, (self.rect.x, self.rect.y + 50))
        else:
            if self.clicked:
                surf.blit(spell, (self.rect.x, self.rect.y + 50))

    def cast_spell(self):
        mouse_position = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_position):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
            elif pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

    def attack(self, surf, enemy_rect, gain_health):
        self.character_health += gain_health
        if self.character_health <= 0:
            pass
        elif self.rect.colliderect(enemy_rect):
            self.__collide = True
            if self.__collide and not self.clicked:
                self.__collide = True
                self.character_health -= 1.2
        else:
            self.__collide = False


class Enemy(pygame.sprite.Sprite):  # inherits functions from pygame sprite class
    def __init__(self, enemy, w, h):
        super().__init__()
        self.enemy_health = 100
        self.enemy = enemy
        self.x_pos = rand.randint(100, 1000)  # random pos
        self.y_pos = rand.randint(200, 600)
        self.enemy_rect = pygame.Rect(self.x_pos, self.y_pos, w, h)
        self.__collide = False
        self.mov_x = rand.randint(1, 4)

    def get_enemy_rect(self):
        return self.enemy_rect

    def draw_enemy(self, surf):

        enemy = self.enemy
        surf.blit(enemy, self.enemy_rect)
        # pygame.draw.rect(surf, (0, 0, 0),  self.enemy_rect, 1)

    def attack(self, player_rect, clicked):
        player_gain_health = 0
        if self.enemy_health <= 0:
            self.kill()  # funct from parent class, delete sprite from group
            player_gain_health = 15  # for every enemy killed player gains 15 health

        elif self.enemy_rect.colliderect(player_rect):
            if not self.__collide and clicked:
                self.__collide = True
                self.enemy_health -= rand.randint(1, 10)
            else:
                self.__collide = False

        return player_gain_health

    def scroll(self, cam_x, cam_y):
        self.enemy_rect.x += cam_x
        self.enemy_rect.y += cam_y

    # polymorphism (overwriting default update function from parent sprite class)
    def update(self, width):
        self.enemy_rect.move_ip(self.mov_x, 0)

        if self.enemy_rect.right >= width:
            self.mov_x = -self.mov_x

        if self.enemy_rect.left <= 5:
            self.mov_x = rand.randint(1, 4)


class TilemapSurf:
    def __init__(self):
        self.__tiles = []  # private

    def create_map(self, data, tile_list):

        y_counter = 0
        for row in data:
            x_counter = 0
            for item in row:
                image = tile_list[int(item)]
                image_rect = image.get_rect()

                image_x = x_counter * (16 * TILE_SIZE)  # tiles 16 x 16 pxl
                image_y = y_counter * (16 * TILE_SIZE)

                image_rect.center = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y]

                if int(item) >= 0:
                    self.__tiles.append(tile_data)
                else:
                    pass
                x_counter += 1
            y_counter += 1

    def draw(self, surf):
        for tile in self.__tiles:
            surf.blit(tile[0], tile[1])

    def camera_scroll(self, cam_x, cam_y):
        for tile in self.__tiles:
            tile[2] += cam_x  # 2,3 = x, y pos
            tile[3] += cam_y
            tile[1].center = (tile[2], tile[3])

    def collisions(self, player_rect, tile_list, x, y):

        for tile in self.__tiles:
            if tile[0] == tile_list[4] or tile[0] == tile_list[5]:  # wall sprites
                if tile[1].colliderect(player_rect):

                    if x < 0:
                        player_rect.left = tile[1].right
                    elif x > 0:
                        player_rect.right = tile[1].left

                    elif y > 0:
                        player_rect.bottom = tile[1].top
                    elif y < 0:
                        player_rect.top = tile[1].bottom


class Collectables(pygame.sprite.Sprite):
    def __init__(self, item_id, img, xpos, ypos, w, h):
        super().__init__()
        self._item_id = item_id  # protected
        self.img = img
        self.x_pos = xpos
        self.y_pos = ypos
        self.item_rect = pygame.Rect(self.x_pos, self.y_pos, w, h)
        self.collide = False

    def draw(self, surf):
        surf.blit(self.img, self.item_rect)
        # pygame.draw.rect(surf, (255, 255, 255), self.item_rect, 1)

    def scroll(self, cam_x, cam_y):
        self.item_rect.x += cam_x
        self.item_rect.y += cam_y

    def spell_book(self, player):
        touch = False

        if self._item_id == BOOK_ID and player.clicked:
            touch = True

        return touch

    def complete(self, complete):
        if complete:
            self.kill()  # method from parent sprite class

    def collect_key(self, player_rect, key_queue, dequeued_key):

        if self.item_rect.colliderect(player_rect):
            if self._item_id == KEY_ID:
                dequeued_key = key_queue.popleft()  # FIFO
                self.kill()
                print("found", dequeued_key)

        return key_queue, dequeued_key

    def drink(self, player):

        if self.item_rect.colliderect(player.rect):

            if self._item_id == 3:  # blue potion restores 50 health
                player.character_health += 50
                self.kill()  # del sprite from group - inherits from parent sprite class

            elif self._item_id == 2:  # red potion restores 10 - 100  health
                health = rand.randint(10, 100)
                player.character_health += health
                self.kill()

    def enter_red_door(self, player):
        enter = False
        if self._item_id == R_DOOR_ID:
            if self.item_rect.colliderect(player.rect) and player.clicked:
                enter = True
        return enter

    def enter_blue_door(self, player, dequeued_key):
        enter = False
        if self._item_id == B_DOOR_ID and dequeued_key == "blue":
            if self.item_rect.colliderect(player.rect) and player.clicked:
                enter = True
                print("enter blue door")
        return enter

    def enter_green_door(self, player, dequeued_key):
        enter = False
        if self._item_id == G_DOOR_ID and dequeued_key == "green":
            if self.item_rect.colliderect(player.rect) and player.clicked:
                enter = True
                print("enter green door")
        return enter

    def enter_yellow_door(self, player, dequeued_key):
        enter = False
        if self._item_id == Y_DOOR_ID and dequeued_key == "yellow":
            if self.item_rect.colliderect(player.rect) and player.clicked:
                enter = True
                print("enter yellow door")
        return enter

    def enter_pink_door(self, player, dequeued_key):
        enter = False
        if self._item_id == P_DOOR_ID and dequeued_key == "pink":
            if self.item_rect.colliderect(player.rect) and player.clicked:
                enter = True
                print("enter pink door")
        return enter


class DraggableItem:
    def __init__(self, img, x, y, identifier):
        self.id = identifier  # protected
        self.img = img
        self.item_rect = pygame.Rect(0, 0, 100, 100)
        self.item_rect.center = (x, y)
        self.position = (x, y)
        self.drag = False

    def get_node(self):
        if self.id == 1:
            return "coin"
        if self.id == 2:
            return "scroll"
        if self.id == 3:
            return "silver"
        if self.id == 4:
            return "blade"

    def draw(self, surf):
        surf.blit(self.img, self.item_rect)
        # pygame.draw.rect(surf, (255, 255, 255), self.item_rect, 1)

    def update(self):
        if self.drag:
            self.position = pygame.mouse.get_pos()
            self.item_rect.center = pygame.mouse.get_pos()
        if not self.drag:
            return self.item_rect.center


class Node:
    def __init__(self, item, identifier):
        self.item = item
        self.next = None
        self.prev = None  # double ll
        self.identifier = identifier  # dictionary key


class LinkedList:
    def __init__(self):
        self.__head = None
        self.__tail = None  # double ll
        self._size = 0  # protected attribute
        self._dict = {}  # dict reduce traversal (protected)

    def append_ll(self, item, identifier):  # add new node to end of ll

        # duplicate check
        current = self.__head
        while current:
            if current.identifier == identifier:
                return False  # exit if duplicate is found
            current = current.next

        new_node = Node(item, identifier)  # composition

        if not self.__head:  # if empty
            self.__head = new_node
            self.__tail = new_node

        else:  # not empty
            new_node.prev = self.__tail
            self.__tail.next = new_node
            self.__tail = new_node
        self._size += 1

    def insert_ll(self, item, identifier, position):
        # dupes check
        current = self.__head
        while current:
            if current.identifier == identifier:
                return False
            current = current.next

        if position < 0 or position > self._size:
            return False

        new_node = Node(item, identifier)

        # empty
        if self.__head is None:
            self.__head = new_node
            self.__tail = new_node

        else:
            if position == 0:  # insert beginning
                new_node.next = self.__head
                self.__head.prev = new_node
                self.__head = new_node

            elif position == self._size:  # insert end
                new_node.prev = self.__tail
                self.__tail.next = new_node
                self.__tail = new_node

            else:  # insert insert middle
                current = self.__head
                for i in range(position):
                    current = current.next
                new_node.next = current
                new_node.prev = current.prev
                current.prev.next = new_node
                current.prev = new_node

        self._size += 1
        self._dict[identifier] = new_node  # key = id

    def remove_ll(self, identifier):
        try:
            if self.__head is None:
                return False

            current = self.__head
            while current:  # traverse
                if current.identifier == identifier:
                    break
                current = current.next

            # not in ll
            if current is None:
                return False

            # del only node
            if self._size == 1:
                self.__head = None
                self.__tail = None

            # node = head
            elif current == self.__head:
                self.__head = current.next
                self.__head.prev = None

            # node = tail
            elif current == self.__tail:
                self.__tail = current.prev
                self.__tail.next = None

            # node in middle
            else:
                current.prev.next = current.next
                current.next.prev = current.prev

            self._size -= 1
            del self._dict[identifier]  # del from dict

        except:
            pass

    def display_ll(self):
        items_list = []
        current = self.__head
        while current:
            items_list.append(current.item)
            current = current.next
        return items_list

