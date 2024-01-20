#Pacman in Python with PyGame
#https://github.com/hbokmann/Pacman
  
from pygame import *
import pygame
from Wall import *
from Block import *
from Player import *
from Ghost import *
from helpers import *
from Astar import *
import time
from Analytics import *

# Function to update the ghost position
def update_ghost_position(ghost, graph, pacman_position):
    next_destination = A_star(graph, ghost.getVertexPosition(), pacman_position)[-2]
    ghost.setVertexPosition(next_destination.x, next_destination.y)


def startGame(screen, clock, font):
  # This is a list of 'sprites.' Each block in the program is
  # added to this list. The list is managed by a class called 'RenderPlain.'
  all_sprites_list = pygame.sprite.RenderPlain()
  block_list = pygame.sprite.RenderPlain()
  vertices_list = pygame.sprite.RenderPlain()
  monsta_list = pygame.sprite.RenderPlain()
  wall_list = setupMaze(all_sprites_list)

  pacman_initial_x = random.choice([32,572])
  pacman_initial_y = random.choice([32,572])
  # Create the player paddle object
  Pacman = Player(pacman_initial_x, pacman_initial_y, "images/pacman.png" )
  all_sprites_list.add(Pacman)

  Graph = initialize_A_star(vertices_list,wall_list)
  ghost = createGhost(Pacman.getVertexPosition(),Graph)
  monsta_list.add(ghost)
   
  drawFoods(block_list,all_sprites_list)

  bll = len(block_list)
  score = 0
  game_quitted = False
  ghost_update = False

  analytics_logger = initialize_analytics()
  init_time = time.time()
  while not game_quitted:
      # apply logging for analytics
      log_entity_movement("Pacman", Pacman.getVertexPosition(),analytics_logger)
      for i, ghost in enumerate(monsta_list):
        log_entity_movement("Ghost_"+str(i), ghost.getVertexPosition(),analytics_logger)
      # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              game_quitted=True

          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_LEFT:
                  Pacman.changespeed(-30,0)
              if event.key == pygame.K_RIGHT:
                  Pacman.changespeed(30,0)
              if event.key == pygame.K_UP:
                  Pacman.changespeed(0,-30)
              if event.key == pygame.K_DOWN:
                  Pacman.changespeed(0,30)

          if event.type == pygame.KEYUP:
              if event.key == pygame.K_LEFT:
                  Pacman.changespeed(30,0)
              if event.key == pygame.K_RIGHT:
                  Pacman.changespeed(-30,0)
              if event.key == pygame.K_UP:
                  Pacman.changespeed(0,30)
              if event.key == pygame.K_DOWN:
                  Pacman.changespeed(0,-30)
          
      # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
   
      # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
                  
      if(time.time()-init_time > 10): # if more than 10 seconds is passed
         init_time = time.time()
         ghost = createGhost(Pacman.getVertexPosition(),Graph)
         monsta_list.add(ghost)
         
      Pacman.update(wall_list)

      if(ghost_update):
        ghost_update = False
        for ghost in monsta_list:
           if(is_closer_than_threshold(ghost.getVertexPosition(),Pacman.getVertexPosition())):
              ghost_next_destination = A_star(Graph, ghost.getVertexPosition(),Pacman.getVertexPosition())[-2]
              ghost.setVertexPosition(ghost_next_destination.x,ghost_next_destination.y)
           else:
              ghost.randomMovement(wall_list)
      else:
         ghost_update = True

      # See if the Pacman block has collided with anything.
      # dokill = True parameter (3rd) removes the collided blocks from the screen.
      blocks_hit_list = pygame.sprite.spritecollide(Pacman, block_list, True)
      # Check the list of collisions.
      if len(blocks_hit_list) > 0:
          score +=len(blocks_hit_list)
      
      # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT
   
      # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
      screen.fill(black)
      wall_list.draw(screen)
      all_sprites_list.draw(screen)
      monsta_list.draw(screen)

      text=font.render("Score: "+str(score)+"/"+str(bll), True, red)
      screen.blit(text, [10, 10])

      if score == bll:
        doNext("Congratulations, you won!",145,all_sprites_list,block_list,monsta_list,wall_list, screen, clock, font)

      monsta_hit_list = pygame.sprite.spritecollide(Pacman, monsta_list, False)

      if monsta_hit_list:
        doNext("Game Over",235,all_sprites_list,block_list,monsta_list,wall_list, screen, clock, font)

      # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
      pygame.display.flip()
      clock.tick(10)

def is_closer_than_threshold(obj1, obj2, thresh = 360):
   return (math.sqrt((obj1[0] - obj2[0])**2 + (obj1[1] - obj2[1])**2) < thresh)


def doNext(message,left,all_sprites_list,block_list,monsta_list,wall_list, screen, clock, font):
  while True:
      # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            pygame.quit()
          if event.key == pygame.K_RETURN:
            del all_sprites_list
            del block_list
            del monsta_list
            del wall_list
            startGame(screen, clock, font)

      #Grey background
      w = pygame.Surface((400,200))  # the size of your rect
      w.set_alpha(10)                # alpha level
      w.fill((128,128,128))           # this fills the entire surface
      screen.blit(w, (100,200))    # (0,0) are the top-left coordinates

      #Won or lost
      text1=font.render(message, True, white)
      screen.blit(text1, [left, 233])

      text2=font.render("To play again, press ENTER.", True, white)
      screen.blit(text2, [135, 303])
      text3=font.render("To quit, press ESCAPE.", True, white)
      screen.blit(text3, [165, 333])

      pygame.display.flip()
      clock.tick(10)


# This creates all the walls in room 1
def setupMaze(all_sprites_list):
    # Make the walls. (x_pos, y_pos, width, height)
    wall_list=pygame.sprite.RenderPlain()
    #TODO: Add wall list as a random maze generation process, not constant walls. The grid is 606*606
    # This is a list of walls. Each is in the form [x, y, width, height]
    walls = create_walls()#predefined_edges #predefined_walls
    # Loop through the list. Create the wall, add it to the list
    for x,y,w,h in walls:
        new_wall=Wall(x,y,w,h,blue)
        wall_list.add(new_wall)
        all_sprites_list.add(new_wall)         
    # return our new list
    return wall_list

def createGhost(pacman_pos, graph):
  min_distance = 360
  max_distance = 390
  color_path = random.choice(["images/Blinky.png", "images/Pinky.png", "images/Inky.png", "images/Clyde.png"])
  v,e = graph
  for vertex in v:
     if(min_distance < math.sqrt((pacman_pos[0] - vertex.x)**2 + (pacman_pos[1] - vertex.y)**2) < max_distance):
        ghost_pos = (vertex.x,vertex.y)
  ghost = Ghost(ghost_pos[0], ghost_pos[1], color_path)
  #print("Ghost is at:", ghost_pos)
  return ghost
  

def drawFoods(block_list,all_sprites_list):
   # Draw the grid
  for row in range(19):
      for column in range(19):
          # if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
          #     continue
          # else:
          block = Block(yellow, 4, 4)
          # Set a random location for the block
          block.rect.x = (30*column+6)+26
          block.rect.y = (30*row+6)+26
          # check the collision between walls+pacman with foods
          collision = pygame.sprite.spritecollide(block, all_sprites_list, False)
          if collision:
              continue
          else:
              # Add the block to the list of objects
              block_list.add(block)
              all_sprites_list.add(block)