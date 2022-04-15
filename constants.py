import pygame
import os 
pygame.font.init()

CAPTION = 'LASER DEFENSE'
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

LEVEL_TIME = 30 #seconds
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 10 # can be increased with bullet count upgrade
SPAWN_ZONE_SIZE = 100
BASE_HEIGHT, BASE_WIDTH = HEIGHT, 30
BASE = pygame.Rect(0, HEIGHT//2 - BASE_HEIGHT//2, BASE_WIDTH, BASE_HEIGHT) # base to protect

HERO_WIDTH, HERO_HEIGHT = 40, 40
MONSTER_SIZE = 40//3
HERO_START_X, HERO_START_Y = BASE_WIDTH + HERO_WIDTH + 10, HEIGHT//2 - HERO_HEIGHT//2 
GUN_LENGTH, GUN_WIDTH = 20, 4
BULLET_HEIGHT, BULLET_WIDTH = 10, 4
SKILL_WIDTH = 24 #bullets
MANA_BAR_HEIGHT = 20
MAX_HEALTH, MAX_MANA = 20, 150
SKILL_MANA_COST = 20
MANA_REFRESH_RATE = 0.2
BULLET_REFRESH_RATE = 1/30
BULLET_MANA_COST = 5
ITEM_PRICES = {'Health Stone': 100, 'Power Stone':100, 'Electric Wall':250}
#FONTS
GENERAL_FONT_SIZE = 25
MANA_FONT_SIZE = 15
GOLD_FONT_SIZE = 20
GENERAL_FONT = pygame.font.SysFont('comicsans', GENERAL_FONT_SIZE)
MANA_FONT = pygame.font.SysFont('comicsans', MANA_FONT_SIZE)
GOLD_FONT = pygame.font.SysFont('comicsans', GOLD_FONT_SIZE)

#IMAGES
SYMBOL_WIDTH, SYMBOL_HEIGHT = 40, 40
ITEM_WIDTH, ITEM_HEIGHT = 100, 100
SPACE_IMAGE = pygame.image.load(os.path.join('Assets','space.png'))
SPACE_IMAGE = pygame.transform.scale(SPACE_IMAGE, (WIDTH,HEIGHT))
HEART_IMAGE = pygame.image.load(os.path.join('Assets','heart.png'))
HEART_IMAGE = pygame.transform.scale(HEART_IMAGE, (SYMBOL_WIDTH,SYMBOL_HEIGHT))
POWER_IMAGE = pygame.image.load(os.path.join('Assets','power.png'))
POWER_IMAGE = pygame.transform.scale(POWER_IMAGE, (SYMBOL_WIDTH,SYMBOL_HEIGHT))
GOLD_IMAGE = pygame.image.load(os.path.join('Assets','gold.png'))
GOLD_IMAGE = pygame.transform.scale(GOLD_IMAGE, (SYMBOL_WIDTH,SYMBOL_HEIGHT))
LASER_IMAGE = pygame.image.load(os.path.join('Assets','laser.png'))
LASER_IMAGE = pygame.transform.scale(LASER_IMAGE, (ITEM_WIDTH,ITEM_HEIGHT))
ELECTRIC_IMAGE = pygame.image.load(os.path.join('Assets','electric_wall.png'))
ELECTRIC_IMAGE = pygame.transform.scale(ELECTRIC_IMAGE, (SYMBOL_WIDTH,SYMBOL_HEIGHT))


#SAVED COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 0 , 0)
MAGENTA = (255, 0, 255)
HERO_COLOR = (150, 150, 0)
DEEP_SKY_BLUE = (0,191,255)
#SOUNDS
#BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
#BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))