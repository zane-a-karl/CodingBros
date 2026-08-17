#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: singleplay.py
Description: This is single player screen used for setup before playing against the cpu

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

class SelectSinglePlayOptions(GameState):
    """
    As names a class that defines the attributes of the Splash Screen State
    """
    def __init__(self):
        super(SelectSinglePlayOptions, self).__init__()

        # Setup
        self.persist["screen_color"] = "G.BLACK"
        self.show_bad_inputs_popup = False
        self.next_state = "NONE"
        self.cpu_level_selection = None
        self.token_type_selection = None
        self.error_text = ""
        self.button_list = []
        self.popup_button_list = []
        self.checkboxes_list = []
        self.text_dict = {}
        self.surfaces_list = {}
        self.persist["user_token_type"] = self.token_type_selection

        # Title
        title_font = pg.font.Font(G.EIGHT_BIT_FONT_PATH, 72)
        title = title_font.render("SETUP", True, G.WHITE)
        title_rect = title.get_rect()
        title_rect.center = (self.screen_rect.centerx, self.screen_rect.top + 50)

        # Label Setup
        label_font = pg.font.Font(G.EIGHT_BIT_FONT_PATH, 42)
        label_x_offset = 50
        cb_x_label_offset = label_x_offset + 200
        cpu_label_y = 125
        cpu_cb_label_y = cpu_label_y + 50
        token_label_y = 325
        token_cb_label_y = token_label_y + 50

        # Labels
        cpu_level = label_font.render("CPU Level:", True, G.WHITE)
        cpu_level_rect = cpu_level.get_rect()
        cpu_level_rect.topleft = (label_x_offset, cpu_label_y)

        token_type = label_font.render("Token Type:", True, G.WHITE)
        token_type_rect = token_type.get_rect()
        token_type_rect.topleft = (label_x_offset, token_label_y)
        
        # CPU Level
        cpu_boxes = []

        self.easy_cb = Checkbox(
            self.screen_rect, 
            cb_x_label_offset, cpu_cb_label_y, 0, 
            type = "cpu_level",
            caption='Easy',
            font = pg.font.Font(G.EIGHT_BIT_FONT_PATH, 42),
            font_color = G.WHITE)
        
        self.medium_cb = Checkbox(
            self.screen_rect, 
            cb_x_label_offset, cpu_cb_label_y + 50, 1,
            type = "cpu_level",
            caption='Medium',
            font = pg.font.Font(G.EIGHT_BIT_FONT_PATH, 42),
            font_color = G.WHITE)
        
        self.hard_cb = Checkbox(
            self.screen_rect,
            cb_x_label_offset, cpu_cb_label_y + 100, 2,
            type = "cpu_level",
            caption='Hard',
            font = pg.font.Font(G.EIGHT_BIT_FONT_PATH, 42),
            font_color = G.WHITE)
        
        cpu_boxes.append(self.easy_cb)
        cpu_boxes.append(self.medium_cb)
        cpu_boxes.append(self.hard_cb)

        # Token Selection
        token_boxes = []
        
        self.x_cb = Checkbox(
            self.screen_rect, 
            cb_x_label_offset, token_cb_label_y, 0,
            type = "token_selection",
            caption="X's",
            font = pg.font.Font(G.EIGHT_BIT_FONT_PATH, 42),
            font_color = G.WHITE)
        
        self.o_cb = Checkbox(
            self.screen_rect,
            cb_x_label_offset, token_cb_label_y + 50, 1,
            type = "token_selection",
            caption="O's",
            font = pg.font.Font(G.EIGHT_BIT_FONT_PATH, 42),
            font_color = G.WHITE)
        
        token_boxes.append(self.x_cb)
        token_boxes.append(self.o_cb)

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
                             self.verifyUserInputs,
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
        self.checkboxes_list.append(cpu_boxes)
        self.checkboxes_list.append(token_boxes)

        self.add_to_text_dict("Single Player Title", title, title_rect)
        self.add_to_text_dict("CPU Level", cpu_level, cpu_level_rect)
        self.add_to_text_dict("Token Type", token_type, token_type_rect)
        
    def add_to_text_dict(self, name, rendered_text, text_rect, type = "normal"):
        self.text_dict[name] ={"rendered_text": rendered_text,
                               "text_rect": text_rect,
                               "type": type}

    def render_wrapped_text(self, text, font, color, max_width):
        """return a list of (surface, rect) for each wwrapped line."""
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            # Try to add the next word
            test_line = current_line + word + " "
            test_surface = font.render(test_line, True, color)

            if test_surface.get_width() <= max_width:
                current_line = test_line
            else:
                # commit the current line and start a new one
                lines.append(current_line.strip())
                current_line = word + " "

        if current_line:
            lines.append(current_line.strip())

        # Render each line into a surface
        surfaces = []
        for i, line in enumerate(lines):
            surf = font.render(line, True, color)
            rect = surf.get_rect()
            surfaces.append((surf, rect))
        
        return surfaces
    
    def close_popup(self):
        self.popup_button_list.remove(self.closePopupButton)
        self.show_bad_inputs_popup = False

    def render_popup(self):
        # Layout vars
        button_width = 250
        button_height = 50
        border = 40 

        # Fonts - Need to store globally this is stupid
        title_font = pg.font.Font(G.EIGHT_BIT_FONT_PATH, 50)
        font = pg.font.Font(G.EIGHT_BIT_FONT_PATH, 42)

        # Screen
        self.popup_size = (self.screen_rect.width - border,
                           self.screen_rect.height - border)
        self.popup = pg.Surface(self.popup_size, pg.SRCALPHA)  # allow transparency
        self.popup_rect = self.popup.get_rect(center=(300, 200))
        self.popup_rect.center = (self.screen_rect.centerx, self.screen_rect.centery)

        # Dimmed background overlay
        self.overlay = pg.Surface(self.screen_rect.size, pg.SRCALPHA)
        # overlay.fill((0, 0, 0, 150))  # G.BLACK w/ 150 alpha
        # surface.blit(overlay, (0, 0))

        # Clear popup
        # popup.fill((230, 230, 230, 240))  # light gray w/ some transparency

        # Draw border
        # pg.draw.rect(popup, G.BLACK, popup.get_rect(), 3)

        # Title
        self.title_text = title_font.render("Input Error", True, (0, 0, 0))
        self.title_text_rect = self.title_text.get_rect(center = (self.popup_rect.centerx, 
                                                        self.popup_rect.top + border))
        # popup.blit(title_text, title_text_rect)

        # Image
        error_image = pg.image.load("images/error_image.png").convert_alpha()
        scale = 0.5
        self.error_image_scaled = pg.transform.scale(error_image, 
                                                (int(error_image.get_width() * scale), 
                                                 int(error_image.get_height() * scale)))
        self.error_image_rect = self.error_image_scaled.get_rect(center = (self.popup_rect.centerx, 
                                                                 self.popup_rect.centery - self.error_image_scaled.get_height()/2))
        # popup.blit(error_image_scaled, error_image_rect)

        # Text
        self.wrapped_message_text = self.render_wrapped_text(self.error_text,
                                                        font,
                                                        G.BLACK,
                                                        self.popup_rect.width - 40)
        # y = popup_rect.centery
        # for surf, rect in wrapped_message_text:
        #     rect.topleft = (popup_rect.left + 20, y)
        #     popup.blit(surf, rect)
        #     y += rect.height + 5

        # Button
        BUTTON_STYLE = {"hover_font_color" : G.ORANGE,
                        "font" : pg.font.Font(G.EIGHT_BIT_FONT_PATH, 42),
                        "font_color": G.WHITE,
                        "hover_font_color": G.BLACK,
                        "hover_color": G.GREEN,
                        "hover_sound" : pg.mixer.Sound(G.BLIP_SHORT_SOUND_PATH)}
        self.closePopupButton = Button((self.popup_rect.centerx - button_width/2, 
                                        self.popup_rect.bottom - button_height - 40, 
                                        button_width, 
                                        button_height),
                                        G.ORANGE,
                                        self.close_popup,
                                        text="Close",
                                        **BUTTON_STYLE)
        self.popup_button_list.append(self.closePopupButton)
        # self.closePopupButton.update(popup)

        # surface.blit(popup, popup_rect)

        return None
    
    def draw_popup(self, surface):
        # Overlay
        surface.blit(self.overlay, (0, 0))

        # Clear popup
        self.popup.fill((230, 230, 230, 240))  # light gray w/ some transparency

        # Draw border
        pg.draw.rect(self.popup, G.BLACK, self.popup.get_rect(), 3)
        self.popup.blit(self.title_text, self.title_text_rect)

        # Image
        
        self.popup.blit(self.error_image_scaled, self.error_image_rect)

        y = self.popup_rect.centery
        for surf, rect in self.wrapped_message_text:
            rect.topleft = (self.popup_rect.left + 20, y)
            self.popup.blit(surf, rect)
            y += rect.height + 5

        # Button
        #self.closePopupButton.update(self.popup)

        surface.blit(self.popup, self.popup_rect)

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True

        # Handle Normal Buttons accordingly
        if(self.show_bad_inputs_popup):
            for button in self.popup_button_list:
                button.check_event(event)
        else:
            for button in self.button_list:
                button.check_event(event)

            # Handle/Toggle Checkboxes accordingly
            for current_list in self.checkboxes_list:
                nothing_checked = True
                for current_button in current_list:
                    current_button.check_event(event)
                    if (current_button.checked):
                        nothing_checked = False
                        if(current_button.type == "cpu_level"):
                            self.cpu_level_selection = current_button.caption
                        elif(current_button.type == "token_selection"):
                            self.token_type_selection = current_button.caption
                        for button in current_list:
                            if button != current_button:
                                button.checked = False
                if nothing_checked:
                    if(current_button.type == "cpu_level"):
                        self.cpu_level_selection = None
                    elif(current_button.type == "token_selection"):
                        self.token_type_selection = None

    def reset_initial_values(self, screen):
        self.bad_inputs_popup = False
        self.next_state = "NONE"
        self.cpu_level_selection = None
        self.token_type_selection = None
        self.error_text = ""

        for current_list in self.checkboxes_list:
            for current_button in current_list:
                current_button.reset_to_default(screen)

    def return_home(self):
        self.change_state("SPLASH")
        pass

    def change_color(self, box, cb_list):
        if box.checked is True:
            for b in cb_list:
                if b != box:
                    b.checked = False

    def draw(self, surface):
        # Background
        surface.fill(pg.Color(G.BG_COLOR))

        # Draw Popup
        if(self.show_bad_inputs_popup):
            self.draw_popup(surface)
            for button in self.popup_button_list:
                button.update(surface)
        else:
            # Text
            for text in self.text_dict:
                if self.text_dict[text]["type"] == "normal":
                    surface.blit(self.text_dict[text]["rendered_text"], 
                                self.text_dict[text]["text_rect"])
                
            # Draw Buttons
            for button in self.button_list:
                button.update(surface)

            # Draw Checkboxes
            for current_list in self.checkboxes_list:
                for button in current_list:
                    button.update(surface)
              
    def verifyUserInputs(self):
        GAME_STYLE = {"cpu_level" : self.cpu_level_selection,
                      "user_token" : self.token_type_selection,
                      "cpu_token": G.WHITE}
        
        error_found = False
        
        # Verify user input
        if self.cpu_level_selection == None:
            error_found = True
            self.error_text = "You haven't selected a CPU level! Please close and select."
        elif self.token_type_selection == None:
            error_found = True
            self.error_text = "You haven't select a token type! Please close and select."
        
        if error_found:
            self.render_popup()
            self.show_bad_inputs_popup = True
            return
        
        self.persist["user_token_type"] = self.token_type_selection
        self.change_state("GAMEPLAY", **GAME_STYLE)

    def change_state(self, state, **kwargs):
        self.next_state = state
        self.done = True
