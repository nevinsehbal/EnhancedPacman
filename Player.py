import pygame

# This class represents the bar at the bottom that the player controls
class Player(pygame.sprite.Sprite):
    # Set speed vector
    change_x=0
    change_y=0
  
    # Constructor function
    def __init__(self,x,y, filename):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
   
        # Set height, width
        self.image = pygame.image.load(filename).convert()
  
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.setVertexPosition(x,y)
        # self.rect.top = y
        # self.rect.left = x # x = 255, we want it to be x+2 (257) for Inky. x-2 for Clyde
        

    # Change the speed of the player
    def changespeed(self,x,y):
        self.change_x+=x
        self.change_y+=y

    def getVertexPosition(self):
        return (self.rect.left+15,self.rect.top+13)
    
    def setVertexPosition(self,left,top):
        self.rect.left = left-15
        self.rect.top = top-13
          
    # Find a new position for the player
    def update(self,walls):
        # Get the old position, in case we need to go back to it
        
        old_x=self.rect.left
        new_x=old_x+self.change_x
        self.rect.left = new_x

        old_y=self.rect.top
        new_y=old_y+self.change_y

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