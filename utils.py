import pygame
import easygui
from constants import *
import random


class hero_class(pygame.Rect):
    def __init__(self, left, top, width, height):
        super().__init__(left, top, width, height)
        self.gold = 0
        self.health = MAX_HEALTH
        self.mana = MAX_MANA
        self.max_health = MAX_HEALTH
        self.max_mana = MAX_MANA
        self.laser = False # becomes true after buying the laser upgrade
        self.bullets = MAX_BULLETS
        self.max_bullets = MAX_BULLETS
        self.electric_walls = 0

    def create_bullet(self, shift):
        return pygame.Rect(self.x + self.width,
                        self.y + self.height//2 - BULLET_WIDTH//2 + shift,
                        BULLET_HEIGHT//2,
                        BULLET_WIDTH)

def handle_hero_movement(keys_pressed, hero):

    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_a] and hero.x - VEL > 0: #LEFT
        hero.x -= VEL
    if keys_pressed[pygame.K_d] and hero.x + hero.width + VEL < WIDTH: #RIGHT
        hero.x += VEL
    if keys_pressed[pygame.K_w] and hero.y - VEL > 0: #UP
        hero.y -= VEL
    if keys_pressed[pygame.K_s] and hero.y + hero.height + VEL + 15 < HEIGHT: #DOWN
        hero.y += VEL

def handle_big_bullets(big_bullets, monster_dict, hero):

    monsters_to_remove = []
    for bullet in big_bullets:
        bullet.x += BULLET_VEL
        for monster_id in monster_dict:
            if monster_dict[monster_id].colliderect(bullet):
                monsters_to_remove.append(monster_id)

    big_bullets[:] = [bullet for bullet in big_bullets if bullet.x < WIDTH]

    for monster_id in monsters_to_remove:
        if monster_id not in monster_dict: continue #monster could've been added multiple times.
        hero.gold += 1
        del monster_dict[monster_id]

def handle_bullets(bullets, monster_dict, hero):

    bullets_to_remove = []
    monsters_to_remove = []
    for bullet in bullets:
        bullet.x += BULLET_VEL
        for monster_id in monster_dict:
            if monster_dict[monster_id].colliderect(bullet):
                monsters_to_remove.append(monster_id)
                bullets_to_remove.append(bullet)
                
    bullets[:] = [bullet for bullet in bullets if bullet.x < WIDTH and
                        bullet not in bullets_to_remove]

    for monster_id in monsters_to_remove:
        if monster_id not in monster_dict: continue #monster could've been added multiple times.
        hero.gold += 1
        del monster_dict[monster_id]

def generate_monster(monster_dict, vertical_random=5):
    
    x_coord = WIDTH - SPAWN_ZONE_SIZE + random.randint(-vertical_random,vertical_random)
    y_coord = HEIGHT//2 + random.randint(-50,50)

    new_monster = pygame.Rect(x_coord, y_coord, MONSTER_SIZE, MONSTER_SIZE)
    new_key = len(monster_dict)
    while new_key in monster_dict:
        new_key += 1
    monster_dict[new_key]= new_monster

def draw_monsters(monster_dict, color):
    for monster in monster_dict.values():
        pygame.draw.rect(WIN, color, monster) #draw one monster
        pygame.draw.rect(WIN, BLACK, monster, width=1) #border

def move_monsters(monster_dict, velocity=1, jump_prob=2):
    for monster in monster_dict.values():
        monster.x -= velocity #move left every frame
        
        if random.randint(1,100) < jump_prob:
            monster.x -= 10*velocity # 10% jump prob. 
        
        direction = random.choice([-1, -2, 1, 2]) #for y axis
        delta = direction*velocity
        if random.randint(1,100) < jump_prob:
            delta *= 5 # 10% jump prob.
              
        if direction > 0: #going down
            if monster.y + monster.height + delta >= HEIGHT:
                delta *= -1 
        elif direction < 0: #going up
            if monster.y + delta < 0:
                delta *= -1
        
        monster.y += delta
        
