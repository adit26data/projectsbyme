import pygame
from pygame.sprite import Sprite
class Bullet(Sprite):
#CLASS TO MANAGE BULLETS
    def __init__(self,ai_game):
        #create a bullet object at the ship current position
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        self.color=self.settings.bullet_color
        #creating a new bullet at 0,0 position
        self.rect=pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
        self.rect.midtop=ai_game.ship.rect.midtop
        self.y=float(self.rect.y)

    def update(self):
        #move bullet on the screen
        self.y-=self.settings.bullet_speed
        #update the rect position
        self.rect.y=self.y
    def draw_bullet(self):
        #draw bullet on the screen
        pygame.draw.rect(self.screen,self.color,self.rect)
        
