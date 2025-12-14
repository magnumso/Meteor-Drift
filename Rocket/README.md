# Meteor Drift!
### Video Demo:

## 1. Project overview
In "Meteor Drift" you are piloting a rocket and the objective is to make it as far as possible while avoiding collisions with both the walls on the left and rights side of the screen as well as incomming meteors. In addition, to keep the rocket going you have to collect fuel supplies to avoid the rocket fuel store from depleting. 

## 2. Game mechanic and design
The game is sopposed to make it look like you are flying through space in in the rocket ship. To give the illusion that you are flying forward, the trick is to actually make everything else move downward. To do this we just move all the objects down at each pass through the game loop at the "speed" we want the rocket to move. To controll the rocket i decided to use the arrow keys which is common for these types of games. The game is lost if the player collides with either the walls on the sides of the screen or a meteor. The player also has to collect fuel packages to keep the rocket going forward and looses if the fuel runs out. 

## 3. Code breakdown
### Files:
In the project folder we have two python files called "sprites.py" and "game.py" and a folder called "sprites" containing the sprite images which make up the visual part of the moving objects in the game.

### sprites(folder):
This folder contains the sprite images used for the moving parts in the game such as the rocket ship, the flames comming out of the engine and the meteors. These images where made using pixelapp.com which is a free online sprite editor for creating pixel art. 

### sprites.py
This file contains all the classes of all the objects in the game. By creating these in a separate file it made the game.py file smaller and easier to work with. All the objects are classes with different properties which make them react in certain ways in the game. All visible objects except form the stars inherit from pygame.sprite.Sprite which allows us to use Pygame's group rendering and collision systems.

#### 1. Class: Rocket
In the Rocket class the rocket sprite image gets loaded and resized by a factor to make it the right size for our game. The image also goes through a few transformation steps which helps with performance as well as better collision detection. Then we create a rectangle object using the image and set its initial (x, y) position at the lower middle of the screen so that we have a longer time to react to the incoming objects. Next we initialize some variables the rocket uses.

* **start_engine, stop_engine**:
Sets the engine_on to true or false


* **fuel**:
I added a getter and setter method to the fuel so that we can add and subtract from it like a normal variable

* **rotate**:
Checks whether the right or left arrow keys have been pressed and then rotates the rocket on that direction

* **update**:
Each sprite is updated at head pass through the game loop and the update function checks for states and decides if values should be updated. In the case of the rocket, the fuel gets burned every pass-through  if the rocket still has fuel left. It also calculates the new angle, speed and x position of the rocket.

* **reset**:
The reset function resets all the values to their initial values and is called when the “try again” button is pressed so that the game can start fresh.

#### 2. Class: Flame
To make the flame coming out of the rocket to look like its burning i used three different size images of flames and cycled through them. The flame class handles this by using a for loop and  changing the image three times per pass through the game loop.

#### 3. Class: Wall
The Wall class creates two walls using pygame.Surface, these walls ends the game if the rocket collides with them, the same as with the meteors. I added them to make the game slightly harder since catching fuel close to the walls added some difficulty

#### 4. Class: Stars
To make it look as if the rocket is in space i wanted to add stars in the background. We start by having a for loop assign random (x, y) values to n number of stars and then we add a different speeds to each star so that they look like some are further away than others. and add these stars to a list

* **update**:
In the update function which is called at each pass through the game loop, We calculate its speed which is based on its speed multiplier and the speed of the rocket. Since its actually all the other objects that are moving downwards and not the rocket that is moving upwards. The rocket speed is added to the stars as well. Then if stars reach past the bottom of the screen i.e out of frame, then they are removed and ned ones are spawned at a little over the top of the screen.

* **draw**:
This function draws the stars on the screen from the stars list using the draw.circle function from pygame.

#### 5. Class: FuelPackage
The FuelPackage class creates the circle objects and gives them a random x position between the walls at a few pixels over the frame, then at each pass through the game loop, the y position is updated by the velocity so the object falls downwards.

#### 6. Class: Meteor
Creates circle objects and give them a random x position above the frame between the walls and at each pass through the loop the x position is changed so that the object "falls" downwards.

### game.py
In game.py we import the sprites we are going to use from sprites.py, then we start by initialyzing the pygame screen, all the sprite objects we created as well as other variables like font which we are going to be using in the game loop.

* **reset_game**:
Calls the reset function on our rocket object as well as removes all the fuel packages from screen.

* **main**:
This is our game loop function, we start off by creating some variables we will be using in the loop like the running variable which will decide whether the game is running or stopped. 

In the while loop we check the players mouse actions and if they perform actions like clicking the exit button, then the game exits or if they press the “try again” button after losing then the game resets.

For each pass through the screen gets wiped to get rid of everything from the previous loop so that it can draw all the objects with their new positions. Then it checks whether the game is still going and if it is, then it updates all the objects on the screen using the update() function. It also checks for collisions between the rocket and other objects by using the spritecollide function from pygame. If the rocket collides with the walls or the meteors then the game_over variable is set to true.  It also checks whether we collide with the fuel packages. If we do then the fuel storage is refilled by the refill amount we initialized earlier. Next the fuel amount and the distance is updated and shown on the screen. Later all the objects are drawn to the screen, rendered and then the next pass through the loop starts.


