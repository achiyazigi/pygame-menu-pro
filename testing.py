import pygame

from pygame_menu_pro import *

clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('title')
WIDTH = 1080
HEIGHT = WIDTH//1.6
WINDOW_SIZE = (WIDTH, HEIGHT)
CREDITS_TEXT = """
    those are the credits...
    if you want to see more please visit my
    github profile every once in a while to get the
    most updated versions of my libraries...
    thank you for choosing to develope with my art."""

screen = pygame.display.set_mode(WINDOW_SIZE, depth=32)
TITLE_POS = (screen.get_width()//2, screen.get_height()//4)

Option.font.set_default_option(pygame.font.SysFont('Comic Sans MS', 50))
Option.font.set_default_title(pygame.font.SysFont('Plaguard-ZVnjx', 80))
Option.font.set_default_highlight(
    pygame.font.SysFont('Comic Sans MS', 50, bold=True))

Option.font.add_font('credits_font', pygame.font.SysFont('Plaguard-ZVnjx', 30))
Option.font.add_font('link_font', pygame.font.SysFont('Arial', 30))
Option.font.add_font('highlight_link_font',
                     pygame.font.SysFont('Arial', 30, bold=True))


def exit_menu(menu: Menu):
    menu.run_display = False
    Option.input.reset_last_checked()


cursor = Option.font.get_font('default_option_font').render(
    '*', True, Color(255, 255, 255))

start = Option('Start')\
    .add.highlight()

quit = Option('Quit')\
    .add.highlight()\
    .add.select_listener(lambda _: exit_menu(menu))

credits = Option('Credits', color=Color(200, 100, 42)).add.highlight(
).add.menu(screen, TITLE_POS, background_color=Color(165, 211, 97))


def skip_me(menu: Menu):
    if(menu.up in Option.input.last_checked_input):
        menu.state -= 1
    elif(menu.down in Option.input.last_checked_input):
        menu.state += 1
    menu.state %= len(menu.get_options())


credits_link = Option('https://github/achiyazigi', 'link_font')\
    .add.highlight('highlight_link_font')

credits_text = Option(CREDITS_TEXT, 'credits_font', color=Color(35, 71, 100))\
    .add.active_listener(lambda _: skip_me(credits))

credits_back = Option('Back')\
    .add.highlight()\
    .add.select_listener(lambda _: exit_menu(credits))

graphics_list = ['Low', 'Medium', 'High', 'Ultra']


def volume_adjustment(option: InputOption):
    if(K_LEFT in Option.input.last_checked_input):
        option.input_output -= 1
    elif(K_RIGHT in Option.input.last_checked_input):
        option.input_output += 1


volume = Option('Volume:')\
    .add.highlight()\
    .add.input(0)\
    .add.active_listener(volume_adjustment)\
    .add.select_listener(lambda _: print(volume.input_output))


def graphics_adjustment(option: InputOption):
    shift = 0
    index = graphics_list.index(option.input_output)
    if(option.left in Option.input.last_checked_input):
        shift = -1
    elif(option.right in Option.input.last_checked_input):
        shift = 1
    option.input_output = graphics_list[(index + shift) % len(graphics_list)]


graphics = Option('Graphics:')\
    .add.input(graphics_list[0])\
    .add.active_listener(graphics_adjustment)

back = Option('Back')\
    .add.highlight()\
    .add.select_listener(lambda _: exit_menu(options))


menu = Option('Main Menu')\
    .add.menu(screen, TITLE_POS, cursor=cursor)

options = Option('Options')\
    .add.highlight()\
    .add.activation_key(K_SPACE)\
    .add.input(':)')\
    .add.menu(screen, TITLE_POS, background_color=Color(75, 23, 175), cursor=cursor)


menu.cursor_offset = -20
options.cursor_offset = -20


def voip_toggle(option: InputOption):
    option.input_output = not option.input_output


simple_music_toggle = Option('voip:')\
    .add.input(True)\
    .add.select_listener(voip_toggle)


def adv_simp_toggle(option: Menu):
    if(K_SPACE in Option.input.last_checked_input):
        if(option.text == 'Advanced Options'):
            option.text = 'Simple Options'
            option.set_options([
                simple_music_toggle
            ])
        elif(option.text == 'Simple Options'):
            option.text = 'Advanced Options'
            option.set_options([
                Option('FPS'),
                Option('Dark Mode'),
                Option('Choose server:...')
            ])


advanced = Option('Advanced Options')\
    .add.highlight()\
    .add.menu(screen, TITLE_POS)\
    .set_options([
        Option('Back')
        .add.select_listener(lambda _: exit_menu(advanced))
    ])\
    .add.active_listener(adv_simp_toggle)


menu.set_options([
    start,
    options,
    credits,
    quit
])

options.set_options([
    volume,
    graphics,
    advanced,
    back
])
credits.set_options([
    credits_link,
    credits_text,
    credits_back
])


menu.display_menu()
print(volume.input_output)
print(graphics.input_output)
