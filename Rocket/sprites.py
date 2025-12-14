import pygame
import random
import math

class Rocket(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()

        self.original_image = pygame.image.load("./sprites/Rocket_Sprite.png").convert_alpha()
        original_width, original_height = self.original_image.get_size()
        scale_factor = 0.2

        self.base_image = pygame.transform.smoothscale(self.original_image, (int(original_width * scale_factor), int(original_height * scale_factor)))

        # Pygame variables used by sprite
        self.image = self.base_image
        self.rect = self.image.get_rect()   # has to be called rect | is a rectangle the size of the image
        # (x, y) are the top left corner of the rectangle, we center it by subtracting the width and height of the rocket divided by 2
        self.rect.x = (screen.get_width() / 2) - (self.rect.width / 2)
        self.rect.y = screen.get_height() - 200 #  Keeps the rocket lower on the screen so we can see ahead

        # Custom variables
        self.fuel = 100
        self.engine_on = False
        self.fuel_timer = 0
        self.burn_rate = 0.1
        self.velocity = 0   #   Velocity speed for background
        self.angle = 0  #   0 degrees is straight up
        self.rotation_speed = 180   #   Degrees per second
        self.mask = pygame.mask.from_surface(self.image)
        self.distance = 0

    def start_engine(self):
        self.engine_on = True

    def stop_engine(self):
        self.engine_on = False
    
    @property
    def fuel(self):
        return self._fuel
    
    @fuel.setter
    def fuel(self, value):
        if value < 0:
            self._fuel = 0
        else:
            self._fuel = value
    
    def rotate(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.angle += self.rotation_speed * dt
        if keys[pygame.K_RIGHT]:
            self.angle -= self.rotation_speed * dt

        self.image = pygame.transform.rotozoom(self.base_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):   #  controls what the rocket does at each frame by rocket.update()

        self.rotate(dt)

        if self.engine_on and self.fuel > 0:
            self.velocity = 400   # Pixel per second "Upward" speed

            radians = math.radians(self.angle)
            horizontal_speed = -math.sin(radians) * self.velocity * dt
            self.rect.x += horizontal_speed
            self.distance += self.velocity * dt
            self.fuel_timer += dt
            if self.fuel_timer >= self.burn_rate:   #   Burns fuel every 10 sec
                self.fuel -= 1  #   Burn fuel
                self.fuel_timer = 0 #   Reset timer

        
        else:
            self.velocity = 0 # Stop moving if engine is off
            self.stop_engine()

    def reset(self):
        self.rect.centerx = 300
        self.rect.y = 600
        self.fuel = 100
        self.angle = 0
        self.velocity = 0
        self.engine_on = True
        self.fuel_timer = 0
        self.distance = 0
        self.image = self.base_image
        self.mask = pygame.mask.from_surface(self.image)

class Flame(pygame.sprite.Sprite):
    def __init__(self, rocket):
        super().__init__()
        self.rocket = rocket
        self.frames = []
        for i in range(1, 4):
            img = pygame.image.load(f"./sprites/flame_{i}.png").convert_alpha()
            w, h = img.get_size()
            scale = 0.4
            img = pygame.transform.smoothscale(img, (int(w * scale), int(h * scale)))
            self.frames.append(img)

            self.frame_index = 0
            self.animation_timer = 0
            self.animation_speed = 0.1  #   Switches flame every 0.1 seconds
            self.image = self.frames[0]
            self.rect = self.image.get_rect()
            self.offset_distance = 45  #   Distance from the center of the rocket to the nozzle
        
    def update(self, dt):
        if self.rocket.engine_on and self.rocket.fuel > 0:
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.frame_index += 1
                if self.frame_index >= len(self.frames):
                    self.frame_index = 0
                self.animation_timer = 0

            current_original_frame = self.frames[self.frame_index]
            self.image = pygame.transform.rotozoom(current_original_frame, self.rocket.angle, 1)
            offset_vector = pygame.math.Vector2(0, self.offset_distance)
            rotated_offset = offset_vector.rotate(-self.rocket.angle)
            self.rect = self.image.get_rect()
            center_x = self.rocket.rect.centerx + rotated_offset.x
            center_y = self.rocket.rect.centery + rotated_offset.y        
            self.rect.center = (center_x, center_y)
        
        else:
            self.image = pygame.Surface((0,0))


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, Window_height, color):
        super().__init__()

        self.image = pygame.Surface([width, Window_height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        self.mask = pygame.mask.from_surface(self.image)

class Stars:
    def __init__(self, screen, num_stars, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.stars = []

        for _ in range(num_stars):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, screen_height)
            speed_multiplier = random.uniform(0.2, 0.8) # With different speeds it looks like some are farther away than others

            self.stars.append([x, y, speed_multiplier])

    def update(self, base_speed, dt):
        # Base speed: How fast the rocket is flying "up" (how fast stars move down)
        for star in self.stars:
            star[1] += base_speed * star[2] * dt
            if star[1] > self.screen_height:
                star[1] = -5 #   Star sligtgtly above screen
                star[0] = random.randint(0, self.screen_width)  #   New random

    def draw(self, screen):
        for star in self.stars:
            pygame.draw.circle(screen, "white", (int(star[0]), int(star[1])), 1)

class FuelPackage(pygame.sprite.Sprite):
    def __init__(self, screen_width):
        super().__init__()

        self.radius = 15
        self.image = pygame.Surface((self.radius * 2, self.radius * 2)) # Create 30x30 square
        self.image.fill("black")    #   Make square transparent
        self.image.set_colorkey("black")

        pygame.draw.circle(self.image, "green", (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(30, screen_width - 50)
        self.rect.y = -50   #   Spawn just above visible screen

    def update(self, velocity, dt):

        self.rect.y += velocity * dt

        if self.rect.y > 1000:  #   If fuelpackage passes bottom of the screen
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, screen_width):
        super().__init__()

        self.radius = random.randint(15, 40)
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.fill("black")
        self.image.set_colorkey("black")

        pygame.draw.circle(self.image, "grey", (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(25, screen_width - 25 - (self.radius * 2))
        self.rect.y = -100
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self, velocity, dt):

        self.rect.y += velocity * dt

        if self.rect.y > 1000:
            self.kill()

