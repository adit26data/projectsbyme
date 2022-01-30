import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
    #a class to manage ships used in the game
    def __init__(self,ai_game):
        #initialising ship position
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        self.screen_rect=ai_game.screen.get_rect()
        #loading ship
        self.image=pygame.image.load("images/ship.bmp")
        self.rect=self.image.get_rect()
        #starting ship at the bottom centre
        self.rect.midbottom=self.screen_rect.midbottom
        self.x=float(self.rect.x)
        #movement flag
        self.moving_right=False
        self.moving_left=False
    def update(self):
        #update ship movement based on flag
        if self.moving_right and self.rect.right<self.screen_rect.right:
            self.x+=self.settings.ship_speed
        if self.moving_left and self.rect.left>0:
            self.x-=self.settings.ship_speed
        self.rect.x=self.x
    def blitme(self):
        #ship at current location
        self.screen.blit(self.image,self.rect)
    def center_ship(self):
        self.rect.midbottom=self.screen_rect.midbottom
        self.x=float(self.rect.x)
        
