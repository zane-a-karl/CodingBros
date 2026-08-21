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
    Defines the attributes of the Add Friend Screen State
    """
    def __init__(self):
        super(AddFriend, self).__init__()

        # Setup
        self.persist["screen_color"] = "G.BLACK"
        self.next_state = "NONE"
        self.button_list = []
        self.text_dict = {}
        self.surfaces_list = {}

        # Title
        title_font = pg.font.Font(G.EIGHT_BIT_FONT_PATH, 72)
        title = title_font.render("Add Friend", True, G.WHITE)
        title_rect = title.get_rect()
        title_rect.center = (self.screen_rect.centerx, self.screen_rect.top + 50)

        # Buttons
        button_gap = 300
        BUTTON_STYLE = {"hover_font_color" : G.ORANGE,
                        "font" : pg.font.Font(G.EIGHT_BIT_FONT_PATH, 42),
                        "font_color": G.WHITE,
                        "hover_font_color": G.BLACK,
                        "hover_color": G.GREEN,
                        "hover_sound" : pg.mixer.Sound(G.BLIP_SHORT_SOUND_PATH)}
        self.nextBut = Button((0,0,225,35),
                                G.ORANGE, 
                                self.return_home,
                                text="NEXT", 
                                **BUTTON_STYLE)
        self.backBut = Button((0,0,225,35),
                                G.ORANGE,
                                self.return_home,
                                text="BACK", 
                                **BUTTON_STYLE)
        self.backBut.rect.center = (self.screen_rect.centerx - button_gap/2, 
                                    self.screen_rect.bottom - 100)
        self.nextBut.rect.center = (self.screen_rect.centerx + button_gap/2, 
                                        self.screen_rect.bottom - 100)

        # Add widgets to access lists 
        self.button_list.append(self.backBut)
        self.button_list.append(self.nextBut)

        self.add_to_text_dict("Single Player Title", title, title_rect)

    def get_event(self, event):
        """Looks for pygame events"""
        # Quitting
        if event.type == pg.QUIT:
            self.quit = True

        # Handle Normal Buttons
        for button in self.button_list:
                button.check_event(event)

    def add_to_text_dict(self, name, rendered_text, text_rect, type = "normal"):
        self.text_dict[name] ={"rendered_text": rendered_text,
                                "text_rect": text_rect,
                                "type": type}

    def return_home(self):
        self.change_state("SPLASH")

    def change_state(self, state, **kwargs):
        self.next_state = state
        self.done = True
    
    def draw(self, surface):
        """Draws the Add Friend screen - Widgets/Text/etc..."""
        # Background
        surface.fill(pg.Color(G.BG_COLOR))

        # Text
        for text in self.text_dict:
            if self.text_dict[text]["type"] == "normal":
                surface.blit(self.text_dict[text]["rendered_text"], 
                            self.text_dict[text]["text_rect"])
            
        # Draw Buttons
        for button in self.button_list:
            button.update(surface)
