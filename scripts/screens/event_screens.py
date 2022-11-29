from random import choice
import pygame_gui

from .base_screens import Screens, draw_menu_buttons, cat_profiles, draw_clan_name

from scripts.events import events_class
from scripts.patrol import patrol
from scripts.utility import draw
from scripts.game_structure.buttons import buttons
from scripts.game_structure.text import *
from scripts.game_structure.image_button import UIImageButton

class SingleEventScreen(Screens):

    def on_use(self):
        # LAYOUT
        if game.switches['event'] is not None:
            events_class.all_events[game.switches['event']].page()

        # buttons
        buttons.draw_button(('center', -150),
                            text='Continue',
                            cur_screen='events screen')

    def screen_switches(self):
        pass

class EventsScreen(Screens):
    event_display_type = "clan events"
    clan_events = ""
    relation_events = ""
    display_text = "<center> Check this page to see which events are currently happening at the Clan.</center>"
    display_events = ""

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.timeskip_button:
                events_class.one_moon()
                if game.cur_events_list is not None and game.cur_events_list != []:
                    for i in range(len(game.cur_events_list)):
                        if not isinstance(game.cur_events_list[i], str):
                            game.cur_events_list.remove(game.cur_events_list[i])
                            break        
                    self.clan_events = "<font color='#000000'>" + '\n\n'.join(game.cur_events_list) + "</font>"
                else:
                    self.clan_events = "<font color='#000000'>Nothing significant happened this moon.</font>"


                if game.relation_events_list is not None and game.relation_events_list != []:
                    for i in range(len(game.relation_events_list)):
                        if not isinstance(game.relation_events_list[i], str):
                            game.game.relation_events_list(game.relation_events_list[i])
                            break        
                    self.relation_events = "<font color='#000000'>" + '\n'.join(game.relation_events_list) + "</font>"
                else:
                    self.relation_events = "<font color='#000000'>Nothing significant happened this moon.</font>"

                if self.event_display_type == "clan events":
                    self.display_events = self.clan_events
                elif self.event_display_type == "relationship events":
                    self.display_events = self.relation_events

                self.update_events_display()
        
            elif event.ui_element == self.toggle_borders_button:
                if game.clan.closed_borders == True:
                    game.clan.closed_borders = False
                    self.toggle_borders_button.set_text("Close Clan Borders")
                else:
                    game.clan.closed_borders = True
                    self.toggle_borders_button.set_text("Open Clan Borders")

            #Change the type of events displayed
            elif event.ui_element == self.relationship_events_button:
                self.event_display_type = "relationship events"
                self.clan_events_button.enable()
                self.relationship_events_button.disable()
                #Update Display
                self.display_events = self.relation_events
                self.update_events_display()
            elif event.ui_element == self.clan_events_button:
                self.event_display_type = "clan events"
                self.clan_events_button.disable()
                self.relationship_events_button.enable()
                #Update Display
                self.display_events = self.clan_events
                self.update_events_display()
            else:
                self.menu_button_pressed(event) 

    def screen_switches(self):
        cat_profiles() #Note - what does this do? 
        self.timeskip_button = UIImageButton(pygame.Rect((310, 205),(180, 30)), "", object_id = "#timeskip_button")
        if game.clan.closed_borders == True:
            self.toggle_borders_button = pygame_gui.elements.UIButton(pygame.Rect((500,210),(200, 30)), "Open Clan orders")
        else:
            self.toggle_borders_button = pygame_gui.elements.UIButton(pygame.Rect((500,210),(200, 30)), "Close Clan Borders")
        
        #Sets up the buttons to switch between the event types. 
        self.clan_events_button = UIImageButton(pygame.Rect((224, 245),(176, 30)), "", object_id = "#clan_events_button")
        self.relationship_events_button = UIImageButton(pygame.Rect((400, 245),(176, 30)), "", object_id = "#relationship_events_button")
        if self.event_display_type == "clan events":
            self.clan_events_button.disable() 
        elif self.event_display_type == "relationship events":
            self.relationship_events_button.disable() 

        self.events_list_box = pygame_gui.elements.UITextBox(self.display_events, pygame.Rect((100,290),(600,400)))

        #Display text
        #self.explain_text = pygame_gui.elements.UITextBox(self.display_text, pygame.Rect((25,110),(750,40)))

        #Draw and disable the correct menu buttons. 
        self.set_disabled_menu_buttons(["events_screen"])
        self.show_menu_buttons()

    def exit_screen(self):
        self.timeskip_button.kill()
        self.toggle_borders_button.kill()
        self.clan_events_button.kill()
        self.relationship_events_button.kill()
        self.events_list_box.kill()
        #self.hide_menu_buttons()

    def on_use(self):
        draw_clan_name()
        verdana.text(
            'Check this page to see which events are currently happening at the Clan.',
            ('center', 110))

        verdana.text(f'Current season: {str(game.clan.current_season)}',
                     ('center', 140))

        if game.clan.age == 1:
            verdana.text(f'Clan age: {str(game.clan.age)} moon',
                         ('center', 170))
        if game.clan.age != 1:
            verdana.text(f'Clan age: {str(game.clan.age)} moons',
                         ('center', 170))

        #What does this do? 
        if game.switches['events_left'] == 0:
            self.timeskip_button.enable()
        else:
            self.timeskip_button.disable()

    def update_events_display(self):
        self.events_list_box.kill()
        self.events_list_box = pygame_gui.elements.UITextBox(self.display_events, pygame.Rect((100,290),(600,400)))


