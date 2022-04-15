import pygame
import os
from constants import *
from utils import *
import easygui

pygame.display.set_caption(CAPTION)

def draw_window(hero, bullets, big_bullets, electric_bullets,
                tower_bullets, monster_dict, level, display_new_level,
                remaining_seconds):
    
    WIN.blit(SPACE_IMAGE, (0,0))
    draw_bases(level)
    if UPGRADE_DICT[8] == False:
        draw_monsters(monster_dict, color=WHITE)
    else:
        draw_monsters(monster_dict, color=GREEN)   
    draw_hero(hero)
    draw_health_mana_gold(hero)
    draw_texts(hero, level, remaining_seconds)
    #draw_shop_button()
    
    draw_bullets(bullets, color=GREEN)
    draw_bullets(big_bullets, color=MAGENTA)
    draw_bullets(electric_bullets, color=DEEP_SKY_BLUE)
    draw_bullets(tower_bullets, color=MAGENTA)

    if hero.health <= 0:
        display_end_text()
        pygame.display.update()
        pause()
        run_main_menu()
        main()

    pygame.display.update()
    
    if display_new_level:
        display_level_text(level)
        pause(seconds=2)
        if level == 20:
            easygui.msgbox(
            '''If you have come this far, maybe should stop playing!
                But keep going if you want :) ''')
        
        if level in UPGRADE_DICT:
            draw_upgrade_window(level, UPGRADE_DICT, hero)

        draw_shop_window(level, hero)
        monster_dict.clear() #remove monsters from screen
        bullets.clear() #remove bullets from screen
        big_bullets.clear()
        hero.x, hero.y = HERO_START_X, HERO_START_Y #hero back to start position
        hero.health, hero.mana = hero.max_health, hero.max_mana

def main():
    pygame.mixer.init()
    pygame.mixer.music.load('./Assets/laser_defence.mp3')
    pygame.mixer.music.play(-1)
    monster_gen_rate = 2 #add new monster every 30 frames
    monster_vel = 1 #monsters randomly move 2 pixels every frame
    monster_dict = dict()
    hero = hero_class(left=HERO_START_X, top=HERO_START_Y,
                        width=HERO_WIDTH, height=HERO_HEIGHT)
    level = 1
    time_variable = 0
    bullets, big_bullets, electric_bullets, tower_bullets = [], [], [], []
    clock = pygame.time.Clock()
    remaining_seconds = LEVEL_TIME+1
    run = True
    upgrade_window = False
    shop_button = pygame.Rect(560,15,100,50)
    vertical_random = 5

    while run:
        clock.tick(FPS)
        display_new_level = False
        time_variable = (time_variable + 1) % FPS
        if time_variable == 1: #generate at the first frame of every second
            remaining_seconds -= 1
            for _ in range(monster_gen_rate):
                generate_monster(monster_dict, vertical_random)
            
        if level >= 10 and time_variable in [20, 40, 60]: #tower bullets
            tower_y_coord = 125 + random.randint(1,4)*50
            new_bullet = pygame.Rect(BASE_WIDTH//2, tower_y_coord, BULLET_HEIGHT, BULLET_WIDTH)
            tower_bullets.append(new_bullet)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k and hero.mana >= BULLET_MANA_COST:
                    hero.mana -= BULLET_MANA_COST
                    bullet = pygame.Rect(hero.x + hero.width + 10,
                                        hero.y + hero.height + GUN_LENGTH - BULLET_WIDTH//2,
                                        BULLET_HEIGHT, BULLET_WIDTH)
                    bullets.append(bullet)
                if (event.key == pygame.K_l and 
                    hero.mana >= SKILL_MANA_COST and 
                    hero.laser): #laser is opened at level 5
                    hero.mana -= SKILL_MANA_COST
                    for shift in range(-SKILL_WIDTH//2,SKILL_WIDTH//2+1):
                        bullet = hero.create_bullet(shift)
                        big_bullets.append(bullet)
                if event.key == pygame.K_o and hero.electric_walls > 0: #shoot electric wall
                    hero.electric_walls -= 1
                    for shift in range(-2*SKILL_WIDTH,2*SKILL_WIDTH+1):
                        bullet = hero.create_bullet(shift)
                        electric_bullets.append(bullet)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if shop_button.collidepoint(pos):
                    draw_shop_window(level, UPGRADE_DICT, hero)

        keys_pressed = pygame.key.get_pressed()
        handle_hero_movement(keys_pressed, hero)

        update_health(monster_dict, hero, level)
        move_monsters(monster_dict, velocity=monster_vel)
        handle_bullets(bullets, monster_dict, hero)
        handle_bullets(tower_bullets, monster_dict, hero)
        handle_big_bullets(big_bullets, monster_dict, hero)
        handle_big_bullets(electric_bullets, monster_dict, hero)
        hero.mana = max(0, min(hero.max_mana, hero.mana + MANA_REFRESH_RATE))
        hero.bullet = min(hero.max_bullets, hero.bullets + 2) #2 bullets per second
        
        if remaining_seconds == 0:
            remaining_seconds = LEVEL_TIME
            level += 1
            display_new_level = True
            monster_gen_rate += 1  #gen rate +1 every level
            if level % 10 == 0:
                monster_vel += 1
            if level % 3 == 0:
                vertical_random += 1

        draw_window(hero, bullets, big_bullets, electric_bullets, tower_bullets,
        monster_dict, level, display_new_level, remaining_seconds)
        
if __name__ == '__main__':
    UPGRADE_DICT = {5: False, 8:False, 10:False}
    run_main_menu()
    main()
