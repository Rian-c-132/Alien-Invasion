import sys
import pygame
from settings import Settings
from bullet import Bullet
from ship import *
from alien import Alien

class AlienInvasion:
	#manage game overall

	def __init__(self):
		pygame.init()
		self.settings = Settings()
		self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
		pygame.display.set_caption("Alien Invasion")
		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()
		self._create_fleet()
		
	def run(self):
		while True:
			self._check_events()
			self.ship.update()
			self._update_bullets()
			collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True )
			self._update_aliens()
			for bullet in self.bullets.copy():
				if bullet.rect.bottom <= 0:
					self.bullets.remove(bullet)
			self.bullets.update()
			self._update_screen()
	def _update_aliens(self):
		self._check_fleet_edges()
		self.aliens.update()
	def _check_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					self.ship.moving_right = True
				elif event.key == pygame.K_LEFT:
					self.ship.moving_left = True
				elif event.key == pygame.K_SPACE:
					self._fire()
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_RIGHT:
					self.ship.moving_right = False
				if event.key == pygame.K_LEFT:
					self.ship.moving_left = False
	def _create_fleet(self):
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_aliens_x = available_space_x // (2*alien_width)
		ship_height = self.ship.rect.height
		available_space_y = self.settings.screen_height - (2 * alien_height - ship_height)
		number_of_rows = available_space_y // (2 * alien_height)
		for row_number in range (number_of_rows):
			for alien_number in range (number_aliens_x):
				self._create_alien(alien_number, row_number)
	def _check_fleet_edges(self):
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break
	def _change_fleet_direction(self):
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1
	def _update_bullets(self):
		self.bullets.update()
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

			
	def _create_alien(self, alien_number, row_number):
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
		self.aliens.add(alien)

	def _fire(self):
		new_bullet = Bullet(self)
		self.bullets.add(new_bullet)
	def _update_screen(self):
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		
		for bullet in self.bullets.sprites():
			bullet.draw_b()
		self.aliens.draw(self.screen)
		pygame.display.flip()



if __name__ == '__main__':
	ai = AlienInvasion()
	ai.run()
