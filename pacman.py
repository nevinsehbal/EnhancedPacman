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

def startGame(screen, clock, font):
  # This is a list of 'sprites.' Each wall, pacman and food in the program is
  # added to this list. The list is managed by a class called 'RenderPlain.'
  all_sprites_list = pygame.sprite.RenderPlain()
  block_list = pygame.sprite.RenderPlain()
  vertices_list = pygame.sprite.RenderPlain()
  monsta_list = pygame.sprite.RenderPlain()
  # Maze is created using recursive_backtracking algorithm
  wall_list = setupMaze(all_sprites_list)
  # Create the player paddle object
  Pacman = Player(random.choice([32,572]), random.choice([32,572]), "images/pacman.png" )
  all_sprites_list.add(Pacman)
  # Create Graph (vertices, edges) using wall list and vertices list
  Graph = initialize_A_star(vertices_list,wall_list)
  # Ghosts are spawned at a random location with minimum distance of 360 and maximum of 390.
  # Recall that the overall maze is 600*600 excluding the frames.
  ghost = createGhost(Pacman.getVertexPosition(), Graph, min_distance = 360, max_distance = 390)
  monsta_list.add(ghost)
  # Pacman foods are drawn at the places where no wall and PAc-Man exist.
  drawFoods(block_list,all_sprites_list)
  # number of foods will be used to determine the score of the Player
  num_of_foods = len(block_list)
  score = 0
  game_quitted = False
  # Ghost update boolean is toggled to update the ghost movement every 20ms, Pacman position is updated every 10ms.
  ghost_update = False
  # The movement of the entities are logged in log files on each game play.
  analytics_logger = initialize_analytics()
  # Time is kept to spawn another ghost at every GHOST_SPAWN_TIME_SEC seconds.
  init_time = time.time()
  GHOST_SPAWN_TIME_SEC = 10 # Trials [5,10,30,60]
  SENSITIVITY_DISTANCE = 400 # Trials [100,300,500]
  log_custom("GHOST_SPAWN_TIME_SEC is "+str(GHOST_SPAWN_TIME_SEC),analytics_logger)
  log_custom("SENSITIVITY_DISTANCE is "+str(SENSITIVITY_DISTANCE),analytics_logger)
  while not game_quitted:
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
      # apply logging
      log_entity_movement("Pacman", Pacman.getVertexPosition(),analytics_logger)
      for i, ghost in enumerate(monsta_list):
        log_entity_movement("Ghost_"+str(i), ghost.getVertexPosition(),analytics_logger)          
      # if more than GHOST_SPAWN_TIME_SEC seconds is passed, spawn a new ghost
      if(time.time()-init_time > GHOST_SPAWN_TIME_SEC): 
         init_time = time.time()
         ghost = createGhost(Pacman.getVertexPosition(),Graph)
         monsta_list.add(ghost)
      # update Pacman position
      Pacman.update(wall_list)
      # ghost position is updated with two functions. If the ghost is inside of a circle
      # with radius = SENSITIVITY_DISTANCE, then the ghost path is determined with A_star algorithm. 
      # If it is not inside this circular area, the ghost movements are random. In the random movement,
      # ghost can go to up, down, right, left, upper left, upper right, lower left, lower right.
      if(ghost_update):
        ghost_update = False
        for ghost in monsta_list:
           if(is_closer_than_threshold(ghost.getVertexPosition(),Pacman.getVertexPosition(),thresh=SENSITIVITY_DISTANCE)):
              ghost_next_destination = A_star(Graph, ghost.getVertexPosition(),Pacman.getVertexPosition())[-2]
              ghost.setVertexPosition(ghost_next_destination.x,ghost_next_destination.y)
           else:
              ghost.randomMovement(wall_list)
      else:
         ghost_update = True
      # See if the Pacman block has collided with anything.
      # dokill = True parameter (3rd) removes the collided blocks from the screen.
      foods_hit_list = pygame.sprite.spritecollide(Pacman, block_list, True)
      # Check the list of collisions.
      if len(foods_hit_list) > 0:
          log_custom("Pacman ate "+str(len(foods_hit_list))+" food",analytics_logger)
          score +=len(foods_hit_list)
      # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT
   
      # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
      screen.fill(black)
      wall_list.draw(screen)
      all_sprites_list.draw(screen)
      monsta_list.draw(screen)
      text=font.render("Score: "+str(score)+"/"+str(num_of_foods), True, red)
      screen.blit(text, [10, 10])
      if score == num_of_foods:
        log_custom("Pacman score is: "+str(score)+"/"+str(num_of_foods),analytics_logger)
        doNext("Congratulations, you won!",145,all_sprites_list,block_list,monsta_list,wall_list, screen, clock, font)
      monsta_hit_list = pygame.sprite.spritecollide(Pacman, monsta_list, False)
      if monsta_hit_list:
        log_custom("Pacman score is: "+str(score)+"/"+str(num_of_foods),analytics_logger)
        doNext("Game Over",235,all_sprites_list,block_list,monsta_list,wall_list, screen, clock, font)
      # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
      pygame.display.flip()
      clock.tick(10)

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

#----------------------- HELPER FUNCTIONS ---------------------

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

def createGhost(pacman_pos, graph, min_distance = 360, max_distance = 390):
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


# Function to update the ghost position
def update_ghost_position(ghost, graph, pacman_position):
    next_destination = A_star(graph, ghost.getVertexPosition(), pacman_position)[-2]
    ghost.setVertexPosition(next_destination.x, next_destination.y)

def is_closer_than_threshold(obj1, obj2, thresh = 360):
   return (math.sqrt((obj1[0] - obj2[0])**2 + (obj1[1] - obj2[1])**2) < thresh)