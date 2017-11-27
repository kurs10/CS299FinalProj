import pygame, pygame.font, pygame.event, pygame.draw, string,sys
from pygame.locals import *

def getKey():
  while 1:
    event = pygame.event.poll()
    # If key pressed
    if event.type == KEYDOWN:
      return event.key
    # Else if x exit box pressed
    elif event.type == pygame.QUIT:
      pygame.display.quit()
      pygame.quit()
      sys.exit(0)
    # Anything else skip
    else:
      pass

def display(screen, message):
  x = 110 # x-position
  y = 375 # y-position
  w = 425 # width of box
  h = 50 # height of box
  fontobject = pygame.font.Font("freesansbold.ttf",48)
  # Draws black box
  pygame.draw.rect(screen, (0, 0, 0),(x,y,w,h), 0)
  # Draws white box outline 
  pygame.draw.rect(screen, (255,255,255),(x-5,y-5,w,h+5), 1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (255,255,255)),(x, y))
  # Updates display
  pygame.display.flip()

def ask(screen, question):
  pygame.font.init()
  current_string = [] #holds input
  display(screen, question + ": " + "".join(map(str,current_string)))
  num = 0
  while 1:    
    inkey = getKey()
    # Delete character
    if inkey == K_BACKSPACE:
      current_string = current_string[0:-1]
      if num >= 1:
        num = num - 1
    # Exit and return input
    elif inkey == K_RETURN:
      break
    # Add character and length not longer than 9
    elif inkey <= 127 and num < 9:
      current_string.append(chr(inkey))
      num = num + 1
    # Update display
    display(screen, question + ": " + "".join(map(str,current_string)))
  return "".join(map(str,current_string))

'''
screen= pygame.display.set_mode((640, 480))
print (ask(screen, "Name") + " was entered")
pygame.display.quit()
pygame.quit()
'''
