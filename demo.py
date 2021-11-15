
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
        screen.fill(Color(62,241,100))
        title_surf = Option.font.draw_text('Game Started', 'default_title_font', color=Color(132,37,92))
        title_surf.get_rect().center = screen.get_rect().center
        screen.blit(title_surf, title_surf.get_rect().center)
        Option.input.check_input()
        Option.clock.tick(60)
        display.update()
        Option.input.reset()


def vol_change(option: Option):
    if(Option.input.mouse_wheel[1] < 0):
        option.input_output -= 1
    elif(Option.input.mouse_wheel[1] > 0):
        option.input_output += 1


start = Option('Start').add.highlight(
).add.select_listener(lambda _: start_game())
volume = Option('volume').add.highlight().add.input(
    0).add.active_listener(vol_change)
options = Option('Options').add.menu(screen, TITLE_POS).set_options([
    Option('those are the options..')
]).add.highlight()

options.add.active_listener(vol_change)
menu = Option('menu').add.mouse_menu(screen, TITLE_POS).set_options([
    start,
    volume,
    options
])

menu.display_menu()

# game.vol = volume.input_output
# while(not game.over):
#     ...
