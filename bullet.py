import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	"""docstring for Bullet"""
	def __init__(self, ai_game):
		super().__init__()
		self.settings = ai_game.settings
		self.screen = ai_game.screen
		self.color = self.settings.bullet_color
		self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
		self.rect.midtop = ai_game.ship.rect.midtop
		self.y = float(self.rect.y)

	def update(self):
		self.y -= self.settings.bullet_speed
		self.rect.y = self.y
	def draw_b(self):
		pygame.draw.rect(self.screen, self.color, self.rect)