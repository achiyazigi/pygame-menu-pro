from types import FunctionType
import pygame
from pygame.locals import *
from pygame.font import Font

from pygameMenuPro.event import Event



COLOR_BLACK = Color(0, 0, 0)
COLOR_WHITE = Color(255, 255, 255)


class InputManager:
    def __init__(self):
        self.last_checked_input = []
        self.last_mouse_position: list[tuple[int, int]] = []
        self.mouse_clicked = (False, False, False)
        self.mouse_wheel = (0, 0)

    def check_input(self) -> int:
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
                exit(0)
            elif(event.type == KEYDOWN):
                self.last_checked_input.append(event.key)
                return event.key
            elif(event.type == MOUSEWHEEL):
                self.mouse_wheel = (event.x, event.y)

        self.last_mouse_position.append(pygame.mouse.get_pos())
        self.mouse_clicked = pygame.mouse.get_pressed()

        return 0

    def reset(self):
        self.reset_last_checked()
        self.reset_last_mouse_position()
        self.reset_mouse_wheel()

    def reset_last_checked(self):
        self.last_checked_input.clear()

    def reset_last_mouse_position(self):
        self.last_mouse_position.clear()

    def reset_mouse_wheel(self):
        self.mouse_wheel = (0, 0)


class FontManager:
    def __init__(self, fonts: dict[str, Font] = {}):
        pygame.font.init()
        self._fonts = fonts

    def add_font(self, font_str: str, font: Font):
        self._fonts[font_str] = font

    def get_font(self, font_str: str):
        return self._fonts.get(font_str, None)

    def set_default_option(self, font: Font):
        """
        set the default option font
        """
        self.add_font('default_option_font', font)

    def set_default_highlight(self, font: Font):
        self.add_font('default_highlight_font', font)

    def set_default_title(self, font: Font):
        self.add_font('default_title_font', font)

    def draw_text(self, text: str, font_str: str, color: Color = Color(255, 255, 255)):
        font = self._fonts[font_str]
        lines = text.splitlines()
        maxline = max(lines, key=len)
        surface = pygame.Surface(
            (font.size(maxline)[0], font.get_height() * 1.25 * len(lines)))
        for i, line in enumerate(lines):
            line_surf = font.render(line, True, color)
            text_rect = line_surf.get_rect()
            text_rect.centerx = surface.get_rect().centerx
            text_rect.top = i * font.get_height() * 1.25
            surface.blit(line_surf, text_rect.topleft)
        return surface


