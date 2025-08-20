#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: addFriend.py
Description: This is on of the screens for TicTacToe it's used for connecting with other users

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

class AddFriend(GameState):
    """
    As names a class that defines the attributes of the Add Friend Screen State
    """
    def __init__(self):
        super(AddFriend, self).__init__()
        self.title = self.font.render("ADDFREIND", True, pg.Color("dodgerblue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.persist["screen_color"] = "G.BLACK"
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
        surface.fill(pg.Color(G.BG_COLOR))
