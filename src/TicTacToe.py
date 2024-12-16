#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: TicTacToe.py
Description: This is the main file for the TicTacToe Program

Author: Coding Bros
Email: See team info <project_root>/misc/teamInfo.txt
Date Created: 2024-10-13
Last Modified: 2024-10-31
Version: 1.0

Dependencies:
    - pygame
"""

# Imports
import sys
import pygame as pg
from button import Button

## GLOBALS ##
WIDTH = 600
BLACK = (0,0,0)
WHITE = (255,255,255)
ORANGE = (255,180,0)
GREEN = (106,168,79)
BG_COLOR = (67,67,67)

# Local Classes
class Game(object):
    """
    A single instance of this class is responsible for 
    managing which individual game state is active
    and keeping it updated. It also handles many of
    pygame's nuts and bolts (managing the event 
    queue, framerate, updating the display, etc.). 
    and its run method serves as the "game loop".
    """
    def __init__(self, screen, states, start_state):
        """
        Initializes the Game Object
        
        Screen: The Pygame display surface
        States: A dict mapping of the state-names to the GameState Objects
        Start_state: The Name of the First active game state
        """
        self.done = False
        self.screen = screen
        self.clock = pg.time.Clock()
        self.fps = 60
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]

    def event_loop(self):
        """Events are passed for handling to the current state"""
        for event in pg.event.get():
            self.state.get_event(event)

    def flip_state(self):
        """Switches to the next game state"""
        current_state = self.state_name
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        persistent = self.state.persist
        self.state = self.states[self.state_name]
        self.state.startup(persistent)

    def update(self, dt):
        """
        Check for state flip and update the active state
        
        dt: ms since the last frame
        """
        if self.state.quit:
            self.done = True

        elif self.state.done:
            self.flip_state()

        self.state.update(dt)

    def draw(self):
        """Pass display surface to active state for drawing"""
        self.state.draw(self.screen)

    def run(self):
        """The while loop where the games runtime will be spent inside"""
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            pg.display.update()

class GameState(object):
    """
    Parent class for individual game states to inherit from. 
    """
    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pg.display.get_surface().get_rect()
        self.persist = {}
        self.font = pg.font.Font(None, 24)

    def startup(self, persistent):
        """
        Called when a state resumes being active.
        Allows information to be passed between states.
        
        persistent: A dict passed from state to state
        """
        self.persist = persistent        
        
    def get_event(self, event):
        """
        Handle a single event passed by the Game object.
        """
        pass
        
    def update(self, dt):
        """
        Update the state. Called by the Game object once
        per frame. 
        
        dt: time since last frame
        """
        pass
        
    def draw(self, surface):
        """
        Draw everything to the screen.
        """
        pass

class SplashScreen(GameState):
    """
    As names a class that defines the attributes of the Splash Screen State
    """
    def __init__(self):
        super(SplashScreen, self).__init__()

        # Title
        title_font = pg.font.Font("../misc/Eight-Bit Madness.ttf", 72)
        self.title = title_font.render("TIC - TAC - TOE", True, WHITE)
        self.title_rect = self.title.get_rect()
        self.title_rect.center = (self.screen_rect.centerx, self.screen_rect.top + 50)
        splashScreenImage = pg.image.load('../images/splashScreenCenter.png').convert_alpha()
        self.splashScreenImage = CustomGameImage(300 - (splashScreenImage.get_width() * .5)/2, 
                                                 self.screen_rect.top + 125, 
                                                 splashScreenImage, 
                                                 0.5)
        
        # Setup
        self.persist["screen_color"] = "black"
        self.next_state = "GAMEPLAY"

        # Buttons/Labels
        BUTTON_STYLE = {"hover_font_color" : ORANGE,
                        "font" : pg.font.Font("../misc/Eight-Bit Madness.ttf", 42),
                        "font_color": WHITE,
                        "hover_font_color": BLACK,
                        "hover_color": GREEN,
                        "hover_sound" : pg.mixer.Sound("../misc/blipshort1.wav")}
        
        self.singlePlayerBut = Button((0,0,350,35),
                            ORANGE, 
                            self.single_play_selected,
                            text="SINGLE PLAYER", 
                            **BUTTON_STYLE)
        
        self.addPlayerBut = Button((0,0,350,35),
                             ORANGE, 
                             self.change_color,
                             text="ADD FRIEND", 
                             **BUTTON_STYLE)
        
        self.onlinePlayBut = Button((0,0,350,35),
                             ORANGE, 
                             self.change_color,
                             text="ONLINE PLAY", 
                             **BUTTON_STYLE)
        
        self.exitBut = Button((0,0,350,35),
                             ORANGE,
                             self.exit,
                             text="EXIT", 
                             **BUTTON_STYLE)
         
        self.singlePlayerBut.rect.center = (self.screen_rect.centerx, self.screen_rect.bottom - 250)
        self.addPlayerBut.rect.center = (self.screen_rect.centerx, self.screen_rect.bottom - 200)
        self.onlinePlayBut.rect.center = (self.screen_rect.centerx, self.screen_rect.bottom - 150)
        self.exitBut.rect.center = (self.screen_rect.centerx, self.screen_rect.bottom - 100)
        self.button_list = [self.singlePlayerBut, self.addPlayerBut, self.onlinePlayBut, self.exitBut]

    def single_play_selected(self):
        self.next_state = "GAMEPLAY"
        self.done = True

    def get_event(self, event):
        for button in self.button_list:
            button.check_event(event)
    
    def exit(self):
        self.quit = True
    
    def change_color(self):
        pass
        
    def draw(self, surface):
        # Background
        surface.fill(pg.Color(BG_COLOR))
        surface.blit(self.title, self.title_rect)
        self.splashScreenImage.draw(surface)
        for button in self.button_list:
            button.update(surface)

    def change_state(self, state):
        self.next_state = state
        self.done = True

class AddFriend(GameState):
    """
    As names a class that defines the attributes of the Add Friend Screen State
    """
    def __init__(self):
        super(AddFriend, self).__init__()
        self.title = self.font.render("ADDFREIND", True, pg.Color("dodgerblue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.persist["screen_color"] = "black"
        self.next_state = "SPLASH"
        
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            self.persist["screen_color"] = "gold"
            self.done = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.persist["screen_color"] = "dodgerblue"
            self.done = True
    
    def draw(self, surface):
        # Background
        surface.fill(pg.Color(BACKGROUND_COLOR))

class Gameplay(GameState):
    def __init__(self):
        super(Gameplay, self).__init__()
        

        # self.rect = pg.Rect((0, 0), (128, 128))
        # self.x_velocity = 1
        
    def startup(self, persistent):
        self.screen_color = pg.Color(BG_COLOR)
        self.title = self.font.render("gameplay", True, pg.Color("gray10"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.title_rect.center = event.pos
        
    def update(self, dt):
        pass
        # self.rect.move_ip(self.x_velocity, 0)
        # if (self.rect.right > self.screen_rect.right
        #     or self.rect.left < self.screen_rect.left):
        #     self.x_velocity *= -1
        #     self.rect.clamp_ip(self.screen_rect)
                 
    def draw(self, surface):
        surface.fill(BG_COLOR)
        rect = pg.Rect(100, 100, 300, 200)  # Position and size (x, y, width, height)
        pg.draw.rect(surface, BLACK, rect, border_radius=20)  # Set border_radius to round corners
        # surface.blit(self.title, self.title_rect)
        # pg.draw.rect(surface, pg.Color("darkgreen"), self.rect)

class CustomGameImage():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pg.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
    
    def draw(self, screen):
        # Draw the button on the screen
        screen.blit(self.image, (self.rect.x, self.rect.y))

class OldButton():
    """
    Generic Button class that can be used to create a button out of a image/shape
    """
    def __init__(self, x, y, image, image_hover, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pg.transform.scale(image, (int(width * scale), int(height * scale)))
        self.image_hover = pg.transform.scale(image_hover, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        self.current_image = self.image
    
    def draw(self, screen):
        # Default action state
        action = False
        
        # Get the mouse position
        pos = pg.mouse.get_pos()

        # Check Mouse Over and click
        if(self.rect.collidepoint(pos)):
            self.current_image = self.image_hover
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False: # Left Click
                self.clicked = True
                action = True

        # Reset Click
        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw the button on the screen
        screen.blit(self.current_image, (self.rect.x, self.rect.y))

        return action

def main():
    # Initial Pygame Screen/Window Setup
    pg.init()
    pg.display.set_caption("Coding Bros Tic Tac Toe")
    screen = pg.display.set_mode((WIDTH, WIDTH))

    # Define the different game states - The Screens that will exist
    states = {"SPLASH": SplashScreen(), 
              "GAMEPLAY": Gameplay(),
              "ADDFRIEND": AddFriend()
              }

    # Create a Game object - The Brain/Coordinator for State logic
    game = Game(screen, states, "SPLASH")

    # Start the Game - Game/While Loop that runs for the duration of the game
    game.run()

    # Exit Sequence
    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()
