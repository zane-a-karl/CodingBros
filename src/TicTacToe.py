#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: TicTacToe.py
Description: This is the main file for the TicTacToe Program

Author: Coding Bros
Email: See team info <project_root>/misc/teamInfo.txt
Date Created: 2024-10-13
Last Modified: 2024-10-13
Version: 1.0

Dependencies:
    - pygame
"""

# Imports
import pygame

## GLOBALS ##
# Pygame Window Information - Move to better location
WIDTH = 600
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("Coding Bros Tic Tac Toe")

# Colors for use in visualization - Move to Support file
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE= (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


def show_start_screen(window):
    """
    Called at the beginning to show starting screen for user.
    
    Args:
        window (pygame element): Pygame window element.
        
    Returns:
        n/a.
    """
    window.fill(GREEN)
    pygame.display.update()

def main():
    """
    Main routinue that runs while the game is being played. Processes all user action.
    
    Args:
        n/a
        
    Returns:
        n/a
    """
    # Initialize Locals
    quit = False

    # Show Start Screen
    show_start_screen(WIN)

    # Loop while game is being played
    while(quit == False):
        # Update the display
        pygame.display.update()

        # Process the Current Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
                print("Quit Signal Received")
    pygame.quit()

if __name__ == "__main__":
    main()