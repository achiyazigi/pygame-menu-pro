# pygame-menu-pro
create a pygame menu fast without compromise
## Usage:
--(before you run this code make sure you have installed/changed the fonts in the code)
```python
import pygame
from pygame_menu_pro import *

# pygame setup:
pygame.init()
pygame.display.set_caption('Pygame Menu Pro')

# consts:
WIDTH= 1080
HEIGHT=WIDTH//1.6
WINDOW_SIZE = (WIDTH, HEIGHT)

# The surface for my menu:
screen = pygame.display.set_mode(WINDOW_SIZE, depth=32)

# This can be different for each Menu element,
# I Chose here for simplicity and style to place all titles the same...
TITLE_POS = (screen.get_width()//2, screen.get_height()//4)

# setting up your font with your names so it will be much easier to
# access them with the correct context.
# keep your fonts orgenized and patterned
Option.font.add_font('option_font', pygame.font.SysFont('Comic Sans MS', 50))
Option.font.add_font('highlight_font', pygame.font.SysFont('Comic Sans MS', 50, bold=True))
Option.font.add_font('title_font', pygame.font.SysFont('Plaguard-ZVnjx', 80))

# options for Main Menu
start_option = HighlightOption(Option('Start', 'option_font'), 'highlight_font')
options_menu = HighlightMenu(Menu(Option('Options', 'option_font'), screen, TITLE_POS, 'title_font'), 'highlight_font')
quit_option = HighlightOption(Option('Quit', 'option_font'), 'highlight_font')

# every menu is also an Option element and can be presented as an option in other menu/s...
main_menu = Menu(Option('Main Menu', 'option_font'), screen, TITLE_POS, 'title_font')

# add a function to quit
def quit(option:Option, menu:Menu):
    if(option.is_selected()):
        menu.run_display = False

# apply the quit function to the quit option!
# the quit function above will be called each time quit_option is active (highlighted but not nesceserly)
quit_option.add_on_active_function(lambda: quit(quit_option, main_menu))

# options for options-menu
back_option = Option('Back', 'option_font')
# using the same quit function to quit the options-menu and actualy return to the parent menu!
back_option.add_on_active_function(lambda: quit(back_option, options_menu))

# apply an option to options-menu
options_menu.add_option(back_option)

# apply multiple options to main-menu
main_menu.set_options([
    start_option,
    options_menu,
    quit_option
])

# run!
main_menu.display_menu()


```
