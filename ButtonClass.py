import pygame
from Config import *

class Button():
	def __init__(self,text,x,y,w,h,button_color=(89,89,89), font = "arial", bold=False):
		self.pos = (x,y)
		self.size = (w,h)
		self.font = font
		self.button_color = button_color
		self.hColor = tuple(min(x+65,255) for x in self.button_color)
		self.text = text
		self.highlighted = False
		self.font = pygame.font.SysFont(font,
			int(self.size[1]// (1 if self.text=="<<" else 1.7)), 
			bold = bold)

	def update(self, mouse):
		if (mouse[0]>=self.pos[0] and mouse[0]<=self.pos[0]+self.size[0]) and   (mouse[1]>=self.pos[1] and mouse[1]<=self.pos[1]+self.size[1]):
			self.highlighted = True
		else:
			self.highlighted = False


	def draw(self, window, text_color=BLACK):
		font = self.font.render(self.text, False, text_color)
		font_h = font.get_height()
		font_w = font.get_width()
		color = self.hColor if self.highlighted else self.button_color
		pygame.draw.rect(window, color,(self.pos, self.size), border_radius=4)
		pygame.draw.rect(window, GRAY, (self.pos, self.size),5, border_radius=4)
		font_x = self.pos[0] + (self.size[0] - font_w)//2
		font_y = self.pos[1] + (self.size[1] - font_h)//2
		window.blit(font,(font_x, font_y))
