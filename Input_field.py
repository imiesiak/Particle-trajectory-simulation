import pygame
class TextInput:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color('black')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = text
        self.txt_surface = pygame.font.Font(None, 25).render(text, True, self.color)
        self.active = False
        self.first_click = True

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = self.color_active

                # Jeśli tekst to dokładnie "0", to usuń
                if self.text.strip() == '0':
                    self.text = ''
            else:
                # Jeśli użytkownik kliknął gdzie indziej i nic nie wpisał — przywróć "0"
                if self.active and self.text.strip() == '':
                    self.text = '0'
                self.active = False
                self.color = self.color_inactive

            self.txt_surface = pygame.font.Font(None, 25).render(self.text, True, self.color)

        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return self.text
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if event.unicode.isnumeric() or event.unicode in '.-':
                    self.text += event.unicode

            self.txt_surface = pygame.font.Font(None, 25).render(self.text, True, self.color)


    def draw(self, surface):
        surface.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(surface, self.color, self.rect, 2)

    def get_value(self):
        try:
            return float(self.text)
        except ValueError:
            return 0

class Checkbox:
    def __init__(self, x, y, label, checked=False):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.label = label
        self.checked = checked
        self.font = pygame.font.SysFont(None, 24)
        self.label_surface = self.font.render(self.label, True, 'black')
        self.label_pos = self.label_surface.get_rect(midleft=(self.rect.right + 10, self.rect.centery))

    def draw(self, surface):
        # Obrys checkboxa
        pygame.draw.rect(surface, 'black', self.rect, 2)

        # Zaznaczenie jeśli aktywny
        if self.checked:
            pygame.draw.line(surface, 'black', self.rect.topleft, self.rect.bottomright, 2)
            pygame.draw.line(surface, 'black', self.rect.topright, self.rect.bottomleft, 2)

        # Rysowanie tekstu
        surface.blit(self.label_surface, self.label_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.checked = not self.checked

class Dropdown:
    def __init__(self, x, y, w, h, font, main_color, option_color, options, selected_index=0):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.main_color = main_color
        self.option_color = option_color
        self.options = options
        self.selected_index = selected_index
        self.expanded = False

    def draw(self, surface):
        # Draw main box
        pygame.draw.rect(surface, self.main_color, self.rect)
        pygame.draw.rect(surface, pygame.Color('black'), self.rect, 2)
        msg = self.font.render(self.options[self.selected_index], True, pygame.Color('black'))
        surface.blit(msg, (self.rect.x + 5, self.rect.y + 5))

        if self.expanded:
            for i, option in enumerate(self.options):
                opt_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height,
                                       self.rect.width, self.rect.height)
                pygame.draw.rect(surface, self.option_color, opt_rect)
                pygame.draw.rect(surface, pygame.Color('black'), opt_rect, 1)
                msg = self.font.render(option, True, pygame.Color('black'))
                surface.blit(msg, (opt_rect.x + 5, opt_rect.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.expanded = not self.expanded
            elif self.expanded:
                for i in range(len(self.options)):
                    opt_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height,
                                           self.rect.width, self.rect.height)
                    if opt_rect.collidepoint(event.pos):
                        self.selected_index = i
                        self.expanded = False
                        break
                else:
                    self.expanded = False

    def get_selected(self):
        return self.options[self.selected_index]

    def was_clicked(self, pos):
        if self.rect.collidepoint(pos):
            return True
        if self.expanded:
            for i in range(len(self.options)):
                opt_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height,
                                    self.rect.width, self.rect.height)
                if opt_rect.collidepoint(pos):
                    return True
        return False
__all__=['Dropdown']