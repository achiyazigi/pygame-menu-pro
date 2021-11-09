import pygame
from pygame_menu_pro import *

clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('title')
WIDTH= 1080
HEIGHT=WIDTH//1.6
WINDOW_SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(WINDOW_SIZE, depth=32)
TITLE_POS = (screen.get_width()//2, screen.get_height()//4)

Option.font.add_font('option_font', pygame.font.SysFont('Comic Sans MS', 50))
Option.font.add_font('highlight_font', pygame.font.SysFont('Comic Sans MS', 50, bold=True))
Option.font.add_font('title_font', pygame.font.SysFont('Plaguard-ZVnjx', 80))
Option.font.add_font('credits_font', pygame.font.SysFont('Plaguard-ZVnjx', 30))
Option.font.add_font('link_font', pygame.font.SysFont('Arial', 30))
Option.font.add_font('highlight_link_font', pygame.font.SysFont('Arial', 30, bold=True))


def exit_menu(menu:Menu, option:Option):

    if(option.is_selected()):
        menu.run_display = False
        Option.input.reset_last_checked()


def highlight_me(option:Option):
    option.set_font_str('highlight_font')

def dont_highlight_me(option:Option):
    option.set_font_str('option_font')


cursor = Option.font.get_font('option_font').render('*', True, Color(255,255,255))

start = HighlightOption(Option('Start', 'option_font'), 'highlight_font')
                 
quit = Option('Quit', 'option_font')
quit.add_on_active_function(lambda: highlight_me(quit))
quit.add_on_deactive_function(lambda: dont_highlight_me(quit))
quit.add_on_active_function(lambda: exit_menu(menu, quit))

credits = HighlightMenu(Menu(Option('Credits', 'option_font'), screen, TITLE_POS, 'title_font', background_color=Color(165,211,97)), 'highlight_font')
credits.color = Color(200,100,42)

def skip_me(menu:Menu):
    if(menu.up in Option.input._last_checked_input):
        menu.state -= 1
    elif(menu.down in Option.input._last_checked_input):
        menu.state += 1
    menu.state %= len(menu.get_options())
credits_link = HighlightOption(Option('https://github/achiyazigi', 'link_font'), 'highlight_link_font')
credits_text = Option("""
    those are the credits...
    if you want to see more please visit my
    github profile every once in a while to get the
    most updated versions of my libraries...
    thank you for choosing to develope with my art.
""", 'credits_font', color=Color(35,71,100))

credits_text.add_on_active_function(lambda: skip_me(credits))

credits_back = HighlightOption(Option('Back', 'option_font'),'highlight_font')
credits_back.add_on_active_function(lambda: exit_menu(credits, credits_back))

graphics_list = ['Low', 'Medium', 'High', 'Ultra']

def volume_adjustment(option:InputOption):
    if(K_LEFT in Option.input._last_checked_input):
        option.input_output -= 1
    elif(K_RIGHT in Option.input._last_checked_input):
        option.input_output += 1
    


volume = InputOption(Option('Volume:', 'option_font'),0)
volume.add_on_active_function(lambda: volume_adjustment(volume))

def graphics_adjustment(option:InputOption):
    shift = 0
    index = graphics_list.index(option.input_output)
    if(K_LEFT in Option.input._last_checked_input):
        shift = -1
    elif(K_RIGHT in Option.input._last_checked_input):
        shift = 1
    option.input_output = graphics_list[(index + shift)% len(graphics_list)]
    
graphics = InputOption(Option('Graphics:', 'option_font'), graphics_list[0])
graphics.add_on_active_function(lambda: graphics_adjustment(graphics))

back = Option('Back', 'option_font')
back.add_on_active_function(lambda: exit_menu(options, back))
back.add_on_active_function(lambda: highlight_me(back))
back.add_on_deactive_function(lambda: dont_highlight_me(back))


menu = Menu(Option('Main Menu', 'option_font'),screen, TITLE_POS,'title_font', cursor=cursor)

options = Menu(Option('Options', 'option_font'), screen, TITLE_POS, 'title_font', background_color=Color(75, 23, 175), cursor=cursor)
options = HighlightMenu(options, 'highlight_font')
options.cursor = cursor


options.add_activation_key(K_SPACE)

menu.cursor_offset = -10
options.cursor_offset = -10

menu.set_options([
    start,
    options,
    credits,
    quit
])

options.set_options([
    volume,
    graphics,
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
