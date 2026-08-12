#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: image.py
Description: This is custom game image class used for importing and positioning images on different screens

Author: Coding Bros
Email: See team info <project_root>/misc/teamInfo.txt
Date Created: 2024-10-13
Last Modified: 2024-10-31
Version: 1.0
"""

# ===============
# Start Imports
# ===============
import pygame as pg

# ===============
# End Imports
# ===============

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
