#!/usr/bin/python
# python2.7, pygame 1.9.1
# pong clone using pygame
# Daniel Browne (jairuncaloth@gmail.com)
import random
import math
import pygame 
from pygame.locals import *

def dist(p,q):
    return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)

class Pong:
  # Handles creating and managing the game area and game objects

  def __init__(self):
    self.running = True
    pygame.init()
    self.size = self.width, self.height = 800, 600 
    self.display_surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
    self.player1_score = 0
    self.player2_score = 0
   
  def on_event(self, event):
    key_dict = {K_UP: [self.right_paddle.move_up, self.right_paddle.move_stop], K_DOWN: [self.right_paddle.move_down, self.right_paddle.move_stop],
                K_w: [self.left_paddle.move_up, self.left_paddle.move_stop], K_s: [self.left_paddle.move_down, self.left_paddle.move_stop]}

    if event.type == pygame.QUIT:
      self.running = False
    elif event.type == KEYDOWN and event.key in key_dict:
      key_dict[event.key][0]()
    elif event.type == KEYUP and event.key in key_dict:
      key_dict[event.key][1]()
  
  def collisions(self, left_paddle, right_paddle, ball):
    # top/bottom wall collision detection
    if ball.pos[1] <= ball.radius or self.height - ball.pos[1] <= ball.radius:
      ball.bounce_vert()
    
    # left/right paddle collisions
    if ball.pos[0] - left_paddle.pos[0] <= ball.radius:
        if (left_paddle.pos[1] - (left_paddle.length / 2) <= ball.pos[1]
            and left_paddle.pos[1] + (left_paddle.length / 2) >= ball.pos[1]):
           ball.bounce_horiz()
    elif self.width - ball.pos[0] - (self.width - right_paddle.pos[0]) <= ball.radius:
      if (right_paddle.pos[1] - (right_paddle.length / 2) <= ball.pos[1]
          and right_paddle.pos[1] + (right_paddle.length / 2) >= ball.pos[1]):
        ball.bounce_horiz()
        

  def on_loop(self):

    self.collisions(self.left_paddle, self.right_paddle, self.game_ball)
    
    if self.game_ball.pos[0] < 0:
      self.player2_score += 1
      self.on_execute()
    elif self.game_ball.pos[0] > self.width:
      self.player1_score += 1
      self.on_execute()

  def on_render(self):
    # draw the playing area
    self.display_surface.fill((0, 0, 0))
    pygame.draw.line(self.display_surface, (255,255,255), (self.width / 2, 0), (self.width / 2, self.height), 4)

    # draw the paddles and the ball
    self.game_ball.draw(self.display_surface, self.width, self.height)
    self.left_paddle.draw(self.display_surface)
    self.right_paddle.draw(self.display_surface)

    # display the score
    p1_score_display = self.font.render(str(self.player1_score), True, (255, 255, 255))
    self.display_surface.blit(p1_score_display, ((self.width / 2) - 130, 100))
    p2_score_display = self.font.render(str(self.player2_score), True ,(255, 255, 255))
    self.display_surface.blit(p2_score_display, ((self.width / 2) + 100, 100))

    pygame.display.flip()
    self.clock.tick(60)

  def on_cleanup(self):
    pygame.quit()

  def reset(self):
    self.game_ball = Ball()


  def on_execute(self):
    # create instances of the ball and paddles
    rand_vel_list = (-3, -2, -1, 1, 2, 3)
    rand_vel = [random.choice(rand_vel_list), random.choice(rand_vel_list)]
    self.game_ball = Ball(rand_vel)
    self.left_paddle = Paddle([20, self.height / 2])
    self.right_paddle = Paddle([self.width - 20, self.height/ 2])
    
    self.font = pygame.font.SysFont('Arial', 42, True)
    self.clock = pygame.time.Clock()

    while self.running:
      for event in pygame.event.get():
        self.on_event(event)
      self.on_loop()
      self.on_render()
    self.on_cleanup()


class Ball:
  # Creates a ball and moves it around the screen

  def __init__(self, velocity = [0, 0]):
    self.radius = 20
    self.color = (255, 255, 255)
    self.velocity = velocity
    self.pos = [400, 300]
    self.screen_width = game.display_surface.get_width()
    self.screen_height = game.display_surface.get_height()
    
  def draw(self, surface, screen_width, screen_height):
    self.screen_height = screen_height
    self.screen_width = screen_width
    pygame.draw.circle(surface, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)

    self.pos[0] += self.velocity[0]
    self.pos[1] += self.velocity[1]

  def bounce_horiz(self):
   #if self.pos[0] <= self.radius or game.display_surface.get_width() - self.pos[0] <= self.radius:
    self.velocity[0] = -(self.velocity[0] + (self.velocity[0] * .1))
    self.velocity[1] += self.velocity[1] * .1

  def bounce_vert(self):
   #if self.pos[1] <= self.radius or game.display_surface.get_height() - self.pos[1] <= self.radius:
    self.velocity[1] = -self.velocity[1]


class Paddle:
  # Creates a paddle and provides methods to move it

  def __init__(self, pos):
    self.length = 80
    self.width = 8
    self.pos = pos
    self.velocity = 0

  def draw(self, surface):
    pygame.draw.line(surface, 
                    (255,255,255), 
                    (self.pos[0], self.pos[1] - (self.length / 2)), 
                    (self.pos[0], self.pos[1] + (self.length / 2)), 
                    self.width)
    # only allow paddle to move if it will stay on the screen
    if (self.pos[1] + (self.length / 2) + self.velocity <= 600 and 
        self.pos[1] - (self.length / 2) + self.velocity >= 0):
      self.pos[1] += self.velocity

  def move_up(self):
    self.velocity = -4

  def move_down(self):
    self.velocity = 4

  def move_stop(self):
    self.velocity = 0


if __name__ == '__main__':
  game = Pong()
  game.on_execute()
