from Player import Player
import pygame
import random

#Inheritime Player klassist
class Ghost(Player):
    # pacman position corners: [17,19] [557,19] [17,559] [557,559]
    # pacman jumps ±30 pixels each time.
    def updateGhostPosition(self,next_destination):
       self.rect.top = next_destination.x-13
       self.rect.left = next_destination.y-15
       return
    
    def randomMovement(self, walls):
        change_x = random.choice([+30, -30, 0])
        change_y = random.choice([+30, -30, 0])

        old_x=self.rect.left
        new_x=old_x+change_x
        self.rect.left = new_x

        old_y=self.rect.top
        new_y=old_y+change_y

        # Did this update cause us to hit a wall?
        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:
            # Whoops, hit a wall. Go back to the old position
            self.rect.left=old_x
        else:
            self.rect.top = new_y
            # Did this update cause us to hit a wall?
            y_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_collide:
                # Whoops, hit a wall. Go back to the old position
                self.rect.top=old_y