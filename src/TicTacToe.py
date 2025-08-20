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
"""

# ===============
# Start Imports
# ===============

# Basic
import sys
import pygame as pg

# Screens
from splash import SplashScreen
from singleplay import SelectSinglePlayOptions
from gamestate import GameState
from addFriend import AddFriend
from gameplay import Gameplay

# Global Variables
from globals import TicTacToeGlobals as G

# ===============
# End Imports
# ===============

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
            if self.state_name == "SINGLE_GAMEPLAY_OPTIONS":
                self.state.reset_initial_values(self.screen)

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

def main():
    # Initial Pygame Screen/Window Setup
    pg.init()
    pg.display.set_caption("Coding Bros Tic Tac Toe")
    screen = pg.display.set_mode((G.WIDTH, G.WIDTH))

    # Define the different game states - The Screens that will exist
    states = {"SPLASH": SplashScreen(), 
              "SINGLE_GAMEPLAY_OPTIONS": SelectSinglePlayOptions(),
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
