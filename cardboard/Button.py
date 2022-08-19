import pygame
import time
from cardboard.Text import *

class Button:
	def __init__(self, x, y, widths,heights,text,image="cardboard/images/gui/button_neutral.png",command=None,toggle=False,disabled=False):
		self.image = pygame.image.load(image)
		width = self.image.get_width()
		self.text = text
		self.text_object = Text(self.text,(x,y))
		height = self.image.get_height()
		self.image = pygame.transform.scale(self.image, (int(widths), int(heights)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
		self.type = "button"
		self.toggle = toggle
		self.command = command
		self.widths = widths
		self.heights = heights
		self.x, self.y = x,y
		self.disabled = disabled
		self.pressed = False

	def parent_draw(self):
		surface = pygame.display.get_surface()
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		if not self.disabled:
			surface.blit(self.image, (self.rect.x, self.rect.y))
		elif self.disabled:
			self.image = pygame.image.load("cardboard/images/gui/button_locked.png")
			width = self.image.get_width()
			height = self.image.get_height()
			self.image = pygame.transform.scale(self.image, (int(self.widths), int(self.heights)))
			self.rect = self.image.get_rect()
			self.rect = self.image.get_rect()
			self.rect.topleft = (self.x, self.y)
			surface.blit(self.image, (self.rect.x, self.rect.y))

		if action and not self.disabled:
			if self.command != None:
				self.command()
			if self.toggle:
				if self.pressed:
					self.image = pygame.image.load("cardboard/images/gui/button_pressed.png")
					width = self.image.get_width()
					height = self.image.get_height()
					self.image = pygame.transform.scale(self.image, (int(self.widths), int(self.heights)))
					self.rect = self.image.get_rect()
					self.rect = self.image.get_rect()
					self.rect.topleft = (self.x, self.y)
					self.pressed = False
				elif not self.pressed:
					self.image = pygame.image.load("cardboard/images/gui/button_neutral.png")
					width = self.image.get_width()
					height = self.image.get_height()
					self.image = pygame.transform.scale(self.image, (int(self.widths), int(self.heights)))
					self.rect = self.image.get_rect()
					self.rect = self.image.get_rect()
					self.rect.topleft = (self.x, self.y)
					self.pressed = True
			elif not self.toggle:
				self.image = pygame.image.load("cardboard/images/gui/button_neutral.png")
				width = self.image.get_width()
				height = self.image.get_height()
				self.image = pygame.transform.scale(self.image, (int(self.widths), int(self.heights)))
				self.rect = self.image.get_rect()
				self.rect = self.image.get_rect()
				self.rect.topleft = (self.x, self.y)

		self.text_object.parent_draw()


