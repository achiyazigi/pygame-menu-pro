from types import FunctionType
import pygame
from pygame.locals import *
from pygame.font import Font
from event import Event


COLOR_BLACK = Color(0, 0, 0)


class InputManager:
    def __init__(self):
        self._last_checked_input = []

    def check_input(self) -> int:
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
                exit(0)
            elif(event.type == KEYDOWN):
                self._last_checked_input.append(event.key)
                return event.key
        return 0

    def reset_last_checked(self):
        self._last_checked_input.clear()


class FontManager:
    def __init__(self, fonts: dict[str, Font] = {}):
        pygame.font.init()
        self._fonts = fonts

    def add_font(self, font_str: str, font: Font):
        self._fonts[font_str] = font

    def get_font(self, font_str: str):
        return self._fonts.get(font_str, None)

    def draw_text(self, surface: pygame.Surface, text: str, pos: tuple[int, int], font_str: str, color: Color = Color(255, 255, 255)):
        font = self._fonts[font_str]
        lines = text.splitlines()
        for i, line in enumerate(lines):
            surf = font.render(line, True, color)
            text_rect = surf.get_rect()
            text_rect.center = (pos[0], pos[1] + i * font.get_height() * 1.25)
            surface.blit(surf, text_rect)


class Option:
    input = InputManager()
    font = FontManager()
    clock = pygame.time.Clock()

    def __init__(self, text: str, font_str: str, color: Color = Color(255, 255, 255)):

        self._event = Event()
        self.text = text
        self._pos = None
        self._font_str = font_str
        self._activation_keys: list[int] = [K_RETURN]
        self.color = color

    def get_text(self):
        return self.text

    def set_text(self, text: str):
        self.text = text

    def get_font_str(self):
        return self._font_str

    def add_activation_key(self, key: int):
        self._activation_keys.append(key)

    def is_selected(self):
        return len(list(set(Option.input._last_checked_input) & set(self._activation_keys))) > 0

    def on_select(self):
        self.post_event('on_select', self)

    def post_event(self, event_type: str, *data):
        self._event.post_event(event_type, *data)

    # will be called when this option is the current selected option in the menu

    def on_active(self, *data):
        self.post_event('on_active', *data)
        if(self.is_selected()):
            self.on_select()

    # will be called before the next selected option is being activated
    def on_deactive(self):
        self.post_event('on_deactive', self)

    def draw(self, surface, pos):
        self.font.draw_text(surface, self.get_text(), pos,
                            self.get_font_str(), color=self.color)

    # called after Option.on_active()
    def add_active_listener(self, func):
        self._event.subscribe('on_active', func)

    # called after Option.on_deactive()
    def add_deactive_listener(self, func):
        self._event.subscribe('on_deactive', func)

    # called after Option.on_select()
    def add_select_listener(self, func):
        self._event.subscribe('on_select', func)

    def set_font_str(self, font_str: str):
        self._font_str = font_str


class Decorator(Option):
    def __init__(self, option: Option):
        self._option = option
        self.color = option.color

    def option(self):
        return self._option

    def get_font_str(self):
        return self.option().get_font_str()

    def draw(self, surface, pos):
        self.option().draw(surface, pos)

    def add_activation_key(self, key: int):
        self.option().add_activation_key(key)

    def add_active_listener(self, func):
        self.option().add_active_listener(func)

    def add_deactive_listener(self, func):
        self.option().add_deactive_listener(func)

    def add_select_listener(self, func):
        self.option().add_select_listener(func)

    def is_selected(self):
        return self.option().is_selected()

    def on_select(self):
        self.option().on_select()

    def on_active(self, *data):
        self.option().on_active(*data)

    def on_deactive(self):
        self.option().on_deactive()

    def post_event(self, event_type: str, *data):
        self.option().post_event(event_type, *data)

    def set_text(self, text: str):
        self.option().set_text(text)

    def get_text(self):
        return self.option().get_text()


class HighlightOption(Decorator):
    def __init__(self, option: Option, highlight_font_str: str):
        super().__init__(option)
        self._highlight_font_str = highlight_font_str
        self._regular_font_str = self.option().get_font_str()

        def highlight_me(_):
            option.set_font_str(self._highlight_font_str)

        def dont_highlight_me(_):
            option.set_font_str(self._regular_font_str)
        option.add_active_listener(highlight_me)
        option.add_deactive_listener(dont_highlight_me)


class Menu(Decorator):
    def __init__(self, option: Option, surface: pygame.Surface, title_pos: tuple[int, int], title_font_str: str, options: list[Option] = [], background_color=COLOR_BLACK, cursor: pygame.Surface = None):
        super().__init__(option)
        # private:
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
        self.add_select_listener(activate_display_menu)

    def display_menu(self):
        self.run_display = True
        while(self.run_display):
            self._surface.fill(self._background_color)
            # draw title:
            Option.font.draw_text(
                self._surface, self.get_text(), self._title_pos, self.title_font_str)

            # checking input:
            k = self.input.check_input()
            self.update_state(k)
            if(len(self._options) > 0):

                # activate selected option:
                self._options[self.state].on_active(self._options[self.state])

                # draw options:
                last_height = Option.font.get_font(
                    self.title_font_str).get_height() + self._title_pos[1]
                for option in self._options:
                    option._pos = (self._title_pos[0], last_height)
                    option.draw(self._surface, option._pos)

                    last_option_font = Option.font.get_font(
                        option.get_font_str())
                    text_height = last_option_font.get_height(
                    ) * 1.25 * len(option.get_text().splitlines())
                    last_height = option._pos[1] + text_height

                # draw cursor:
                if(self.cursor != None):
                    selected_option = self._options[self.state]
                    option_font_size = Option.font.get_font(
                        selected_option.get_font_str()).size(selected_option.get_text())
                    self._surface.blit(self.cursor, (selected_option._pos[0] - int(
                        option_font_size[0]//2) + self.cursor_offset, selected_option._pos[1] - int(option_font_size[1]//2)))
            # reset input list:
            Option.input.reset_last_checked()

            # refresh:
            pygame.display.update()
            Option.clock.tick(60)

    def update_state(self, k: int):
        if(k > 0):
            if(k == self.quit):
                self.run_display = False
            if(k == self.up):
                self._options[self.state].on_deactive()
                self.state -= 1
            elif(k == self.down):
                self._options[self.state].on_deactive()
                self.state += 1
            self.state %= len(self._options)

    def add_option(self, option: Option, index: int = -1):
        if(index == -1):
            self._options.append(option)
        else:
            self._options.insert(index, option)

    def set_options(self, options: list[Option]):
        self._options = options

    def get_options(self):
        return self._options


class InputOption(Decorator):
    def __init__(self, option: Option, input_output):
        super().__init__(option)
        self.left = K_LEFT
        self.right = K_RIGHT
        self.input_output = input_output
        self.text = self.option().get_text()
        self.set_text(self.text + '  ' + str(self.input_output))

        def update_text_with_input(_):
            self.set_text(self.text + '  ' + str(self.input_output))
        self.add_active_listener(update_text_with_input)
