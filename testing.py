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
    menu.run_display = False
    Option.input.reset_last_checked()

cursor = Option.font.get_font('option_font').render('*', True, Color(255,255,255))

start = HighlightOption(Option('Start', 'option_font'), 'highlight_font')
                 
quit = HighlightOption(Option('Quit', 'option_font'), 'highlight_font')

quit.add_select_listener(lambda option: exit_menu(menu, option))

credits = Menu(HighlightOption(Option('Credits', 'option_font'), 'highlight_font'), screen, TITLE_POS, 'title_font', background_color=Color(165,211,97))
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

credits_text.add_active_listener(lambda _: skip_me(credits))

credits_back = HighlightOption(Option('Back', 'option_font'),'highlight_font')
credits_back.add_select_listener(lambda option: exit_menu(credits, option))

graphics_list = ['Low', 'Medium', 'High', 'Ultra']

def volume_adjustment(option:InputOption):
    if(K_LEFT in Option.input._last_checked_input):
        option.input_output -= 1
    elif(K_RIGHT in Option.input._last_checked_input):
        option.input_output += 1
    


volume = InputOption(HighlightOption(Option('Volume:', 'option_font'), 'highlight_font'),0)
volume.add_active_listener(volume_adjustment)

def graphics_adjustment(option:InputOption):
    shift = 0
    index = graphics_list.index(option.input_output)
    if(option.left in Option.input._last_checked_input):
        shift = -1
    elif(option.right in Option.input._last_checked_input):
        shift = 1
    option.input_output = graphics_list[(index + shift)% len(graphics_list)]
    
graphics = InputOption(Option('Graphics:', 'option_font'), graphics_list[0])
graphics.add_active_listener(graphics_adjustment)

back = HighlightOption(Option('Back', 'option_font'), 'highlight_font')
back.add_select_listener(lambda option: exit_menu(options, option))


menu = Menu(Option('Main Menu', 'option_font'),screen, TITLE_POS,'title_font', cursor=cursor)

options = Menu(InputOption(HighlightOption(Option('Options', 'option_font'), 'highlight_font'), ':)'), screen, TITLE_POS, 'title_font', background_color=Color(75, 23, 175), cursor=cursor)

options.cursor = cursor


options.add_activation_key(K_SPACE)
options.up = K_w
options.down = K_s

volume.add_select_listener(lambda _: print(volume.input_output))

menu.cursor_offset = -10
options.cursor_offset = -10

# click_here = MouseOption(Option('Click Here!', 'option_font'))
# click_here._event.subscribe(lambda: highlight_me(click_here))
# click_here._event.subscribe(lambda: dont_highlight_me(click_here))
# click_here.on_select = lambda: exit_menu(menu, click_here)
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
