#!/usr/bin/env python
# python2.7, pygame 1.9.1
# pong clone using pygame
# Daniel Browne (jairuncaloth@gmail.com)

import pygame 
from pygame.locals import *


class Pong:
  # Handles creating and managing the game area and game objects

  def __init__(self):
    self.running = True
    pygame.init()
    self.size = self.width, self.height = 800, 600 
    self.display_surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
   
  def on_event(self, event):
    if event.type == pygame.QUIT:
      self.running = False

    # up and down controls right paddle
    elif event.type == KEYDOWN and event.key == K_UP:
      self.right_paddle.move_up()
    elif event.type == KEYDOWN and event.key == K_DOWN:
      self.right_paddle.move_down()
    elif event.type == KEYUP and (event.key == K_UP or event.key == K_DOWN):
      self.right_paddle.move_stop()

    # 's' and 'w' controls left paddle
    elif event.type == KEYDOWN and event.key == K_w:
      self.left_paddle.move_up()
    elif event.type == KEYDOWN and event.key == K_s:
      self.left_paddle.move_down()
    elif event.type == KEYUP and (event.key == K_w or event.key == K_s):
      self.left_paddle.move_stop()

  def on_loop(self):
    self.game_ball.bounce_vert()
    if self.game_ball.pos[0] - self.left_paddle.pos[0] <= self.game_ball.radius:
      if (self.left_paddle.pos[1] - (self.left_paddle.length / 2) <= self.game_ball.pos[1]
          and self.left_paddle.pos[1] + (self.left_paddle.length / 2) >= self.game_ball.pos[1]):
        self.game_ball.bounce_horiz()

    elif self.width - self.game_ball.pos[0] - (self.width - self.right_paddle.pos[0]) <= self.game_ball.radius:
      if (self.right_paddle.pos[1] - (self.right_paddle.length / 2) <= self.game_ball.pos[1]
          and self.right_paddle.pos[1] + (self.right_paddle.length / 2) >= self.game_ball.pos[1]):
        self.game_ball.bounce_horiz()

  def on_render(self):
    # draw the playing area
    self.display_surface.fill((0, 0, 0))
    pygame.draw.line(self.display_surface, (255,255,255), (self.width / 2, 0), (self.width / 2, self.height), 4)

    # draw the paddles and the ball
    self.game_ball.draw(self.display_surface, self.width, self.height)
    self.left_paddle.draw(self.display_surface)
    self.right_paddle.draw(self.display_surface)

    pygame.display.flip()
    self.clock.tick(60)

  def on_cleanup(self):
    pygame.quit()

  def on_execute(self):
    # create instances of the ball and paddles
    self.game_ball = Ball()
    self.left_paddle = Paddle([20, self.height / 2])
    self.right_paddle = Paddle([self.width - 20, self.height/ 2])
    self.clock = pygame.time.Clock()

    while self.running:
      for event in pygame.event.get():
        self.on_event(event)
      self.on_loop()
      self.on_render()
    self.on_cleanup()


class Ball:
  # Creates a ball and moves it around the screen

  def __init__(self):
    self.radius = 20
    self.color = (255, 255, 255)
    self.velocity = [-1, -1]
    self.pos = [400, 300]
    self.screen_width = game.display_surface.get_width()
    self.screen_height = game.display_surface.get_height()
    
  def draw(self, surface, screen_width, screen_height):
    self.screen_height = screen_height
    self.screen_width = screen_width
    pygame.draw.circle(surface, self.color, self.pos, self.radius)

    self.pos[0] += self.velocity[0]
    self.pos[1] += self.velocity[1]

  def bounce_horiz(self):
    #if self.pos[0] <= self.radius or game.display_surface.get_width() - self.pos[0] <= self.radius:
      self.velocity[0] = -self.velocity[0]

  def bounce_vert(self):
    if self.pos[1] <= self.radius or game.display_surface.get_height() - self.pos[1] <= self.radius:
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