def draw_bar(value, x=250, y=25, bar_height=MANA_BAR_HEIGHT,
            bar_length=100, max_value=MAX_MANA, color=BLUE):
    window = pygame.Rect(x, y, bar_length, bar_height)
    bar = pygame.Rect(x, y, int(bar_length*(value/max_value)), bar_height)
    pygame.draw.rect(WIN, BLACK, window)
    pygame.draw.rect(WIN, color, bar)   
    pygame.draw.rect(WIN, BLACK, window, width=3)
    display_text = str(int(value)) + '/' + str(max_value)
    text = MANA_FONT.render(display_text, 1, WHITE)
    text_width, text_height = GENERAL_FONT.size(display_text)
    WIN.blit(text, (x + bar_length//3, y))

def draw_health_mana_gold(hero: hero_class):
    WIN.blit(GOLD_IMAGE, (360, 25))
    gold_text = GOLD_FONT.render(str(hero.gold), 1, WHITE)
    WIN.blit(gold_text, (405, 25))

    WIN.blit(ELECTRIC_IMAGE, (470, 25))
    bullet_text = GOLD_FONT.render(str(hero.electric_walls), 1, WHITE)
    WIN.blit(bullet_text, (515, 25))

    WIN.blit(POWER_IMAGE, (200,25))
    draw_bar(value=hero.mana, x=250, y=25, max_value=hero.max_mana)

    WIN.blit(HEART_IMAGE, (40,25))
    draw_bar(value=hero.health, x=90, y=25, max_value=hero.max_health, color=RED)

    

def draw_texts(hero, level, remaining_seconds):
    time_text = GENERAL_FONT.render("Time: {}".format(remaining_seconds), 1, WHITE)
    WIN.blit(time_text, (670, 10))
    level_text = GENERAL_FONT.render("Level: {}".format(level), 1, WHITE)
    WIN.blit(level_text, (790, 10))
    
def update_health(monster_dict, hero, level):
    if len(monster_dict) != 0: #no monsters, health is the same.
        idx_to_remove = []
        for idx, monster in monster_dict.items():
            if monster.colliderect(BASE):
                if level < 8:
                    hero.health -= 1 #reduce health by one for each collision with base
                else:
                    hero.health -=2
                    hero.mana -= 25
                    hero.gold -= 10
                    hero.mana = max(0, 25, hero.mana)
                    hero.gold = max(0, hero.gold)
                idx_to_remove.append(idx)#remove to prevent double count

        for idx in idx_to_remove:
            del monster_dict[idx]

def display_end_text():
    end_text = GENERAL_FONT.render("GAME OVER", 1, WHITE)
    WIN.blit(end_text, (WIDTH//3, HEIGHT//3))    
        
def pause(seconds=3):
    pygame.time.delay(1000*seconds)

def draw_bases(level):
    pygame.draw.rect(WIN, GREEN, BASE)
    pygame.draw.rect(WIN, BLACK, BASE, width=3)

    if level >= 10:
        draw_button(0, 100, text='O', width=BASE_WIDTH, height=BASE_WIDTH, color=MAGENTA)
        draw_button(0, 150, text='O', width=BASE_WIDTH, height=BASE_WIDTH, color=MAGENTA)
        draw_button(0, 200, text='O', width=BASE_WIDTH, height=BASE_WIDTH, color=MAGENTA)
        draw_button(0, 250, text='O', width=BASE_WIDTH, height=BASE_WIDTH, color=MAGENTA)
        draw_button(0, 300, text='O', width=BASE_WIDTH, height=BASE_WIDTH, color=MAGENTA)

    middle_spawn_zone = pygame.Rect(WIDTH-SPAWN_ZONE_SIZE, HEIGHT//2-SPAWN_ZONE_SIZE//2, SPAWN_ZONE_SIZE, SPAWN_ZONE_SIZE)
    pygame.draw.rect(WIN, RED, middle_spawn_zone)
    pygame.draw.rect(WIN, BLACK, middle_spawn_zone, width=5) #to draw borders

def draw_bullets(bullets, color):
    for bullet in bullets:
        pygame.draw.rect(WIN, color, bullet)

def display_level_text(level):
    text = GENERAL_FONT.render("NEXT UP: Level {}!".format(level), 1, WHITE)
    WIN.blit(text, (WIDTH//2 - GENERAL_FONT_SIZE//2 - 100,
                    HEIGHT//2 - GENERAL_FONT_SIZE//2))
    pygame.display.update()

def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))

    pygame.display.update()
    pygame.time.delay(1000)

def draw_hero(hero):
    pygame.draw.rect(WIN, WHITE, hero) #draw hero image
    pygame.draw.rect(WIN, BLACK, hero, width=2) #draw hero border
    bottom_gun = pygame.Rect(hero.x + hero.width//2 - GUN_WIDTH//2,
                            hero.y + hero.height, GUN_WIDTH, GUN_LENGTH)
    bottom_gun_nozzle = pygame.Rect(hero.x + hero.width//2 - GUN_WIDTH//2,
                                    hero.y + hero.height + GUN_LENGTH,
                                    GUN_LENGTH,
                                    GUN_WIDTH)
    pygame.draw.rect(WIN, WHITE, bottom_gun)
    pygame.draw.rect(WIN, BLACK, bottom_gun, width=1)
    pygame.draw.rect(WIN, WHITE, bottom_gun_nozzle)
    pygame.draw.rect(WIN, BLACK, bottom_gun_nozzle, width=1)

    small_gun = ((hero.x + hero.width, hero.y + hero.height + GUN_LENGTH-10),
                 (hero.x + hero.width, hero.y + hero.height + GUN_LENGTH+10),
                 (hero.x + hero.width + 10, hero.y + hero.height + GUN_LENGTH)
    )
    
    pygame.draw.polygon(WIN, GREEN, small_gun) 

    big_gun = ((hero.x + hero.width, hero.y),
                 (hero.x + hero.width, hero.y + hero.height),
                 (hero.x + hero.width + GUN_LENGTH, hero.y + hero.height//2)
    )
    
    pygame.draw.polygon(WIN, GREEN, big_gun)


def draw_button(x, y, text, width=250, height=50, color=GREEN):
    button = pygame.Rect(x, y, width, height)
    pygame.draw.rect(WIN, color, button)
    pygame.draw.rect(WIN, BLACK, button, width=3)
    display_text = GENERAL_FONT.render(text, 1, BLACK)
    text_width, text_height = GENERAL_FONT.size(text)
    WIN.blit(display_text, (x+width//2-text_width//2, y))
    return button

def run_main_menu():
    pygame.mixer.init()
    pygame.mixer.music.load('./Assets/main_menu.wav')
    pygame.mixer.music.play(-1)
    run = True
    game_title = 'LASER DEFENSE'
    display_text = GENERAL_FONT.render(game_title, 1, WHITE)
    text_width, text_height = GENERAL_FONT.size(game_title)
    while run:
        
        WIN.blit(SPACE_IMAGE, (0,0))
        WIN.blit(display_text, (WIDTH//2 - text_width//2, 50))
        button_width = 250
        start_game = draw_button(WIDTH//2-button_width//2, 150, text='start game', width=button_width)
        options = draw_button(WIDTH//2-button_width//2, 225, text='options', width=button_width)       
        quit_button = draw_button(WIDTH//2-button_width//2, 300, text='quit', width=button_width)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if start_game.collidepoint(pos):
                    run = False
                if options.collidepoint(pos):
                    show_options()
                if quit_button.collidepoint(pos):
                    pygame.quit()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()                

def show_options():
    run = True
    game_title = 'LASER DEFENSE'
    display_text = GENERAL_FONT.render(game_title, 1, WHITE)
    text_width, text_height = GENERAL_FONT.size(game_title)
    while run:
        
        WIN.blit(SPACE_IMAGE, (0,0))
        WIN.blit(display_text, (WIDTH//2 - text_width//2, 50))
        button_width = 250
        main_menu = draw_button(100, 400, text='main menu', width=button_width)

        draw_button(100, 100, text='MOVE UP: W', width=button_width, color=BLUE)
        draw_button(100, 150, text='MOVE DOWN: S', width=button_width, color=BLUE)
        draw_button(100, 200, text='MOVE RIGHT: D', width=button_width, color=BLUE)
        draw_button(100, 250, text='MOVE LEFT: A', width=button_width, color=BLUE)
        draw_button(500, 100, text='BULLET: K', width=button_width, color=BLUE)
        draw_button(500, 150, text='LASER: L', width=button_width, color=BLUE)
        draw_button(500, 200, text='ELECTRIC WALL: O', width=button_width, color=BLUE)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if main_menu.collidepoint(pos):
                    run = False
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

def draw_upgrade_window(level, UPGRADE_DICT, hero):
    if UPGRADE_DICT[level] == False:
        if level == 5:
            image = './Assets/laser.png'
            msg = '''
                Congratulations, you have reached level 5! \n
                You have unlocked your ship's laser weapon. To use it,
                you need to press the "L" button on your keyboard.
                Each shot consumes 20 power points, so you should
                use it wisely.
                '''
            choices = ["Continue"]
            reply = easygui.buttonbox(msg, choices=choices, image=image)
            hero.laser = True
      
        if level == 8:
            if UPGRADE_DICT[8] == False:
                easygui.msgbox('''
                                You have made it to level 8. Beware, the
                                aliens are now more powerful! If an alien
                                reaches the gate, you will instantly lose
                                2 Health, 25 Power and 10 Gold.
                            ''', image='./Assets/angry_alien.png')

        if level == 10:
            image = './Assets/tower.png'
            msg = '''
                Congratulations, you have reached level 10! \n
                The aliens are now much faster, but do not worry,
                Because your gate now has protective towers.
                The shooting occurs automatically and at random
                times. It will not cost you any power and you don't
                have to do anything to control this. Good luck!
                '''
            choices = ["Continue"]
            reply = easygui.buttonbox(msg, choices=choices, image=image)
            hero.laser = True

    UPGRADE_DICT[level] = True


def draw_shop_window(level, hero):
    
    title = 'THE MERCHANT'
    image = './Assets/shop_image.png'
    msg = '''
        Welcome to the shop. \n
        What would you like to buy? You currently have {} gold. \n
        -Health Stone: Increases your maximum health by 10.
        -Power Stone: Increases your maximum power by 50.
        -Electric Wall: Creates an electric wall which slides across the
                        map, killing any enemy units it touches.
                        Press "O" to use.
        '''.format(hero.gold)
    choices = ["Health Stone","Power Stone", "Electric Wall", "Continue to Next Level"]
    reply = easygui.buttonbox(msg, title, choices=choices, image=image)

    if reply == image: # pressing image returns image path.
        easygui.msgbox("Please click the buttons below to buy!")
        draw_shop_window(level, hero)
    elif reply in ITEM_PRICES: # pressing x returns None.
        item_cost = ITEM_PRICES[reply]
        if item_cost > hero.gold:
            easygui.msgbox("Not enough gold!")
        elif reply == 'Health Stone':
            hero.max_health += 10
            hero.health += 10
            hero.gold -= item_cost
            easygui.msgbox("Your maximum health increased from {} to {}!".format(hero.max_health-10, hero.max_health))
        elif reply == 'Power Stone':
            hero.max_mana += 50
            hero.mana += 50
            hero.gold -= item_cost
            easygui.msgbox("Your maximum health increased from {} to {}!".format(hero.max_mana-50, hero.max_mana))
        elif reply == 'Electric Wall':
            hero.electric_walls += 1
            hero.gold -= item_cost
            easygui.msgbox("Your now have {} electric walls!".format(hero.electric_walls))
        
        draw_shop_window(level, hero)

def draw_shop_button():
    shop_button = pygame.Rect(560,15,100,50)
    pygame.draw.rect(WIN, GREEN, shop_button)
    pygame.draw.rect(WIN, BLACK, shop_button, width=3)
    display_text = GENERAL_FONT.render("Shop", 1, BLACK)
    WIN.blit(display_text, (570,15))
    pygame.display.update()