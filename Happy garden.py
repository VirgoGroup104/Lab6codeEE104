# -*- coding: utf-8 -*-
"""


@author: lqkvn
"""

import pgzrun
from random import *
import time


#screen dimension variables
WIDTH = 800
HEIGHT = 600

#boolean variables
game_over = False
finalized = False
garden_happy = True
raining = True
#time variables
time_elapsed = 0
start_time = time.time()

#actor variables
cow = Actor("cow")
cow.pos = (100, 500)

#list variables
flower_list = []
wilted_list = []
alien_list = []
alien_vx_list = []
alien_vy_list = []

io_list = []
io_vx_list = []
io_vy_list = []

def draw():
    global game_over, time_elapsed, finalized, raining

    if (not game_over):
        screen.clear()
        if not raining:
            screen.blit("garden", (0, 0))
        else:
            screen.blit("garden-raining", (0, 0))
        cow.draw()
        for flower in flower_list:
            flower.draw()
        for alien in alien_list:
            alien.draw()
        for io in io_list:
            io.draw()
        time_elapsed = int(time.time() - start_time)
        screen.draw.text("Garden happy for: " + str(time_elapsed)
                         + " seconds",topleft=(10,10),color="black")
    else:
        if (not finalized):
            cow.draw()
            screen.draw.text("Garden happy for: " + str(time_elapsed)
                         + " seconds",topleft=(10,10),color="black")
            if(not garden_happy):
                screen.draw.text("GARDEN UNHAPPY-GAME OVER!",topleft=(10,50),color="black")
                finalized = True
            else:
                screen.draw.text("ATTACK-GAME OVER!",topleft=(10,50),color="black")
                finalized = True

def new_flower():
    global flower_list, wilted_list
    flower_new = Actor("flower")
    flower_new.pos = (randint(50,WIDTH-50), randint(150,HEIGHT-100))
    flower_list.append(flower_new)
    wilted_list.append("happy")

def add_flowers():
    global game_over
    if (not game_over):
        new_flower()
        clock.schedule(add_flowers,4)

def check_wilt_times():
    global wilted_list, game_over, garden_happy
    if(len(wilted_list)>0):
        for wilted_since in wilted_list:
            if(not wilted_since == "happy"):
                time_wilted = int(time.time() - wilted_since)
                if(time_wilted > 10.0):
                    garden_happy = False
                    game_over = True
                    break


def wilt_flower():
    global flower_list, wilted_list, game_over
    if (not game_over):
        if(len(flower_list) > 0): 
            rand_flower = randint(0,len(flower_list) - 1)
            if(flower_list[rand_flower].image == "flower"):
                flower_list[rand_flower].image = "flower-wilt"
                wilted_list[rand_flower] = time.time()
        clock.schedule(wilt_flower,99)

def check_flower_collision():
    global cow, flower_list, wilted_list, game_over
    index = 0
    for flower in flower_list:
        if(flower.colliderect(cow) and flower.image == "flower-wilt"):
            flower.image = "flower"
            wilted_list[index] = "happy"
            break
        index = index + 1

def check_alien_collision():
   global game_over
   for alien in alien_list:
       if(alien.colliderect(cow)):
          cow.image = "zap"
          game_over = True
          break
       
def check_io_collision():
   global game_over
   for io in io_list:
       if(io.colliderect(cow)):
          cow.image = "zap"
          game_over = True
          break
      
def velocity():
    random_dir = randint(0,1)
    random_velocity = randint(2,3)
    if(random_dir == 0):
        return -random_velocity
    else:
        return random_velocity

def mutate():
    if (not game_over and len(flower_list) > 0):
        rand_flower = randint(0, len(flower_list) - 1)
        alien_pos_x = flower_list[rand_flower].x
        alien_pos_y = flower_list[rand_flower].y
        del flower_list[rand_flower]
        alien = Actor("alien")
        alien.pos = alien_pos_x, alien_pos_y
        alien_vx = velocity()
        alien_vy = velocity()
        alien = alien_list.append(alien)
        alien_vx_list.append(alien_vx)
        alien_vy_list.append(alien_vy)
        clock.schedule(mutate, 20)

def mutateIO():
    if (not game_over and len(flower_list) > 0):
        rand_flower = randint(0, len(flower_list) - 1)
        io_pos_x = flower_list[rand_flower].x
        ior_pos_y = flower_list[rand_flower].y
        del flower_list[rand_flower]
        io = Actor("io")
        io.pos = io_pos_x, ior_pos_y
        io_vx = velocity()
        io_vy = velocity()
        io = io_list.append(io)
        io_vx_list.append(io_vx)
        io_vy_list.append(io_vy)
        clock.schedule(mutateIO, 10)
    

def update_alien():
    if(not game_over):
        index = 0
        for alien in alien_list:
            alien_vx = alien_vx_list[index]
            alien_vy = alien_vy_list[index]
            alien.x = alien.x + alien_vx
            alien.y = alien.y + alien_vy
            if(alien.left < 0):
                alien_vx_list[index] = -alien_vx
            if(alien.right > WIDTH):
                alien_vx_list[index] = -alien_vx
            if(alien.top < 150):
                alien_vy_list[index] = -alien_vy
            if(alien.bottom > HEIGHT):
                alien_vy_list[index] = -alien_vy
            index = index + 1

def update_ios():
    if(not game_over):
        index = 0
        for io in io_list:
            io_vx = io_vx_list[index]
            io_vy = io_vy_list[index]
            io.x = io.x + io_vx
            io.y = io.y + io_vy
            if(io.left < 0):
                io_vx_list[index] = -io_vx
            if(io.right > WIDTH):
                io_vx_list[index] = -io_vx
            if(io.top < 150):
                io_vy_list[index] = -io_vy
            if(io.bottom > HEIGHT):
                io_vy_list[index] = -io_vy
            index = index + 1

def reset_cow():
    global game_over
    if (not game_over):
      cow.image = "cow"

def update():
  global game_over
  check_alien_collision()
  check_io_collision()
  check_wilt_times()
  if(not game_over):
    if(keyboard.space):
      cow.image = "cow-water"
      clock.schedule(reset_cow, 0.5)
      check_flower_collision()
    if(keyboard.left and cow.x > 0):
      cow.x -= 10
    if(keyboard.right and cow.x < WIDTH):
      cow.x += 10
    if(keyboard.up and cow.y > 150):
        cow.y -= 10
    if(keyboard.down and cow.y < WIDTH):
        cow.y += 10
    if(time_elapsed > 10 and len(alien_list)==0):
        mutate()
    if(time_elapsed > 5 and len(io_list)==0):
        mutateIO()
    update_alien()
    update_ios()

add_flowers()
wilt_flower()
pgzrun.go()  