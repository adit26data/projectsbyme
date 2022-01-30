import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
class Alien_Invasion:
    #overall class to manage the entire program
    def __init__(self):#to create an inital mode for the game
        pygame.init()
        self.settings=Settings()
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()
       
        self.screen=pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("ALIEN INVASION")
        self.stats=GameStats(self)
        self.sb=Scoreboard(self)
        self.ship=Ship(self)
        self._create_fleet()
        self.play_button=Button(self,"PLAY")
        self.bg_color=(230,230,230)  #RGB values for the background colour
        
    def _ship_hit(self):
        #responds to ship being hit by alien
        if self.stats.ships_left>0:
            #decrement of ships and update scoreboard
          self.stats.ships_left-=1
          self.sb.prep_ships()
          self.aliens.empty()
          self.bullets.empty()
          self._create_fleet()
          self.ship.center_ship()
          sleep(0.5) #pause the game momentarily
        else:
            self.stats.game_active=False
            pygame.mouse.set_visible(True)
                 
    def _check_events(self):
         for event in pygame.event.get():  #for keyboard and mouse events
                if event.type==pygame.QUIT:
                    sys.exit()
                elif event.type==pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    mouse_pos=pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
                    
    def _check_play_button(self,mouse_pos):
        #start a new game when the player clicks PLAY
        button_clicked=self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #reset game settings
            self.settings.initialize_dynamic_settings()
            #reset game stats
            self.stats.reset_stats()
            self.stats.game_active=True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)
            
    def _check_keydown_events(self,event):
        #responds to keypresses
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=True
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=True
        elif event.key==pygame.K_q:
            sys.exit()
        elif event.key==pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        #responds to key presses
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=False
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=False

    def _fire_bullet(self):
        #create a new bullet and add to bullet grp
        if len(self.bullets)<self.settings.bullets_allowed:
           new_bullet=Bullet(self)
           self.bullets.add(new_bullet)
           
    def _create_fleet(self):
        #creating fleet of aliens
        alien=Alien(self)
        alien_width,alien_height=alien.rect.size
        available_space_x=self.settings.screen_width -(2*alien_width)
        number_of_aliens_x=available_space_x //(2*alien_width)
        #determining the numbre of rows of aliends that fit into the screen
        ship_height=self.ship.rect.height
        available_space_y=(self.settings.screen_height-(3*alien_height)-ship_height)
        number_of_rows=available_space_y//(2*alien_height)
        #create a full fleet of aliens
        for row_number in range(number_of_rows):
          for alien_number in range(number_of_aliens_x):
              self._create_alien(alien_number,row_number)
           
    def _create_alien(self,alien_number,row_number):
            alien=Alien(self)
            alien_width,alien_height=alien.rect.size
            alien.x=alien_width+(2*alien_width*alien_number)
            alien.rect.x=alien.x
            alien.rect.y=alien.rect.height + 2*(alien.rect.height*row_number)
            self.aliens.add(alien)
            
    def _check_fleet_edges(self):
        #responds if any alien has reached an edge
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        #drop entire fleet and change the fleet direction
        for alien in self.aliens.sprites():
            alien.rect.y+=self.settings.fleet_drop_speed
        self.settings.fleet_direction*=-1
        
        
    
    def _update_bullets(self):
        #update bulle position and get rid of old one
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom<=0:
                self.bullets.remove(bullet)
        #check for bullets hitting the aliens
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions=pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        if collisions:
            for aliens in collisions.values():
              self.stats.score+=self.settings.alien_points*len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            #increase level
            self.stats.level+=1
            self.sb.prep_level()
            
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update() #update fleet positions
        #look for ship and alien collisions
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        #look for aliens hitting bottom of the screen
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        screen_rect=self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom>=screen_rect.bottom:
                #treat this as same when the ship gets hit
                self._ship_hit()
                break
    
            

    def _update_screen(self):
        #redraw the screen with each loop
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen)
            self.sb.show_score()
            if not self.stats.game_active:
                self.play_button.draw_button()
            pygame.display.flip()#for last recent screen

    def run_game(self):
        #start main loop of the game
        while True:
            self._check_events()
            if self.stats.game_active:
              self.ship.update()
              self._update_bullets()
              self._update_aliens()
            self._update_screen()


if __name__=="__main__":
    ai=Alien_Invasion()
    ai.run_game()

                    
