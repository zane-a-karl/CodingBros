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
from gamestate import GameState
from image import CustomGameImage
from globals import TicTacToeGlobals as G
from image import CustomGameImage

class SplashScreen(GameState):
    """
    As names a class that defines the attributes of the Splash Screen State
    """
    def __init__(self):
        super(SplashScreen, self).__init__()

        # Title
        title_font = pg.font.Font(G.EIGHT_BIT_FONT_PATH, 72)
        self.title = title_font.render("TIC - TAC - TOE", True, G.WHITE)
        self.title_rect = self.title.get_rect()
        self.title_rect.center = (self.screen_rect.centerx, self.screen_rect.top + 50)
        splashScreenImage = pg.image.load('images/splashScreenCenter.png').convert_alpha()
        self.splashScreenImage = CustomGameImage(300 - (splashScreenImage.get_width() * .5)/2, 
                                                 self.screen_rect.top + 125, 
                                                 splashScreenImage, 
                                                 0.5)
        
        # Setup
        self.persist["screen_color"] = "G.BLACK"
        self.next_state = "NONE"

        # Buttons/Labels
        BUTTON_STYLE = {"hover_font_color" : G.ORANGE,
                        "font" : pg.font.Font(G.EIGHT_BIT_FONT_PATH, 42),
                        "font_color": G.WHITE,
                        "hover_font_color": G.BLACK,
                        "hover_color": G.GREEN,
                        "hover_sound" : pg.mixer.Sound(G.BLIP_SHORT_SOUND_PATH)}
        
        self.singlePlayerBut = Button((0,0,350,35),
                            G.ORANGE, 
                            self.select_single_play_options,
                            text="SINGLE PLAYER", 
                            **BUTTON_STYLE)
        
        self.addPlayerBut = Button((0,0,350,35),
                             G.ORANGE, 
                             lambda: self.change_state("ADDFRIEND"),
                             text="ADD FRIEND", 
                             **BUTTON_STYLE)
        
        self.onlinePlayBut = Button((0,0,350,35),
                             G.ORANGE, 
                             self.change_color,
                             text="ONLINE PLAY", 
                             **BUTTON_STYLE)
        
        self.exitBut = Button((0,0,350,35),
                             G.ORANGE,
                             self.exit,
                             text="EXIT", 
                             **BUTTON_STYLE)
         
        self.singlePlayerBut.rect.center = (self.screen_rect.centerx, self.screen_rect.bottom - 250)
        self.addPlayerBut.rect.center = (self.screen_rect.centerx, self.screen_rect.bottom - 200)
        self.onlinePlayBut.rect.center = (self.screen_rect.centerx, self.screen_rect.bottom - 150)
        self.exitBut.rect.center = (self.screen_rect.centerx, self.screen_rect.bottom - 100)
        self.button_list = [self.singlePlayerBut, self.addPlayerBut, self.onlinePlayBut, self.exitBut]

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        for button in self.button_list:
            button.check_event(event)
    
    def exit(self):
        self.quit = True

    def select_single_play_options(self):
        self.change_state("SINGLE_GAMEPLAY_OPTIONS")

    def change_color(self):
        pass
        
    def draw(self, surface):
        # Background
        surface.fill(pg.Color(G.BG_COLOR))
        surface.blit(self.title, self.title_rect)
        self.splashScreenImage.draw(surface)
        for button in self.button_list:
            button.update(surface)

    def change_state(self, state):
        self.next_state = state
        self.done = True