class Option:
    # static attribute to check the input
    input = InputManager()
    # static attribute manage the user fonts
    font = FontManager()

    clock = pygame.time.Clock()

    def __init__(self, text: str, font_str: str = 'default_option_font', color: Color = COLOR_WHITE, event=None):
        self.add = AddExtention(self)
        self._event = event
        if(self._event == None):
            self._event = Event()
        self.text = text
        self._pos = None
        self._font_str = font_str
        self._activation_keys: list[int] = [K_RETURN]
        self.color = color
        self.rect = None

    def is_selected(self):
        """
        returns true iff on of the activation keys is in Option.input.last_checked_input
        """
        return len(list(set(Option.input.last_checked_input) & set(self._activation_keys))) > 0

    def on_select(self):
        """
        will be called when is_selected is true
        """
        self._event.post_event('on_select', self)

    def on_active(self):
        """
        will be called when this option is the current active option in the menu
        """
        self._event.post_event('on_active', self)
        if(self.is_selected()):
            self.on_select()

    def on_deactive(self):
        """
        will be called before the next option is being activated
        """
        self._event.post_event('on_deactive', self)

    def draw(self, surface: pygame.Surface, pos):
        surf = self.render()
        self.rect = surface.blit(
            surf, (self._pos[0] - surf.get_width()//2, self._pos[1]))

    def render(self):
        return Option.font.draw_text(self.text, self._font_str, color=self.color)


class AddExtention():
    def __init__(self, option: Option):
        self._option = option

    def option(self):
        return self._option

    def highlight(self, font_str='default_highlight_font'):
        """
        Add a Highlight decorator
        """

        self._regular_font_str = self._option._font_str

        def highlight_me(option: Option):
            option._font_str = font_str

        def dont_highlight_me(option: Option):
            option._font_str = self._regular_font_str
        self._option.add.active_listener(highlight_me)\
            .add.deactive_listener(dont_highlight_me)

        return self._option

    def input(self, input):
        """
        add input decorator
        """
        head = self._option.text
        setattr(self._option, 'input_output', input)
        self._option.left = K_LEFT
        self._option.right = K_RIGHT
        self._option.input_output = input
        self._option.text = head + '  ' + str(self._option.input_output)

        def update_text_with_input(option: Option):
            option.text = head + '  ' + str(self._option.input_output)
        self._option.add.active_listener(update_text_with_input)

        return self._option

    def menu(self, surface: pygame.Surface, title_pos: tuple[int, int], title_font_str: str = 'default_title_font', options: list[Option] = [], background_color=COLOR_BLACK, cursor: pygame.Surface = None):
        """
        convert this option to a menu.
        The menu title will be same as the option text
        """
        self._option = Menu(self.option(), surface, title_pos,
                            title_font_str, options, background_color, cursor)
        return self._option

    def mouse_menu(self, surface: pygame.Surface, title_pos: tuple[int, int], title_font_str: str = 'default_title_font', options: list[Option] = [], background_color=COLOR_BLACK, cursor: pygame.Surface = None):
        """
        convert this option to a mouse menu
        The menu title will be same as the option text
        The options of this menu will be activated by mouse hover,
        and selected by mouse click.
        """
        self._option = MouseMenu(self.option(
        ), surface, title_pos, title_font_str, options, background_color, cursor)
        return self._option

    def select_listener(self, func: FunctionType):
        """
        will be called inside on_select()
        """
        self.option()._event.subscribe('on_select', func)
        return self.option()

    def active_listener(self, func: FunctionType):
        """
        will be called inside on_active()
        """
        self.option()._event.subscribe('on_active', func)
        return self.option()

    def deactive_listener(self, func: FunctionType):
        """
        will be called inside on_deactive()
        """
        self.option()._event.subscribe('on_deactive', func)
        return self.option()

    def activation_key(self, key: int):
        """
        add another activation key to this option
        """
        self.option()._activation_keys.append(key)
        return self.option()


class Menu(Option):
    def __init__(self, option: Option, surface: pygame.Surface, title_pos: tuple[int, int], title_font_str: str = 'default_title_font', options: list[Option] = [], background_color=COLOR_BLACK, cursor: pygame.Surface = None):
        super().__init__(option.text, option._font_str, option.color, option._event)

        # private:
        self._option = option
        self._surface = surface
        self._title_pos = title_pos
        self._options = options
        self._background_color = background_color
        # public:
        self.title_font_str = title_font_str
        self.run_display = False
        self.state = 0
        self.up = K_UP
        self.down = K_DOWN
        self.quit = K_ESCAPE
        self.cursor = cursor
        self.cursor_offset = 0

        def activate_display_menu(_):
            Option.input.reset_last_checked()
            self.display_menu()
        self.add.select_listener(activate_display_menu)

    def display_menu(self):
        """
        Run this display. It can be called from another menu and "hide" this menu.
        Practicaly, this will stop the current menu loop and start this menu loop.
        """
        self.run_display = True
        while(self.run_display):
            self._surface.fill(self._background_color)
            # draw title:
            title_surf = Option.font.draw_text(self.text, self.title_font_str)
            self._surface.blit(
                title_surf, (self._title_pos[0] - title_surf.get_width()//2, self._title_pos[1]))
            # checking input:
            k = self.input.check_input()
            self.update_state(k)
            if(len(self._options) > 0):

                # activate selected option:
                if(self.state >= 0):
                    self._options[self.state].on_active()

                # draw options:
                last_height = Option.font.get_font(
                    self.title_font_str).get_height() + self._title_pos[1]
                for option in self.get_options():
                    option._pos = (self._title_pos[0], last_height)
                    option.draw(self._surface, option._pos)

                    last_option_font = Option.font.get_font(option._font_str)
                    text_height = option.rect.height * \
                        1.25 * len(option.text.splitlines())
                    last_height = option._pos[1] + text_height

                # draw cursor:
                if(self.cursor != None):
                    selected_option = self._options[self.state]
                    option_font_size = Option.font.get_font(
                        selected_option._font_str).size(selected_option.text)
                    self._surface.blit(self.cursor, (selected_option._pos[0] - int(
                        option_font_size[0]//2) + self.cursor_offset, selected_option._pos[1] - int(option_font_size[1]//2)))
            # reset input list:
            Option.input.reset()

            # refresh:
            pygame.display.update()
            Option.clock.tick(60)

    def update_state(self, k: int):
        """
        This method is being called once in every menu's main loop iteration.
        You shouldn't modify this unless you know what you do
        """
        if(k > 0):
            if(k == self.quit):
                self.run_display = False
            if(len(self._options) > 0):
                if(k == self.up):
                    self._options[self.state].on_deactive()
                    self.state -= 1
                elif(k == self.down):
                    self._options[self.state].on_deactive()
                    self.state += 1
                self.state %= len(self._options)

    def add_option(self, option: Option, index: int = -1):
        """
        Add an option to this menu. it can be Menu as well...
        """
        if(index == -1):
            self._options.append(option)
        else:
            self._options.insert(index, option)

    def set_options(self, options: list[Option]):
        """
        Set the options list to this menu. The list can contain other menus.
        The state of this menu will be reset to 0
        """
        self.state = 0
        self._options = options
        return self

    def get_options(self):
        """
        Returns the option list of this menu
        """
        return self._options

    def __getattr__(self, name: str):
        return self._option.__getattribute__(name)


class MouseMenu(Menu):

    def __init__(self, option: Option, surface: pygame.Surface, title_pos: tuple[int, int], title_font_str: str = 'default_title_font', options: list[Option] = [], background_color=COLOR_BLACK, cursor: pygame.Surface = None):
        super().__init__(option, surface, title_pos, title_font_str,
                         options=options, background_color=background_color, cursor=cursor)
        self.state = -1

    def update_state(self, k: int):
        some_option_active = False
        for i, option in enumerate(self._options):
            rect = option.rect
            if(rect != None):
                if(len(Option.input.last_mouse_position) > 0 and rect.collidepoint(Option.input.last_mouse_position[-1])):
                    if(self.state != i and self.state >= 0):
                        self._options[self.state].on_deactive()
                    some_option_active = True
                    self.state = i
        if(not some_option_active):
            if(self.state >= 0):
                self._options[self.state].on_deactive()
            self.state = -1

    def set_options(self, options: list[Option]):
        super().set_options(options)

        def select_with_mouse(option: Option):
            if(Option.input.mouse_clicked[0]):
                option.on_select()
        for option in self._options:
            option.add.active_listener(select_with_mouse)
        return self