class PatrolEventScreen(Screens):

    def handle_event(self, event):
        #random_options = []
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_9:
                for u in range(12):
                    i_max = len(game.patrol_cats)
                    if u < i_max:
                        game.switches['current_patrol'].append(
                            game.patrol_cats[u])

    event_bg = pygame.image.load("resources/images/patrol_event_frame.png").convert_alpha()
    info_bg = pygame.image.load("resources/images/patrol_info.png").convert_alpha()
    image_frame = pygame.image.load("resources/images/patrol_sprite_frame.png").convert_alpha()

    def get_list_text(self, patrol_list):
        if not patrol_list:
            return "None"
        # Removes duplicates.
        patrol_set = list(patrol_list)
        return ", ".join(patrol_set)

    def on_use(self):
        # USER INTERFACE
        draw_clan_name()
        screen.blit(PatrolEventScreen.event_bg, (381, 165))
        screen.blit(PatrolEventScreen.info_bg, (90, 456))
        screen.blit(PatrolEventScreen.image_frame, (65, 140))

        if game.switches['event'] == 0:
            patrol.add_patrol_cats()
            possible_events = patrol.get_possible_patrols(
                game.clan.current_season,
                game.clan.biome,
                game.clan.all_clans,
                game.settings.get('disasters')
            )
            patrol.patrol_event = choice(possible_events)

            if patrol.patrol_event.win_trait is not None:
                win_trait = patrol.patrol_event.win_trait
                patrol_trait = patrol.patrol_traits.index(win_trait)
                patrol.patrol_stat_cat = patrol.patrol_cats[patrol_trait]

            game.switches['event'] = -1

        if game.switches['event'] == -1:
            intro_text = patrol.patrol_event.intro_text
            patrol_size = len(patrol.patrol_cats)

            # adjusting text for solo patrols
            if patrol_size < 2:
                intro_text = intro_text.replace('Your patrol',
                                                str(patrol.patrol_leader.name))
                intro_text = intro_text.replace('The patrol',
                                                str(patrol.patrol_leader.name))
                intro_text = intro_text.replace('o_c_n', str(patrol.other_clan.name) + 'Clan')
                intro_text = intro_text.replace('c_n', str(game.clan.name) + 'Clan')
                if patrol.patrol_stat_cat is not None:
                    intro_text = intro_text.replace('s_c', str(patrol.patrol_stat_cat.name))
            intro_text = patrol.patrol_event.intro_text
            intro_text = intro_text.replace('r_c',
                                            str(patrol.patrol_random_cat.name))
            intro_text = intro_text.replace('p_l',
                                            str(patrol.patrol_leader.name))
            intro_text = intro_text.replace('o_c_n', str(patrol.other_clan.name) + 'Clan')
            intro_text = intro_text.replace('c_n', str(game.clan.name) + 'Clan')

            if patrol.patrol_stat_cat is not None:
                intro_text = intro_text.replace('s_c', str(patrol.patrol_stat_cat.name))

            verdana_dark.blit_text(intro_text,
                              (390, 185),
                              x_limit=715)

            if game.switches['patrol_done'] is False:
                buttons.draw_button((550, 433),
                                    image='buttons/proceed',
                                    text='Proceed',
                                    patrol_done=True,
                                    event=-2)
                buttons.draw_button((550, 461),
                                    image='buttons/do_not_proceed',
                                    text='Do Not Proceed',
                                    patrol_done=True,
                                    event=2)

                if patrol.patrol_event.patrol_id in [500, 501, 502, 503, 504, 505, 510, 800, 801, 802, 803, 804, 805]:
                    buttons.draw_button((550, 491),
                                        image='buttons/antagonize',
                                        text='Antagonize',
                                        patrol_done=True,
                                        event=3)

        if game.switches['event'] == -2:
            patrol.calculate_success()
            game.switches['event'] = 1

        elif game.switches['event'] == 3:
            patrol.calculate_success_antagonize()
            game.switches['event'] = 4

        if game.switches['event'] > 0:
            if game.switches['event'] == 1:
                if patrol.success:
                    success_text = patrol.patrol_event.success_text
                    patrol_size = len(patrol.patrol_cats)

                    # adjusting text for solo patrols
                    if patrol_size < 2:
                        success_text = success_text.replace('Your patrol',
                                                        str(patrol.patrol_leader.name))
                        success_text = success_text.replace('The patrol',
                                                        str(patrol.patrol_leader.name))
                        success_text = success_text.replace(
                        'o_c_n', str(patrol.other_clan.name) + 'Clan')
                        success_text = success_text.replace(
                            'c_n', str(game.clan.name) + 'Clan')
                        if patrol.patrol_stat_cat is not None:
                            success_text = success_text.replace(
                            's_c', str(patrol.patrol_stat_cat.name))
                    success_text = success_text.replace(
                        'r_c', str(patrol.patrol_random_cat.name))
                    success_text = success_text.replace(
                        'p_l', str(patrol.patrol_leader.name))
                    success_text = success_text.replace(
                        'o_c_n', str(patrol.other_clan.name) + 'Clan')
                    success_text = success_text.replace(
                        'c_n', str(game.clan.name) + 'Clan')

                    if patrol.patrol_stat_cat is not None:
                        success_text = success_text.replace(
                        's_c', str(patrol.patrol_stat_cat.name))

                    verdana_dark.blit_text(success_text,
                                      (390, 185),
                                      x_limit=715)

                else:
                    fail_text = patrol.patrol_event.fail_text
                    patrol_size = len(patrol.patrol_cats)

                    # adjusting text for solo patrols
                    if patrol_size < 2:
                        fail_text = fail_text.replace('Your patrol',
                                                            str(patrol.patrol_leader.name))
                        fail_text = fail_text.replace('The patrol',
                                                            str(patrol.patrol_leader.name))
                        fail_text = fail_text.replace(
                        'o_c_n', str(patrol.other_clan.name) + 'Clan')
                        fail_text = fail_text.replace(
                        'c_n', str(game.clan.name) + 'Clan')
                        if patrol.patrol_stat_cat is not None:
                            fail_text = fail_text.replace(
                            's_c', str(patrol.patrol_stat_cat.name))
                    fail_text = fail_text.replace(
                        'r_c', str(patrol.patrol_random_cat.name))
                    fail_text = fail_text.replace(
                        'p_l', str(patrol.patrol_leader.name))
                    fail_text = fail_text.replace(
                        'o_c_n', str(patrol.other_clan.name) + 'Clan')
                    fail_text = fail_text.replace(
                        'c_n', str(game.clan.name) + 'Clan')

                    if patrol.patrol_stat_cat is not None:
                        fail_text = fail_text.replace(
                        's_c', str(patrol.patrol_stat_cat.name))

                    verdana_dark.blit_text(fail_text,
                                      (390, 185),
                                      x_limit=715)

            elif game.switches['event'] == 2:
                decline_text = patrol.patrol_event.decline_text
                patrol_size = len(patrol.patrol_cats)

                # adjusting text for solo patrols
                if patrol_size < 2:
                    decline_text = decline_text.replace('Your patrol',
                                                        str(patrol.patrol_leader.name))
                    decline_text = decline_text.replace('The patrol',
                                                        str(patrol.patrol_leader.name))
                    decline_text = decline_text.replace(
                        'o_c_n', str(patrol.other_clan.name) + 'Clan')
                    decline_text = decline_text.replace(
                        'c_n', str(game.clan.name) + 'Clan')
                decline_text = decline_text.replace(
                    'r_c', str(patrol.patrol_random_cat.name))
                decline_text = decline_text.replace(
                    'p_l', str(patrol.patrol_leader.name))
                decline_text = decline_text.replace(
                        'o_c_n', str(patrol.other_clan.name) + 'Clan')
                decline_text = decline_text.replace(
                        'c_n', str(game.clan.name) + 'Clan')

                if patrol.patrol_stat_cat is not None:
                        decline_text = decline_text.replace(
                        's_c', str(patrol.patrol_stat_cat.name))

                verdana_dark.blit_text(decline_text,
                                  (390, 185),
                                  x_limit=715)

            elif game.switches['event'] == 4:
                antagonize_text = patrol.patrol_event.antagonize_text
                patrol_size = len(patrol.patrol_cats)

                # adjusting text for solo patrols
                if patrol.success:
                    if patrol_size < 2:  # adjusting text for solo patrols
                        antagonize_text = antagonize_text.replace('Your patrol', str(patrol.patrol_leader.name))
                        antagonize_text = antagonize_text.replace('The patrol', str(patrol.patrol_leader.name))
                        antagonize_text = antagonize_text.replace(
                            'o_c_n', str(patrol.other_clan.name) + 'Clan')
                        antagonize_text = antagonize_text.replace(
                            'c_n', str(game.clan.name) + 'Clan')
                        if patrol.patrol_stat_cat is not None:
                            antagonize_text = antagonize_text.replace(
                            's_c', str(patrol.patrol_stat_cat.name))
                    antagonize_text = antagonize_text.replace(
                        'r_c', str(patrol.patrol_random_cat.name))
                    antagonize_text = antagonize_text.replace(
                        'p_l', str(patrol.patrol_leader.name))
                    antagonize_text = antagonize_text.replace(
                            'o_c_n', str(patrol.other_clan.name) + 'Clan')
                    antagonize_text = antagonize_text.replace(
                            'c_n', str(game.clan.name) + 'Clan')

                    if patrol.patrol_stat_cat is not None:
                            antagonize_text = antagonize_text.replace(
                            's_c', str(patrol.patrol_stat_cat.name))

                else:
                    antagonize_fail_text = patrol.patrol_event.antagonize_fail_text

                    # adjusting text for solo patrols
                    if patrol_size < 2:
                        antagonize_fail_text = antagonize_fail_text.replace('Your patrol',
                                                            str(patrol.patrol_leader.name))
                        antagonize_fail_text = antagonize_fail_text.replace('The patrol',
                                                            str(patrol.patrol_leader.name))
                        antagonize_fail_text = antagonize_fail_text.replace(
                            'o_c_n', str(patrol.other_clan.name) + 'Clan')
                        antagonize_fail_text = antagonize_fail_text.replace(
                            'c_n', str(game.clan.name) + 'Clan')
                        if patrol.patrol_stat_cat is not None:
                            antagonize_fail_text = antagonize_fail_text.replace(
                            's_c', str(patrol.patrol_stat_cat.name))
                    antagonize_fail_text = antagonize_fail_text.replace(
                        'r_c', str(patrol.patrol_random_cat.name))
                    antagonize_fail_text = antagonize_fail_text.replace(
                        'p_l', str(patrol.patrol_leader.name))
                    antagonize_fail_text = antagonize_fail_text.replace(
                            'o_c_n', str(patrol.other_clan.name) + 'Clan')
                    antagonize_fail_text = antagonize_fail_text.replace(
                            'c_n', str(game.clan.name) + 'Clan')

                    if patrol.patrol_stat_cat is not None:
                            antagonize_fail_text = antagonize_fail_text.replace(
                            's_c', str(patrol.patrol_stat_cat.name))

                verdana_dark.blit_text(antagonize_text,
                                  (390, 185),
                                  x_limit=715)

            if game.switches['patrol_done'] is True:
                buttons.draw_image_button((400, 137),
                                          button_name='back_to_clan',
                                          text='Return to Clan',
                                          size=(162, 30),
                                          cur_screen='clan screen',
                                          patrol_done=False)
                buttons.draw_image_button((560, 137),
                                          button_name='patrol_again',
                                          text='Patrol Again',
                                          size=(162, 30),
                                          cur_screen='patrol screen',
                                          patrol_done=False)

                buttons.draw_button((550, 433),
                                    image='buttons/proceed',
                                    text='Proceed',
                                    patrol_done=True,
                                    available=False,
                                    event=-2)
                buttons.draw_button((550, 461),
                                    image='buttons/do_not_proceed',
                                    text='Do Not Proceed',
                                    patrol_done=True,
                                    available=False,
                                    event=2)
        pos_x = 0
        pos_y = 0
        for u in range(6):
            if u < len(patrol.patrol_cats):
                draw(patrol.patrol_cats[u],
                     (400 + pos_x, 475 + pos_y))
                pos_x += 50
                if pos_x > 50:
                    pos_y += 50
                    pos_x = 0

        # TEXT CATEGORIES AND CHECKING FOR REPEATS
        members = []
        skills = []
        traits = []
        for x in patrol.patrol_names:
            if x not in patrol.patrol_leader_name:
                members.append(x)
        for x in patrol.patrol_skills:
            if x not in skills:
                skills.append(x)
        for x in patrol.patrol_traits:
            if x not in traits:
                traits.append(x)


        verdana_small_dark.blit_text(
                                f'patrol leader: {patrol.patrol_leader_name} \n'
                                f'patrol members: {self.get_list_text(members)} \n'
                                f'patrol skills: {self.get_list_text(skills)} \n'
                                f'patrol traits: {self.get_list_text(traits)}',
                                (105, 460),
                                x_limit=345,
                                line_break=25)

        draw_menu_buttons()

    def screen_switches(self):
        game.switches['event'] = 0
        game.switches['patrol_done'] = False
        cat_profiles()

