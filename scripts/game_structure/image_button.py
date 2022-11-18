import pygame
import pygame_gui

class UIImageButton(pygame_gui.elements.UIButton):
    def __init__(self, relative_rect, text = "", manager = None, container= None, 
    tool_tip_text = None, starting_height: int = 1, parent_element = None, 
    object_id = None, anchors = None, allow_double_clicks: bool = False, 
    visible: int = 1, text_kwargs = None):
        

        
        super().__init__(relative_rect, text, 
        manager=manager, 
        container=container, 
        tool_tip_text=tool_tip_text, 
        starting_height=starting_height, 
        parent_element=parent_element, 
        object_id=object_id, 
        anchors = anchors, 
        allow_double_clicks = allow_double_clicks, 
        visible = visible, \
        text_kwargs=text_kwargs)

    def _set_any_images_from_theme(self):

        changed = False
        normal_image = None
        try:
            normal_image = self.ui_theme.get_image('normal_image', self.combined_element_ids)
            normal_image = pygame.transform.scale(normal_image, self.relative_rect.size)  # auto-rescale the image
        except LookupError:
            normal_image = None
        finally:
            if normal_image != self.normal_image:
                self.normal_image = normal_image
                self.hovered_image = normal_image
                self.selected_image = normal_image
                self.disabled_image = normal_image
                changed = True

        hovered_image = None
        try:
            hovered_image = self.ui_theme.get_image('hovered_image', self.combined_element_ids)
            hovered_image = pygame.transform.scale(hovered_image, self.relative_rect.size)  # auto-rescale the image
        except LookupError:
            hovered_image = self.normal_image
        finally:
            if hovered_image != self.hovered_image:
                self.hovered_image = hovered_image
                changed = True

        selected_image = None
        try:
            selected_image = self.ui_theme.get_image('selected_image', self.combined_element_ids)
            selected_image = pygame.transform.scale(selected_image, self.relative_rect.size)  # auto-rescale the image
        except LookupError:
            selected_image = self.normal_image
        finally:
            if selected_image != self.selected_image:
                self.selected_image = selected_image
                changed = True

        disabled_image = None
        try:
            disabled_image = self.ui_theme.get_image('disabled_image', self.combined_element_ids)
            disabled_image = pygame.transform.scale(disabled_image, self.relative_rect.size)  # auto-rescale the image
        except LookupError:
            disabled_image = self.normal_image
        finally:
            if disabled_image != self.disabled_image:
                self.disabled_image = disabled_image
                changed = True

        return changed