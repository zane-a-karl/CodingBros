#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: checkbox.py
Description: This is the file containing the code for custom checkboxes used on different setup screens

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


# Pygame initialization
pg.font.init()

class Checkbox:
    def __init__(self, surface, x, y, idnum, type, color=(230, 230, 230),
        caption="", outline_color=(0, 0, 0), check_color=(255,180,0),
        font_color=(0, 0, 0), text_offset=(35, 1), font=pg.font.Font(None,16)):
        self.surface = surface
        self.x = x
        self.y = y
        self.color = color
        self.caption = caption
        self.oc = outline_color
        self.cc = check_color
        self.fc = font_color
        self.to = text_offset
        self.ft = font
        self.type = type

        #identification for removal and reorginazation
        self.idnum = idnum

        # checkbox object
        self.checkbox_obj = pg.Rect(self.x, self.y, 25, 25)
        self.inner_checkbox_obj = pg.Rect(self.x + 5, self.y + 5, 15, 15)
        self.checkbox_outline = self.checkbox_obj.copy()

        # variables to test the different states of the checkbox
        self.checked = False

    def _draw_button_text(self, surface):
        self.font = self.ft
        self.font_surf = self.font.render(self.caption, True, self.fc)
        w, h = self.font.size(self.caption)
        self.font_pos = (self.x + self.to[0], 
                         self.y + 25 / 2 - h / 2 + self.to[1])
        surface.blit(self.font_surf, self.font_pos)

    def render_checkbox(self, surface):
        if self.checked:
            pg.draw.rect(surface, self.color, self.checkbox_obj)
            pg.draw.rect(surface, self.oc, self.checkbox_outline, 1)
            pg.draw.rect(surface, self.cc, self.inner_checkbox_obj)
        elif not self.checked:
            pg.draw.rect(surface, self.color, self.checkbox_obj)
            pg.draw.rect(surface, self.oc, self.checkbox_outline, 1)
        self._draw_button_text(surface)

    def _update(self, event):
        x, y = pg.mouse.get_pos()
        px, py, w, h = self.checkbox_obj
        if px < x < px + w and py < y < py + w:
            if self.checked:
                self.checked = False
            else:
                self.checked = True

    def update(self, surface):
        self.render_checkbox(surface)

    def on_click(self, event):
        self._update(event)

    def check_event(self, event):
        """The button needs to be passed events from your program event loop."""
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)

    def reset_to_default(self, surface):
        self.checked = False
        self.update(surface)
