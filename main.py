#!/usr/bin/env python3
import sys
import os
directory = os.path.dirname(__file__)
if directory:
    os.chdir(directory)
from scripts.game_structure.text import verdana
from scripts.game_structure.buttons import buttons
from scripts.game_structure.load_cat import *
from scripts.cat.sprites import sprites
#from scripts.world import load_map
from scripts.clan import clan_class
import pygame_gui

# import all screens for initialization
from scripts.screens.all_screens import *

# P Y G A M E
clock = pygame.time.Clock()
pygame.display.set_icon(pygame.image.load('resources/images/icon.png'))

# LOAD cats & clan
if not os.path.exists('saves/clanlist.txt'):
    os.makedirs('saves', exist_ok=True)
    with open('saves/clanlist.txt', 'w') as write_file:
        write_file.write('')
with open('saves/clanlist.txt', 'r') as read_file:
    clan_list = read_file.read()
    if_clans = len(clan_list.strip())
if if_clans > 0:
    game.switches['clan_list'] = clan_list.split('\n')
    try:
        load_cats()
        clan_class.load_clan()
    except Exception as e:
        print("\nERROR MESSAGE:\n",e,"\n")
        if not game.switches['error_message']:
            game.switches[
                'error_message'] = 'There was an error loading the cats file!'
"""
    try:
        game.map_info = load_map('saves/' + game.clan.name)
    except NameError:
        game.map_info = {}
    except:
        game.map_info = load_map("Fallback")
        print("Default map loaded.")
        """

# LOAD settings
if not os.path.exists('saves/settings.txt'):
    with open('saves/settings.txt', 'w') as write_file:
        write_file.write('')
game.load_settings()

# reset brightness to allow for dark mode to not look crap
verdana.change_text_brightness()
buttons.change_button_brightness()
sprites.load_scars()

# initialize pygame gui 
manager = pygame_gui.UIManager((800, 700), 'resources/theme.json')
start_screen.screen_switches()
while True:
    time_delta = clock.tick(30) / 1000.0
    if game.switches['cur_screen'] not in ['start screen']:
        if game.settings['dark mode']:
            screen.fill((57, 50, 36))
        else:
            screen.fill((206, 194, 168))

    if game.settings_changed:
        verdana.change_text_brightness()
        buttons.change_button_brightness()

    mouse.check_pos()

    # EVENTS
    for event in pygame.event.get():
        game.all_screens[game.current_screen].handle_event(event)
        

        if event.type == pygame.QUIT:
            # close pygame
            pygame.display.quit()
            pygame.quit()
            sys.exit()

        # MOUSE CLICK
        if event.type == pygame.MOUSEBUTTONDOWN:
            game.clicked = True

        '''if event.type == pygame.KEYDOWN:
            game.keyspressed = []
            keys = pygame.key.get_pressed()
            if keys[pygame.K_0]:
                game.keyspressed.append(0)
            if keys[pygame.K_1]:
                game.keyspressed.append(1)
            if keys[pygame.K_2]:
                game.keyspressed.append(2)
            if keys[pygame.K_3]:
                game.keyspressed.append(3)
            if keys[pygame.K_4]:
                game.keyspressed.append(4)
            if keys[pygame.K_5]:
                game.keyspressed.append(5)
            if keys[pygame.K_6]:
                game.keyspressed.append(6)
            if keys[pygame.K_7]:
                game.keyspressed.append(7)
            if keys[pygame.K_8]:
                game.keyspressed.append(8)
            if keys[pygame.K_9]:
                game.keyspressed.append(9)
            if keys[pygame.K_KP0]:
                game.keyspressed.append(10)
            if keys[pygame.K_KP1]:
                game.keyspressed.append(11)
            if keys[pygame.K_KP2]:
                game.keyspressed.append(12)
            if keys[pygame.K_KP3]:
                game.keyspressed.append(13)
            if keys[pygame.K_KP4]:
                game.keyspressed.append(14)
            if keys[pygame.K_KP5]:
                game.keyspressed.append(15)
            if keys[pygame.K_KP6]:
                game.keyspressed.append(16)
            if keys[pygame.K_KP7]:
                game.keyspressed.append(17)
            if keys[pygame.K_KP8]:
                game.keyspressed.append(18)
            if keys[pygame.K_KP9]:
                game.keyspressed.append(19)
            if keys[pygame.K_UP]:
                game.keyspressed.append(20)
            if keys[pygame.K_RIGHT]:
                game.keyspressed.append(21)
            if keys[pygame.K_DOWN]:
                game.keyspressed.append(22)
            if keys[pygame.K_LEFT]:
                game.keyspressed.append(23)'''
        manager.process_events(event)

    manager.update(time_delta)

    # SCREENS
    game.all_screens[game.current_screen].on_use()

    # update
    game.update_game()
    if game.switch_screens:
        game.all_screens[game.current_screen].screen_switches()
        game.switch_screens = False
    # END FRAME
    manager.draw_ui(screen)

    pygame.display.update()
