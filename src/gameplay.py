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

class Gameplay(GameState):
    def __init__(self):
        super(Gameplay, self).__init__()
        self.popup = None
        self.show_popup = False

        # self.rect = pg.Rect((0, 0), (128, 128))
        # self.x_velocity = 1
        
    def startup(self, persistent):
        self.screen_color = pg.Color(G.BG_COLOR)
        
        self.title = self.font.render("gameplay", True, pg.Color("gray10"))
        #self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        
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
        # Fill the background
        surface.fill(G.BG_COLOR)
        
        # Draw the Tic Tac Toe Board
        self.draw_board(surface)

        # rect = pg.Rect(100, 100, 300, 200)  # Position and size (x, y, G.WIDTH, height)
        # pg.draw.rect(surface, G.BLACK, rect, border_radius=20)  # Set border_radius to round corners
        
    def draw_board(self,surface):
        lt = 12 # Line Thickness
        sw = 150 # Square G.WIDTH
        x_start = self.screen_rect.centerx - sw - (sw/2)
        x_end = self.screen_rect.centerx + sw + (sw/2)
        y_start = self.screen_rect.centery - sw - (sw/2)
        y_end = self.screen_rect.centery + sw + (sw/2)
        
        # Vertical
        pg.draw.line(surface, G.BLACK, (x_start + sw, y_start), (x_start + sw, y_end), lt)
        pg.draw.line(surface, G.BLACK, (x_end - sw, y_start), (x_end - sw, y_end), lt)

        # Horizontal
        pg.draw.line(surface, G.BLACK, (x_start, y_start + sw), (x_end, y_start + sw), lt)
        pg.draw.line(surface, G.BLACK, (x_start, y_end - sw), (x_end, y_end - sw), lt)
