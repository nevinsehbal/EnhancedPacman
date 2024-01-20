from Player import Player
import pygame

#Inheritime Player klassist
class Ghost(Player):
    # pacman position corners: [17,19] [557,19] [17,559] [557,559]
    # pacman jumps ±30 pixels each time.
    def updateGhostPosition(self,next_destination):
       self.rect.top = next_destination.x-13
       self.rect.left = next_destination.y-15
       return