import sys
import pygame
import random
from Game_settings import ship
from Sounds import sounds_effects
from pygame.sprite import Group, Sprite
from Game_settings import enemies, shooting_mechanics
from Images import explosions
from Display import score
from Display import ship_situation
from Saves import save_settings


def get_midpoint(point1, point2) -> tuple:
    return ((point1[0] + point2[0]) // 2, (point1[1] + point2[1]) // 2)


class Game:
    def __init__(self, width, height, *args):
        self.height = height
        self.width = width
        self.clock = pygame.time.Clock()
        self.pause_menu = args[0]
        self.menu_screen = args[1]
        self.menu_music = args[2]
        self.game_global = args[3]
        self.control = args[4]
        self.game_paused = False
        self.running = True
        self.display = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.image.load("Images/game_background.jpg")
        self.scaled = pygame.transform.scale(self.background, (self.width, self.height))
        self.highest_record = save_settings.load_score_from_json()

        self.save_score = save_settings.save_highest_score

    def game_screen(self) -> None:
        menu = self.pause_menu(self.width, self.height)
        alien_class = enemies.Aliens
        aliens_sprite = Group()
        enemy_bullet_sprite = Group()

        ship_sprite = Group()
        ship_instance = ship.Ship(self.display)
        ship_sprite.add(ship_instance)
        # print(ship_sprite)

        bullets = ship_instance.bullets
        rockets = ship_instance.rocket

        explosions_sprite = Group()

        shooting_effect = sounds_effects.GameEffects()
        escape_pressed = False  # Initialize the new flag
        spawn_event = pygame.USEREVENT + 1
        pygame.time.set_timer(spawn_event, 1000)
        alien_x = -1

        scoreboard = score.ScoreBoard(self.display, 32, (255, 255, 255))
        highest_score = score.HighestScore(self.display, 20, (255, 255, 255), self.highest_record)
        ship_characteristics = ship_situation.ShipCharacteristics(self.display, 32, (255, 255, 255))

        def handle_game_over():
            ship_instance.display_gameover_menu(self.display, 32, (255, 0, 145))
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                        # return False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            return True
                        elif event.key == pygame.K_SPACE:
                            return False
                pygame.display.flip()

        while self.running:
            ship_sprite.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()

                if ship_instance.current_health > 0:
                    if event.type == spawn_event:
                        new_alien = alien_class(self.display, alien_x)
                        alien_x = new_alien.rect.x
                        aliens_sprite.add(new_alien)

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE and not escape_pressed:
                            self.game_paused = True
                            menu.draw(self.display)
                            print("game is paused")
                            escape_pressed = True  # Set the flag to True when ESCAPE is pressed

                        if event.key == pygame.K_BACKSPACE and escape_pressed:
                            self.game_paused = False
                            print("Game on")
                            escape_pressed = False  # Reset the flag when BACKSPACE is pressed

                        if event.key == pygame.K_SPACE and escape_pressed:
                            self.running = False
                            self.game_paused = False
                            self.game_global = False
                            escape_pressed = False
                            self.menu_music()
                            return self.menu_screen

                        if event.type == pygame.KEYDOWN and not self.game_paused:
                            match event.key:
                                case pygame.K_LEFT:
                                    ship_instance.shooting("left")
                                    shooting_effect.ship_blasters()
                                case pygame.K_RIGHT:
                                    ship_instance.shooting("right")
                                    shooting_effect.ship_blasters()

                        if event.key == pygame.K_SPACE and not self.game_paused:
                            ship_instance.rocket_launch()
                            shooting_effect.ship_rocket()

            if self.game_paused:
                pass
            elif ship_instance.current_health <= 0:
                restart = handle_game_over()
                if restart:
                    if scoreboard.score > self.highest_record:
                        self.highest_record = scoreboard.score
                        self.save_score(self.highest_record)
                        highest_score.update(highest_score=save_settings.load_score_from_json())
                    self.game_screen()
                else:
                    self.running = False
                    self.game_paused = False
                    self.game_global = False
                    escape_pressed = False
                    self.menu_music()
                    return self.menu_screen

            else:
                self.display.blit(self.scaled, (0, 0))
                ship_instance.create_ship()
                ship_instance.draw_health_bar()
                ship_instance.update_movements(self.control["left"], self.control["right"],
                                               self.control["up"], self.control["down"])
                ship_instance.update_bullets()
                ship_instance.update_rockets()
                alien_class.update_enemies(aliens_sprite, self.display)

                collision_enemy_bullets = pygame.sprite.groupcollide(ship_sprite, enemy_bullet_sprite, False, True)
                for collision in collision_enemy_bullets:
                    collision.decrease_health_bar(10)
                    explosion = explosions.Explosion(self.display, collision.rect.center, "bullet")
                    explosions_sprite.add(explosion)

                collisions_bullets = pygame.sprite.groupcollide(bullets, aliens_sprite, True, True)
                for collision in collisions_bullets:
                    for alien in collisions_bullets[collision]:
                        # Create an explosion at the alien's position
                        explosion = explosions.Explosion(self.display, alien.rect.center, "bullet")
                        explosions_sprite.add(explosion)
                        shooting_effect.blaster_explosion()
                        scoreboard.update(10)

                collisions_rockets = pygame.sprite.groupcollide(rockets, aliens_sprite, True, False)

                for alien in aliens_sprite:
                    if random.randint(0, 75) == 0:  # Firing condition
                        projectile = alien.fire_launch()
                        if projectile:
                            enemy_bullet_sprite.add(projectile)

                for bullet in enemy_bullet_sprite.copy():
                    bullet.fire(enemy_bullet_sprite, bullet)
                enemy_bullet_sprite.draw(self.display)

                for collision in collisions_rockets:
                    explosion_type = "rocket"
                    scoreboard.update(10)

                    for hit_alien in collisions_rockets[collision]:
                        center = hit_alien.rect.center
                        explosion_radius = 150
                        for alien in aliens_sprite:
                            if alien != hit_alien and pygame.math.Vector2(alien.rect.center).distance_to(hit_alien.rect.center) < explosion_radius:
                                alien.kill()
                                alien_1 = alien.rect.center
                                alien_2 = hit_alien.rect.center
                                center = get_midpoint(alien_1, alien_2)
                                explosion_type = "big_boom"
                                aliens_sprite.remove(alien)
                                scoreboard.update(10)

                        explosion = explosions.Explosion(self.display, center, explosion_type)
                        explosions_sprite.add(explosion)
                        hit_alien.kill()
                        aliens_sprite.remove(hit_alien)
                        shooting_effect.rocket_explosion()
                explosions_sprite.update()
                explosions_sprite.draw(self.display)
                scoreboard.draw(self.display)
                highest_score.draw(self.display)
                ship_instance.check_rockets_reloading()
                ship_instance.check_bullet_reloading()
                ship_characteristics.draw_health_amount(ship_instance.current_health)
                ship_characteristics.draw_bullet_amount(ship_instance.bullets_amount, ship_instance.bullets_reloading)
                ship_characteristics.draw_rocket_amount(ship_instance.rockets_amount, ship_instance.rockets_reloading)
            pygame.display.flip()
            self.clock.tick(60)



