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
from button.checkbox import Checkbox

## GLOBALS ##
WIDTH = 600
BLACK = (0,0,0)
WHITE = (255,255,255)
ORANGE = (255,180,0)
GREEN = (106,168,79)
BG_COLOR = (67,67,67)
EIGHT_BIT_FONT_PATH = "font/Eight-Bit Madness.ttf"
BLIP_SHORT_SOUND_PATH = "sounds/blipshort1.wav"

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

class GameState(object):
    """
    Parent class for individual game states to inherit from. 
    """
    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pg.display.get_surface().get_rect()
        self.persist = {}
        self.font = pg.font.Font(None, 24)

    def startup(self, persistent):
        """
        Called when a state resumes being active.
        Allows information to be passed between states.
        
        persistent: A dict passed from state to state
        """
        self.persist = persistent        
        
    def get_event(self, event):
        """
        Handle a single event passed by the Game object.
        """
        pass
        
    def update(self, dt):
        """
        Update the state. Called by the Game object once
        per frame. 
        
        dt: time since last frame
        """
        pass
        
    def draw(self, surface):
        """
        Draw everything to the screen.
        """
        pass

class SplashScreen(GameState):
    """
    As names a class that defines the attributes of the Splash Screen State
    """
    def __init__(self):
        super(SplashScreen, self).__init__()

        # Title
        title_font = pg.font.Font(EIGHT_BIT_FONT_PATH, 72)
        self.title = title_font.render("TIC - TAC - TOE", True, WHITE)
        self.title_rect = self.title.get_rect()
        self.title_rect.center = (self.screen_rect.centerx, self.screen_rect.top + 50)
        splashScreenImage = pg.image.load('images/splashScreenCenter.png').convert_alpha()
        self.splashScreenImage = CustomGameImage(300 - (splashScreenImage.get_width() * .5)/2, 
                                                 self.screen_rect.top + 125, 
                                                 splashScreenImage, 
                                                 0.5)
        
        # Setup
        self.persist["screen_color"] = "black"
        self.next_state = "NONE"

        # Buttons/Labels
        BUTTON_STYLE = {"hover_font_color" : ORANGE,
                        "font" : pg.font.Font(EIGHT_BIT_FONT_PATH, 42),
                        "font_color": WHITE,
                        "hover_font_color": BLACK,
                        "hover_color": GREEN,
                        "hover_sound" : pg.mixer.Sound(BLIP_SHORT_SOUND_PATH)}
        
        self.singlePlayerBut = Button((0,0,350,35),
                            ORANGE, 
                            self.select_single_play_options,
                            text="SINGLE PLAYER", 
                            **BUTTON_STYLE)
        
        self.addPlayerBut = Button((0,0,350,35),
                             ORANGE, 
                             self.change_color,
                             text="ADD FRIEND", 
                             **BUTTON_STYLE)
        
        self.onlinePlayBut = Button((0,0,350,35),
                             ORANGE, 
                             self.change_color,
                             text="ONLINE PLAY", 
                             **BUTTON_STYLE)
        
        self.exitBut = Button((0,0,350,35),
                             ORANGE,
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
        surface.fill(pg.Color(BG_COLOR))
        surface.blit(self.title, self.title_rect)
        self.splashScreenImage.draw(surface)
        for button in self.button_list:
            button.update(surface)

    def change_state(self, state):
        self.next_state = state
        self.done = True

class SelectSinglePlayOptions(GameState):
    """
    As names a class that defines the attributes of the Splash Screen State
    """
    def __init__(self):
        super(SelectSinglePlayOptions, self).__init__()

        # Setup
        self.persist["screen_color"] = "black"
        self.show_bad_inputs_popup = False
        self.next_state = "NONE"
        self.cpu_level_selection = None
        self.token_type_selection = None
        self.error_text = ""
        self.button_list = []
        self.checkboxes_list = []
        self.text_dict = {}
        self.surfaces_list = {}

        # Title
        title_font = pg.font.Font(EIGHT_BIT_FONT_PATH, 72)
        title = title_font.render("SETUP", True, WHITE)
        title_rect = title.get_rect()
        title_rect.center = (self.screen_rect.centerx, self.screen_rect.top + 50)

        # Label Setup
        label_font = pg.font.Font(EIGHT_BIT_FONT_PATH, 42)
        label_x_offset = 50
        cb_x_label_offset = label_x_offset + 200
        cpu_label_y = 125
        cpu_cb_label_y = cpu_label_y + 50
        token_label_y = 325
        token_cb_label_y = token_label_y + 50

        # Labels
        cpu_level = label_font.render("CPU Level:", True, WHITE)
        cpu_level_rect = cpu_level.get_rect()
        cpu_level_rect.topleft = (label_x_offset, cpu_label_y)

        token_type = label_font.render("Token Type:", True, WHITE)
        token_type_rect = token_type.get_rect()
        token_type_rect.topleft = (label_x_offset, token_label_y)
        
        # CPU Level
        cpu_boxes = []

        self.easy_cb = Checkbox(
            self.screen_rect, 
            cb_x_label_offset, cpu_cb_label_y, 0, 
            type = "cpu_level",
            caption='Easy',
            font = pg.font.Font(EIGHT_BIT_FONT_PATH, 42),
            font_color = WHITE)
        
        self.medium_cb = Checkbox(
            self.screen_rect, 
            cb_x_label_offset, cpu_cb_label_y + 50, 1,
            type = "cpu_level",
            caption='Medium',
            font = pg.font.Font(EIGHT_BIT_FONT_PATH, 42),
            font_color = WHITE)
        
        self.hard_cb = Checkbox(
            self.screen_rect,
            cb_x_label_offset, cpu_cb_label_y + 100, 2,
            type = "cpu_level",
            caption='Hard',
            font = pg.font.Font(EIGHT_BIT_FONT_PATH, 42),
            font_color = WHITE)
        
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
            font = pg.font.Font(EIGHT_BIT_FONT_PATH, 42),
            font_color = WHITE)
        
        self.o_cb = Checkbox(
            self.screen_rect,
            cb_x_label_offset, token_cb_label_y + 50, 1,
            type = "token_selection",
            caption="O's",
            font = pg.font.Font(EIGHT_BIT_FONT_PATH, 42),
            font_color = WHITE)
        
        token_boxes.append(self.x_cb)
        token_boxes.append(self.o_cb)

        # Buttons
        button_gap = 300
        BUTTON_STYLE = {"hover_font_color" : ORANGE,
                        "font" : pg.font.Font(EIGHT_BIT_FONT_PATH, 42),
                        "font_color": WHITE,
                        "hover_font_color": BLACK,
                        "hover_color": GREEN,
                        "hover_sound" : pg.mixer.Sound(BLIP_SHORT_SOUND_PATH)}
        
        self.nextBut = Button((0,0,225,35),
                             ORANGE, 
                             self.verifyUserInputs,
                             text="NEXT", 
                             **BUTTON_STYLE)
        
        self.backBut = Button((0,0,225,35),
                             ORANGE,
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
        self.bad_inputs_popup = False

    def draw_popup(self, surface):

    def render_popup(self, surface):
        # Layout vars
        button_width = 250
        button_height = 50
        border = 40 

        # Fonts - Need to store globally this is stupid
        title_font = pg.font.Font(EIGHT_BIT_FONT_PATH, 50)
        font = pg.font.Font(EIGHT_BIT_FONT_PATH, 42)

        # Screen
        popup_size = (surface.get_rect().width - border, 
                      surface.get_rect().height - border)
        popup = pg.Surface(popup_size, pg.SRCALPHA)  # allow transparency
        popup_rect = popup.get_rect(center=(300, 200))
        popup_rect.center = (surface.get_rect().centerx, surface.get_rect().centery)

        # Dimmed background overlay
        overlay = pg.Surface(surface.get_size(), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # black w/ 150 alpha
        surface.blit(overlay, (0, 0))

        # Clear popup
        popup.fill((230, 230, 230, 240))  # light gray w/ some transparency

        # Draw border
        pg.draw.rect(popup, BLACK, popup.get_rect(), 3)

        # Title
        title_text = title_font.render("Input Error", True, (0, 0, 0))
        title_text_rect = title_text.get_rect(center = (popup_rect.centerx, 
                                                        popup_rect.top + border))
        popup.blit(title_text, title_text_rect)

        # Image
        error_image = pg.image.load("images/error_image.png").convert_alpha()
        scale = 0.5
        error_image_scaled = pg.transform.scale(error_image, 
                                                (int(error_image.get_width() * scale), 
                                                 int(error_image.get_height() * scale)))
        error_image_rect = error_image_scaled.get_rect(center = (popup_rect.centerx, 
                                                                 popup_rect.centery - error_image_scaled.get_height()/2))
        popup.blit(error_image_scaled, error_image_rect)

        # Text
        wrapped_message_text = self.render_wrapped_text(self.error_text,
                                                        font,
                                                        BLACK,
                                                        popup_rect.width - 40)
        y = popup_rect.centery
        for surf, rect in wrapped_message_text:
            rect.topleft = (popup_rect.left + 20, y)
            popup.blit(surf, rect)
            y += rect.height + 5

        # Button
        BUTTON_STYLE = {"hover_font_color" : ORANGE,
                        "font" : pg.font.Font(EIGHT_BIT_FONT_PATH, 42),
                        "font_color": WHITE,
                        "hover_font_color": BLACK,
                        "hover_color": GREEN,
                        "hover_sound" : pg.mixer.Sound(BLIP_SHORT_SOUND_PATH)}
        self.closePopupButton = Button((popup_rect.centerx - button_width/2, 
                                        popup_rect.bottom - button_height - 20, 
                                        button_width, 
                                        button_height),
                                        ORANGE,
                                        self.close_popup,
                                        text="Close",
                                        **BUTTON_STYLE)
        #self.closePopupButton.update(popup)

        return None

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True

        # Handle Normal Buttons accordingly
        for button in self.button_list:
            button.check_event(event)

        # Handle/Toggle Checkboxes accordingly
        for current_list in self.checkboxes_list:
            for current_button in current_list:
                current_button.check_event(event)
                if (current_button.checked):
                    if(current_button.type == "cpu_level"):
                        self.cpu_level_selection = current_button.caption
                    if(current_button.type == "token_selection"):
                        self.token_type_selection = current_button.caption
                    for button in current_list:
                        if button != current_button:
                            button.checked = False

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
        surface.fill(pg.Color(BG_COLOR))

        # Draw Popup
        if(self.show_bad_inputs_popup):
            self.draw_popup(surface)

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
                
    def verifyUserInputs (self):
        GAME_STYLE = {"cpu_level" : self.cpu_level_selection,
                      "user_token" : self.token_type_selection,
                      "cpu_token": WHITE}
        
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
        
        self.change_state("GAMEPLAY", **GAME_STYLE)

    def change_state(self, state, **kwargs):
        self.next_state = state
        self.done = True

class AddFriend(GameState):
    """
    As names a class that defines the attributes of the Add Friend Screen State
    """
    def __init__(self):
        super(AddFriend, self).__init__()
        self.title = self.font.render("ADDFREIND", True, pg.Color("dodgerblue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.persist["screen_color"] = "black"
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
        surface.fill(pg.Color(BG_COLOR))

class Gameplay(GameState):
    def __init__(self):
        super(Gameplay, self).__init__()
        self.popup = None
        self.show_popup = False

        # self.rect = pg.Rect((0, 0), (128, 128))
        # self.x_velocity = 1
        
    def startup(self, persistent):
        self.screen_color = pg.Color(BG_COLOR)
        
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
        surface.fill(BG_COLOR)
        
        # Draw the Tic Tac Toe Board
        self.draw_board(surface)

        # rect = pg.Rect(100, 100, 300, 200)  # Position and size (x, y, width, height)
        # pg.draw.rect(surface, BLACK, rect, border_radius=20)  # Set border_radius to round corners
        
    def draw_board(self,surface):
        lt = 12 # Line Thickness
        sw = 150 # Square Width
        x_start = self.screen_rect.centerx - sw - (sw/2)
        x_end = self.screen_rect.centerx + sw + (sw/2)
        y_start = self.screen_rect.centery - sw - (sw/2)
        y_end = self.screen_rect.centery + sw + (sw/2)
        
        # Vertical
        pg.draw.line(surface, BLACK, (x_start + sw, y_start), (x_start + sw, y_end), lt)
        pg.draw.line(surface, BLACK, (x_end - sw, y_start), (x_end - sw, y_end), lt)

        # Horizontal
        pg.draw.line(surface, BLACK, (x_start, y_start + sw), (x_end, y_start + sw), lt)
        pg.draw.line(surface, BLACK, (x_start, y_end - sw), (x_end, y_end - sw), lt)

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

class OldButton():
    """
    Generic Button class that can be used to create a button out of a image/shape
    """
    def __init__(self, x, y, image, image_hover, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pg.transform.scale(image, (int(width * scale), int(height * scale)))
        self.image_hover = pg.transform.scale(image_hover, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        self.current_image = self.image
    
    def draw(self, screen):
        # Default action state
        action = False
        
        # Get the mouse position
        pos = pg.mouse.get_pos()

        # Check Mouse Over and click
        if(self.rect.collidepoint(pos)):
            self.current_image = self.image_hover
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False: # Left Click
                self.clicked = True
                action = True

        # Reset Click
        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw the button on the screen
        screen.blit(self.current_image, (self.rect.x, self.rect.y))

        return action

def main():
    # Initial Pygame Screen/Window Setup
    pg.init()
    pg.display.set_caption("Coding Bros Tic Tac Toe")
    screen = pg.display.set_mode((WIDTH, WIDTH))

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
