import dearpygui.dearpygui as dpg

from object_registry import object_registry
from decorator import add_to_registry_decorator

class ToolBar:
    @add_to_registry_decorator
    def __init__(self, name):
        self.name = name
        self.buttons = []

    def display(self):
        if dpg.does_item_exist(self.name):
            dpg.delete_item(self.name)

        plot_pos = dpg.get_item_pos("pdf_plot")
        
        with dpg.group(horizontal=True, tag=self.name, parent="canvas_window"):
            for button in self.buttons:
                dpg.add_button(label="Draw")
                dpg.add_button(label="Textbox") 
        # if dpg.does_item_exist(self.name):
        #     dpg.show_item(self.name)

    def add_to_registry(self):
        object_registry.register_object(self.name, self)



