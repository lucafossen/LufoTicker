import pygame

class PushButton:
    pygame.font.init()

    def __init__(self, rect, color, textcolor, textfont, text, dest):
        self.initcolor = color
        self.rect = pygame.Rect(rect)
        self.color = color
        self.text = text
        self.textcolor = textcolor
        self.textfont = textfont
        self.dest = dest
        self.textsurface = self.textfont.render(text, True, self.textcolor)
        self.active = False
        self.state = None
        
    def draw(self):
        if self.active == True:
            self.color = (255, 0, 0)
        else:
            self.color = self.initcolor
        pygame.draw.rect(self.dest, self.color, self.rect)
        self.dest.blit(self.textsurface, (self.rect[0]+3, self.rect[1]+2))
    
    def toggle(self):
        if self.active:
            self.active = False
        else:
            self.active = True
    
    #activates self and deselects a list of other buttons
    def select(self, buttons):
        for i in buttons:
            i.active = False
        self.active = True