import pygame
import random
from sprites import Rocket, Wall, Stars, Flame, FuelPackage, Meteor


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 30)
game_over_font = pygame.font.SysFont("Areal", 60, bold=True)
game_over_color = "Red"
font_color = "White"
button_font = pygame.font.SysFont("Areal", 40, bold=True)

walls = pygame.sprite.Group()
left_wall = Wall(0,0, 20, WINDOW_HEIGHT, "Purple")
right_wall = Wall(WINDOW_WIDTH - 20, 0, 20, WINDOW_HEIGHT, "Purple")
walls.add(left_wall)
walls.add(right_wall)

background_stars = Stars(screen, 100, WINDOW_WIDTH, WINDOW_HEIGHT)

fuel_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()

rocket_body = Rocket(screen)
rocket = pygame.sprite.Group()
rocket.add(rocket_body)

rocket_flame = Flame(rocket_body)
flame = pygame.sprite.Group()
flame.add(rocket_flame)

button_rect = pygame.Rect(0,0,250,80)
button_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100)

def reset_game():
    rocket_body.reset()
    fuel_group.empty()  
    meteor_group.empty()

def main():
    dt = 0
    running = True
    game_over = False
    rocket_body.start_engine()

    fuel_timer = 0
    fuel_spawn_delay = 2.5
    fuel_refill_amount = 25

    meteor_timer = 0
    meteor_spawn_delay = 1.5

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:   #  pygame.QUIT Bruker klikket X for å lukke vinduet
                running = False 

            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:   #   Left mouse button
                    if button_rect.collidepoint(event.pos): #   Check if click was inside button
                        reset_game()
                        game_over = False     
        
        screen.fill("black")   #  Fills the screen with a color to wipe away anything from last frame

        if not game_over:

            current_speed = rocket_body.velocity
            background_stars.update(current_speed, dt)
            rocket.update(dt)
            flame.update(dt)
            fuel_group.update(current_speed, dt)
            meteor_group.update(current_speed, dt)

            meteor_timer += dt
            fuel_timer += dt

            if meteor_timer >= meteor_spawn_delay:
                meteor_timer = 0
                new_meteor = Meteor(WINDOW_WIDTH)
                meteor_group.add(new_meteor)
                meteor_spawn_delay = random.uniform(0.5, 1.8)

            if fuel_timer >= fuel_spawn_delay:
                fuel_timer = 0
                new_package = FuelPackage(WINDOW_WIDTH)
                fuel_group.add(new_package)

            if pygame.sprite.spritecollide(rocket_body, meteor_group, False, pygame.sprite.collide_mask):
                print("CRASH")
                game_over = True
                rocket_body.stop_engine()

            if pygame.sprite.spritecollide(rocket_body, walls, False, pygame.sprite.collide_mask):
                print("CRASH!")
                game_over = True
                rocket_body.stop_engine()

            if rocket_body.fuel == 0:
                print("EMPTY TANK!")
                game_over = True
                rocket.draw(screen)
            
            text_surface = font.render(f"Fuel: {str(rocket_body.fuel)}", True, font_color)  
            screen.blit(text_surface, (100,50))

            distance_text = font.render(f"Distance: {int(rocket_body.distance / 10)}m", True, font_color)
            screen.blit(distance_text, (300, 50))

            hits = pygame.sprite.spritecollide(rocket_body, fuel_group, True, pygame.sprite.collide_mask)
            for hit in hits:
                rocket_body.fuel += fuel_refill_amount

        else:
            text = game_over_font.render("GAME OVER", True, "Red")
            text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
            screen.blit(text, text_rect)

            score_text = font.render(f"Final Distance: {int(rocket_body.distance / 10)}m", True, "White")
            score_rect = score_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 40))
            screen.blit(score_text, score_rect)

            pygame.draw.rect(screen, "White", button_rect)
            pygame.draw.rect(screen, "Black", button_rect, 3) # Outline

            btn_text = button_font.render("Try Again", True, "Black")
            btn_text_rect = btn_text.get_rect(center=button_rect.center)
            screen.blit(btn_text, btn_text_rect)
                
        background_stars.draw(screen)    
        walls.draw(screen)
        fuel_group.draw(screen)
        meteor_group.draw(screen)
        flame.draw(screen)
        rocket.draw(screen)
        

        pygame.display.flip()   #   Renders the work to the screen.

        dt = clock.tick(60) / 1000  #  dt is delta time in seconds since last frame, used for framerate-independent physics

    pygame.quit()

if __name__ == "__main__":
    main()
    


