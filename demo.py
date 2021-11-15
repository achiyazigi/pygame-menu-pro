from os import link
from pygame import display
from pygame_menu_pro import *
import pygame

pygame.init()
pygame.display.set_caption('title')
WIDTH = 1080
HEIGHT = WIDTH//1.6
WINDOW_SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(WINDOW_SIZE, depth=32)
TITLE_POS = (screen.get_width()//2, screen.get_height()//4)

Option.font.set_default_option(pygame.font.SysFont('Comic Sans MS', 50))
Option.font.set_default_title(pygame.font.SysFont('Plaguard-ZVnjx', 80))
Option.font.set_default_highlight(
    pygame.font.SysFont('Comic Sans MS', 50, bold=True))


def start_game():
    menu.run_display = False
    while(True):
        pygame.draw.rect(screen, Color(255, 255, 255), Rect(100, 100, 50, 50))
        Option.clock.tick(60)
        display.update()


def vol_change(option: Option):
    if(Option.input.mouse_wheel[1] < 0):
        option.input_output -= 1
    elif(Option.input.mouse_wheel[1] > 0):
        option.input_output += 1


start = Option('Start').add.highlight(
).add.select_listener(lambda _: start_game())
volume = Option('volume').add.highlight().add.input(
    0).add.active_listener(vol_change)
options = Option('Options').add.input(0).add.menu(screen, TITLE_POS).set_options([
    Option('those are the options..')
]).add.highlight()
# Menu(Input(Option))
options.add.active_listener(vol_change)
menu = Option('menu').add.menu(screen, TITLE_POS).set_options([
    start,
    volume,
    options
])
menu = MouseMenu(menu._option, menu._surface, menu._title_pos,
                 menu.title_font_str, menu._options, menu._background_color, menu.cursor)
menu.display_menu()

# game.vol = volume.input_output
# while(not game.over):
#     ...
