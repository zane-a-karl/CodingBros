#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: gameplay.py
Description: This is the gameplay screen for TicTacToe program contains all code related to the playing of the game

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

# Widgets
from button.button import Button
from button.checkbox import Checkbox

# Parent Class
from gamestate import GameState

# Globals
from globals import TicTacToeGlobals as G

# ===============
# End Imports
# ===============


class Square:
    def __init__(self, index, rect, state=0):
        self.index = index
        self.rect = rect
        self.state = state  # 0 = open, 1 = O, 2 = X

    def is_open(self):
        return self.state == 0
    
class Gameplay(GameState):
    def __init__(self):
        super(Gameplay, self).__init__()
        self.popup = None
        self.show_popup = False
        self.hovered_square = None # index of the square currently hovered, or None
        self.squares = [] # list of pg.Rect, index 0 - 8, left-to-right, top-to-bottom
        self.turn_font = pg.font.Font(G.EIGHT_BIT_FONT_PATH, 52)
        self.title_text = "Player 1's Turn" # Placeholder -- Will be updated to be dynamic (Probably show username or something)
        self.build_board()
        
    def startup(self, persistent):
        self.screen_color = pg.Color(G.BG_COLOR)
        self.user_token_type = persistent["user_token_type"]
        
        self.title = self.font.render("gameplay", True, pg.Color("gray10"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.verify_click(event)
        
    def update(self, dt):
        mouse_pos = pg.mouse.get_pos()
        self.hovered_square = None
        for square in self.squares:
            if square.rect.collidepoint(mouse_pos):
                self.hovered_square = square.index
                break

    def verify_click(self, event):
        """Verifies if the click was on an open square and applies the move"""
        for square in self.squares:
            if square.rect.collidepoint(event.pos):
                if square.is_open():
                    if(self.user_token_type == "X's"):
                        square.state = 2
                    else:
                        square.state = 1
                    self.title_text = "Computer's Turn..."
                else:
                    print("Square Taken") # Placeholder -- Will add sound and popup for bad choice later
                
    def build_board(self):
        """Builds the general board for drawing later"""
        sw = 150 # Square G.WIDTH
        x_start = self.screen_rect.centerx - sw - (sw/2)
        y_start = self.screen_rect.centery - sw - (sw/2)

        index = 0
        for row in range(3):
            for col in range(3):
                rect = pg.Rect(x_start + col * sw, y_start + row * sw, sw, sw)
                self.squares.append(Square(index, rect))
                index += 1
                 
    def draw(self, surface):
        """Main draw method that will draw all the individual components for the gameplay screen"""
        # Fill the background
        surface.fill(G.BG_COLOR)

        # Draw turn text
        self.draw_turn(surface)
        
        # Draw the Tic Tac Toe Board
        self.draw_board(surface)

    def draw_turn(self, surface):
        """Function that draws in whos turn it currently is on the top of the screen"""
        text_surface = self.turn_font.render(self.title_text, True, G.WHITE)
        text_rect = text_surface.get_rect()

        # Center the rectangle based on your screen size (e.g., 800x600)
        text_rect.center = (self.screen_rect.width // 2, self.screen_rect.top + 35)

        # Blit using the rect position instead of standard (X, Y) tuples
        surface.blit(text_surface, text_rect)

    def draw_x(self, surface, rect, color, thickness = 20, padding = 25):
        """Draw X on the inside of the hovered rectangle"""
        start_x = rect.left + padding
        end_x = rect.right - padding
        start_y = rect.top + padding
        end_y = rect.bottom - padding

        # Left to right
        pg.draw.line(surface, color, (start_x, start_y), (end_x, end_y), thickness)

        # Right to left
        pg.draw.line(surface, color, (end_x, start_y),(start_x, end_y), thickness)

    def draw_o(self, surface, rect, color, thickness = 20, padding = 25):
        """Draw Y on the inside of the hovered rectangle"""
        o_rect = rect.inflate(-padding * 2, -padding * 2)
        pg.draw.ellipse(surface, color, o_rect, thickness)
        
    def draw_board(self,surface):
        """Actual board drawn to screen"""

        lt = 12 # Line Thickness
        sw = 150 # Square G.WIDTH

        # Draw the placed marks
        for square in self.squares:
            if square.state == 2:
                self.draw_x(surface, square.rect, G.WHITE)
            elif square.state == 1:
                self.draw_o(surface, square.rect, G.WHITE)

        # Highlight hovered square
        if self.hovered_square is not None:
            hover_square = self.squares[self.hovered_square]
            if hover_square.is_open():
                if(self.user_token_type == "X's"):
                    self.draw_x(surface, hover_square.rect, G.HOVER_COLOR)
                elif(self.user_token_type == "O's"):
                    self.draw_o(surface, hover_square.rect, G.HOVER_COLOR)
                else:
                    print("Error - No Token Type")
        
        # Define boundaries
        x_start = self.screen_rect.centerx - sw - (sw/2)
        y_start = self.screen_rect.centery - sw - (sw/2)
        x_end = self.screen_rect.centerx + sw + (sw/2)
        y_end = self.screen_rect.centery + sw + (sw/2)
        
        # Vertical
        pg.draw.line(surface, G.BLACK, (x_start + sw, y_start), (x_start + sw, y_end), lt)
        pg.draw.line(surface, G.BLACK, (x_end - sw, y_start), (x_end - sw, y_end), lt)

        # Horizontal
        pg.draw.line(surface, G.BLACK, (x_start, y_start + sw), (x_end, y_start + sw), lt)
        pg.draw.line(surface, G.BLACK, (x_start, y_end - sw), (x_end, y_end - sw), lt)
